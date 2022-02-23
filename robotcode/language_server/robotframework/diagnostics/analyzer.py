from __future__ import annotations

import ast
import asyncio
import re
from typing import Any, List, Optional, Union, cast

from ....utils.async_tools import CancelationToken
from ....utils.uri import Uri
from ...common.lsp_types import (
    CodeDescription,
    Diagnostic,
    DiagnosticRelatedInformation,
    DiagnosticSeverity,
    DiagnosticTag,
    Location,
    Position,
    Range,
)
from ...common.text_document import TextDocument
from ..utils.ast import (
    Token,
    is_not_variable_token,
    range_from_node_or_token,
    range_from_token,
)
from ..utils.async_ast import AsyncVisitor
from .library_doc import KeywordDoc, is_embedded_keyword
from .namespace import DIAGNOSTICS_SOURCE_NAME, KeywordFinder, Namespace

EXTRACT_COMMENT_PATTERN = re.compile(r".*(?:^ *|\t+| {2,})#(?P<comment>.*)$")
ROBOTCODE_PATTERN = re.compile(r"(?P<marker>\brobotcode\b)\s*:\s*(?P<rule>\b\w+\b)")


class Analyzer(AsyncVisitor):
    async def get(
        self, model: ast.AST, namespace: Namespace, cancelation_token: Optional[CancelationToken] = None
    ) -> List[Diagnostic]:
        self._results: List[Diagnostic] = []
        self._namespace = namespace
        self.cancelation_token = cancelation_token
        self.current_testcase_or_keyword_name: Optional[str] = None
        self.finder = KeywordFinder(self._namespace)

        await self.visit(model)
        return self._results

    async def visit(self, node: ast.AST) -> None:
        await super().visit(node)

    @staticmethod
    async def should_ignore(document: Optional[TextDocument], range: Range) -> bool:
        import builtins

        if document is not None:
            lines = await document.get_lines()
            for line_no in builtins.range(range.start.line, range.end.line + 1):
                line = lines[line_no]

                comment = EXTRACT_COMMENT_PATTERN.match(line)
                if comment and comment.group("comment"):
                    for match in ROBOTCODE_PATTERN.finditer(comment.group("comment")):

                        if match.group("rule") == "ignore":
                            return True

        return False

    async def append_diagnostics(
        self,
        range: Range,
        message: str,
        severity: Optional[DiagnosticSeverity] = None,
        code: Union[int, str, None] = None,
        code_description: Optional[CodeDescription] = None,
        source: Optional[str] = None,
        tags: Optional[List[DiagnosticTag]] = None,
        related_information: Optional[List[DiagnosticRelatedInformation]] = None,
        data: Optional[Any] = None,
    ) -> None:
        if await self.should_ignore(self._namespace.document, range):
            return

        self._results.append(
            Diagnostic(range, message, severity, code, code_description, source, tags, related_information, data)
        )

    async def _analyze_keyword_call(
        self,
        keyword: Optional[str],
        node: ast.AST,
        keyword_token: Token,
        argument_tokens: List[Token],
        analyse_run_keywords: bool = True,
    ) -> Optional[KeywordDoc]:
        from robot.parsing.model.statements import Template, TestTemplate

        result: Optional[KeywordDoc] = None

        try:
            if not is_not_variable_token(keyword_token):
                return None

            result = await self.finder.find_keyword(keyword)

            for e in self.finder.diagnostics:
                await self.append_diagnostics(
                    range=range_from_node_or_token(node, keyword_token),
                    message=e.message,
                    severity=e.severity,
                    source=DIAGNOSTICS_SOURCE_NAME,
                    code=e.code,
                )

            if result is not None:
                if result.errors:
                    await self.append_diagnostics(
                        range=range_from_node_or_token(node, keyword_token),
                        message="Keyword definition contains errors.",
                        severity=DiagnosticSeverity.ERROR,
                        source=DIAGNOSTICS_SOURCE_NAME,
                        related_information=[
                            DiagnosticRelatedInformation(
                                location=Location(
                                    uri=str(
                                        Uri.from_path(
                                            err.source
                                            if err.source is not None
                                            else result.source
                                            if result.source is not None
                                            else "/<unknown>"
                                        )
                                    ),
                                    range=Range(
                                        start=Position(
                                            line=err.line_no - 1
                                            if err.line_no is not None
                                            else result.line_no
                                            if result.line_no >= 0
                                            else 0,
                                            character=0,
                                        ),
                                        end=Position(
                                            line=err.line_no - 1
                                            if err.line_no is not None
                                            else result.line_no
                                            if result.line_no >= 0
                                            else 0,
                                            character=0,
                                        ),
                                    ),
                                ),
                                message=err.message,
                            )
                            for err in result.errors
                        ],
                    )

                if result.is_deprecated:
                    await self.append_diagnostics(
                        range=range_from_node_or_token(node, keyword_token),
                        message=f"Keyword '{result.name}' is deprecated"
                        f"{f': {result.deprecated_message}' if result.deprecated_message else ''}.",
                        severity=DiagnosticSeverity.HINT,
                        source=DIAGNOSTICS_SOURCE_NAME,
                        tags=[DiagnosticTag.Deprecated],
                    )
                if result.is_error_handler:
                    await self.append_diagnostics(
                        range=range_from_node_or_token(node, keyword_token),
                        message=f"Keyword definition contains errors: {result.error_handler_message}",
                        severity=DiagnosticSeverity.ERROR,
                        source=DIAGNOSTICS_SOURCE_NAME,
                    )

                if not isinstance(node, (Template, TestTemplate)):
                    try:
                        if result.arguments is not None:
                            result.arguments.resolve(
                                [v.value for v in argument_tokens],
                                None,
                                resolve_variables_until=result.args_to_process,
                                resolve_named=not result.is_any_run_keyword(),
                            )
                    except (asyncio.CancelledError, SystemExit, KeyboardInterrupt):
                        raise
                    except BaseException as e:
                        await self.append_diagnostics(
                            range=Range(
                                start=range_from_token(keyword_token).start,
                                end=range_from_token(argument_tokens[-1]).end
                                if argument_tokens
                                else range_from_token(keyword_token).end,
                            ),
                            message=str(e),
                            severity=DiagnosticSeverity.ERROR,
                            source=DIAGNOSTICS_SOURCE_NAME,
                            code=type(e).__qualname__,
                        )

        except (asyncio.CancelledError, SystemExit, KeyboardInterrupt):
            raise
        except BaseException as e:
            await self.append_diagnostics(
                range=range_from_node_or_token(node, keyword_token),
                message=str(e),
                severity=DiagnosticSeverity.ERROR,
                source=DIAGNOSTICS_SOURCE_NAME,
                code=type(e).__qualname__,
            )

        if result is not None and analyse_run_keywords:
            await self._analyse_run_keyword(result, node, argument_tokens)

        return result

    async def _analyse_run_keyword(
        self, keyword_doc: Optional[KeywordDoc], node: ast.AST, argument_tokens: List[Token]
    ) -> List[Token]:
        from robot.utils.escaping import unescape

        if keyword_doc is None or not keyword_doc.is_any_run_keyword():
            return argument_tokens

        if keyword_doc.is_run_keyword() and len(argument_tokens) > 0 and is_not_variable_token(argument_tokens[0]):
            await self._analyze_keyword_call(
                unescape(argument_tokens[0].value), node, argument_tokens[0], argument_tokens[1:]
            )

            return argument_tokens[1:]
        elif (
            keyword_doc.is_run_keyword_with_condition()
            and len(argument_tokens) > (cond_count := keyword_doc.run_keyword_condition_count())
            and is_not_variable_token(argument_tokens[cond_count])
        ):
            await self._analyze_keyword_call(
                unescape(argument_tokens[cond_count].value),
                node,
                argument_tokens[cond_count],
                argument_tokens[cond_count + 1 :],
            )
            return argument_tokens[cond_count + 1 :]
        elif keyword_doc.is_run_keywords():
            has_and = False
            while argument_tokens:

                t = argument_tokens[0]
                argument_tokens = argument_tokens[1:]
                if t.value == "AND":
                    await self.append_diagnostics(
                        range=range_from_token(t),
                        message=f"Incorrect use of {t.value}",
                        severity=DiagnosticSeverity.ERROR,
                        source=DIAGNOSTICS_SOURCE_NAME,
                    )
                    continue

                if not is_not_variable_token(t):
                    continue

                and_token = next((e for e in argument_tokens if e.value == "AND"), None)
                args = []
                if and_token is not None:
                    args = argument_tokens[: argument_tokens.index(and_token)]
                    argument_tokens = argument_tokens[argument_tokens.index(and_token) + 1 :]
                    has_and = True
                elif has_and:
                    args = argument_tokens
                    argument_tokens = []

                await self._analyze_keyword_call(unescape(t.value), node, t, args)

            return []

        elif keyword_doc.is_run_keyword_if() and len(argument_tokens) > 1:

            def skip_args() -> List[Token]:
                nonlocal argument_tokens
                result = []
                while argument_tokens:
                    if argument_tokens[0].value in ["ELSE", "ELSE IF"]:
                        break
                    if argument_tokens:
                        result.append(argument_tokens[0])
                    argument_tokens = argument_tokens[1:]

                return result

            result = await self.finder.find_keyword(argument_tokens[1].value)

            if result is not None and result.is_any_run_keyword():
                argument_tokens = argument_tokens[2:]

                argument_tokens = await self._analyse_run_keyword(result, node, argument_tokens)
            else:
                kwt = argument_tokens[1]
                argument_tokens = argument_tokens[2:]

                args = skip_args()

                if is_not_variable_token(kwt):
                    await self._analyze_keyword_call(
                        unescape(kwt.value),
                        node,
                        kwt,
                        args,
                        analyse_run_keywords=False,
                    )

            while argument_tokens:
                if argument_tokens[0].value == "ELSE" and len(argument_tokens) > 1:

                    result = await self._analyze_keyword_call(
                        unescape(argument_tokens[1].value),
                        node,
                        argument_tokens[1],
                        argument_tokens[2:],
                        analyse_run_keywords=False,
                    )

                    argument_tokens = argument_tokens[2:]

                    if result is not None and result.is_any_run_keyword():
                        argument_tokens = await self._analyse_run_keyword(result, node, argument_tokens)

                    skip_args()

                    break
                elif argument_tokens[0].value == "ELSE IF" and len(argument_tokens) > 2:

                    result = await self._analyze_keyword_call(
                        unescape(argument_tokens[2].value),
                        node,
                        argument_tokens[2],
                        argument_tokens[3:],
                        analyse_run_keywords=False,
                    )

                    argument_tokens = argument_tokens[3:]

                    if result is not None and result.is_any_run_keyword():
                        argument_tokens = await self._analyse_run_keyword(result, node, argument_tokens)

                    skip_args()
                else:
                    break

        return argument_tokens

    async def visit_Fixture(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import Fixture

        value = cast(Fixture, node)
        keyword_token = cast(Token, value.get_token(RobotToken.NAME))

        # TODO: calculate possible variables in NAME

        if keyword_token is not None and is_not_variable_token(keyword_token):
            await self._analyze_keyword_call(
                value.name, value, keyword_token, [cast(Token, e) for e in value.get_tokens(RobotToken.ARGUMENT)]
            )

        await self.generic_visit(node)

    async def visit_TestTemplate(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import TestTemplate

        value = cast(TestTemplate, node)
        keyword_token = cast(Token, value.get_token(RobotToken.NAME))

        # TODO: calculate possible variables in NAME

        if keyword_token is not None and is_not_variable_token(keyword_token):
            await self._analyze_keyword_call(value.value, value, keyword_token, [])

        await self.generic_visit(node)

    async def visit_Template(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import Template

        value = cast(Template, node)
        keyword_token = cast(Token, value.get_token(RobotToken.NAME))

        # TODO: calculate possible variables in NAME

        if keyword_token is not None and is_not_variable_token(keyword_token):
            await self._analyze_keyword_call(value.value, value, keyword_token, [])

        await self.generic_visit(node)

    async def visit_KeywordCall(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import KeywordCall

        value = cast(KeywordCall, node)
        keyword_token = cast(RobotToken, value.get_token(RobotToken.KEYWORD))

        if value.assign and not value.keyword:
            await self.append_diagnostics(
                range=range_from_node_or_token(value, value.get_token(RobotToken.ASSIGN)),
                message="Keyword name cannot be empty.",
                severity=DiagnosticSeverity.ERROR,
                source=DIAGNOSTICS_SOURCE_NAME,
                code="KeywordError",
            )
        else:
            await self._analyze_keyword_call(
                value.keyword, value, keyword_token, [cast(Token, e) for e in value.get_tokens(RobotToken.ARGUMENT)]
            )

        if not self.current_testcase_or_keyword_name:
            await self.append_diagnostics(
                range=range_from_node_or_token(value, value.get_token(RobotToken.ASSIGN)),
                message="Code is unreachable.",
                severity=DiagnosticSeverity.HINT,
                source=DIAGNOSTICS_SOURCE_NAME,
                tags=[DiagnosticTag.Unnecessary],
            )

        await self.generic_visit(node)

    async def visit_TestCase(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.blocks import TestCase
        from robot.parsing.model.statements import TestCaseName

        testcase = cast(TestCase, node)

        if not testcase.name:
            name_token = cast(TestCaseName, testcase.header).get_token(RobotToken.TESTCASE_NAME)
            await self.append_diagnostics(
                range=range_from_node_or_token(testcase, name_token),
                message="Test case name cannot be empty.",
                severity=DiagnosticSeverity.ERROR,
                source=DIAGNOSTICS_SOURCE_NAME,
                code="KeywordError",
            )

        self.current_testcase_or_keyword_name = testcase.name
        try:
            await self.generic_visit(node)
        finally:
            self.current_testcase_or_keyword_name = None

    async def visit_Keyword(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.blocks import Keyword
        from robot.parsing.model.statements import Arguments, KeywordName

        keyword = cast(Keyword, node)

        if keyword.name:

            name_token = cast(KeywordName, keyword.header).get_token(RobotToken.KEYWORD_NAME)
            if is_embedded_keyword(keyword.name) and any(
                isinstance(v, Arguments) and len(v.values) > 0 for v in keyword.body
            ):
                await self.append_diagnostics(
                    range=range_from_node_or_token(keyword, name_token),
                    message="Keyword cannot have both normal and embedded arguments.",
                    severity=DiagnosticSeverity.ERROR,
                    source=DIAGNOSTICS_SOURCE_NAME,
                    code="KeywordError",
                )
        else:
            name_token = cast(KeywordName, keyword.header).get_token(RobotToken.KEYWORD_NAME)
            await self.append_diagnostics(
                range=range_from_node_or_token(keyword, name_token),
                message="Keyword name cannot be empty.",
                severity=DiagnosticSeverity.ERROR,
                source=DIAGNOSTICS_SOURCE_NAME,
                code="KeywordError",
            )

        self.current_testcase_or_keyword_name = keyword.name
        try:
            await self.generic_visit(node)
        finally:
            self.current_testcase_or_keyword_name = None
