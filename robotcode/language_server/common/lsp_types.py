from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from enum import Enum, IntEnum, IntFlag
from reprlib import recursive_repr
from typing import Any, Dict, Final, Iterator, List, Literal, Optional, Tuple, Union

from ...utils.dataclasses import to_camel_case, to_snake_case

DocumentUri = str
URI = str
ProgressToken = Union[str, int]


LSPAny = Any


class ErrorCodes:
    PARSE_ERROR: Final = -32700
    INVALID_REQUEST: Final = -32600
    METHOD_NOT_FOUND: Final = -32601
    INVALID_PARAMS: Final = -32602
    INTERNAL_ERROR: Final = -32603
    SERVER_ERROR_START: Final = -32000
    SERVER_ERROR_END: Final = -32099

    JSON_RPC_RESERVED_ERROR_RANGE_START: Final = -32099

    SERVER_NOT_INITIALIZED: Final = -32002
    UNKNOWN_ERROR: Final = -32001

    JSON_RPC_RESERVED_ERROR_RANGE_END: Final = -32000

    LSP_RESERVED_ERROR_RANGE_START: Final = -32899
    REQUEST_FAILED: Final = -32803
    SERVER_CANCELLED: Final = -32802
    CONTENT_MODIFIED: Final = -32801
    REQUEST_CANCELLED: Final = -32800
    LSP_RESERVED_ERROR_RANGE_END: Final = -32800


@dataclass
class Model:
    @classmethod
    def _encode_case(cls, s: str) -> str:
        return to_camel_case(s)

    @classmethod
    def _decode_case(cls, s: str) -> str:
        return to_snake_case(s)

    @recursive_repr()
    def __repr__(self) -> str:
        args = ", ".join(
            f"{f.name}={getattr(self, f.name)!r}"
            for f in dataclasses.fields(self)
            if f.repr
            and (
                (f.default == dataclasses.MISSING and f.default_factory == dataclasses.MISSING)
                or (f.default != dataclasses.MISSING and f.default != getattr(self, f.name))
                or (f.default_factory != dataclasses.MISSING and getattr(self, f.name) != f.default_factory())
            )
        )
        return f"{self.__class__.__qualname__}({args})"


@dataclass
class CancelParams(Model):
    id: Union[int, str]


@dataclass
class WorkDoneProgressParams(Model):
    work_done_token: Optional[ProgressToken] = None


@dataclass
class ClientInfo(Model):
    name: str
    version: Optional[str] = None


class TraceValue(Enum):
    OFF = "off"
    MESSAGE = "message"
    VERBOSE = "verbose"

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class WorkspaceFolder(Model):
    uri: DocumentUri
    name: str


@dataclass
class TextDocumentSyncClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    will_save: Optional[bool] = None
    will_save_wait_until: Optional[bool] = None
    did_save: Optional[bool] = None


class ResourceOperationKind(Enum):
    CREATE = "create"
    RENAME = "rename"
    DELETE = "delete"

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


class FailureHandlingKind(Enum):
    ABORT = "abort"
    TRANSACTIONAL = "transactional"
    TEXT_ONLY_TRANSACTIONAL = "textOnlyTransactional"
    UNDO = "undo"

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class WorkspaceEditClientCapabilitiesChangeAnnotationSupport(Model):
    groups_on_label: Optional[bool] = None


@dataclass
class WorkspaceEditClientCapabilities(Model):
    document_changes: Optional[bool] = None
    resource_operations: Optional[List[ResourceOperationKind]] = None
    failure_handling: Optional[FailureHandlingKind] = None
    normalizes_line_endings: Optional[bool] = None

    change_annotation_support: Optional[WorkspaceEditClientCapabilitiesChangeAnnotationSupport] = None


@dataclass
class DidChangeConfigurationClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class DidChangeWatchedFilesClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class ExecuteCommandClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class SemanticTokensWorkspaceClientCapabilities(Model):
    refresh_support: Optional[bool] = None


@dataclass
class CodeLensWorkspaceClientCapabilities(Model):
    refresh_support: Optional[bool] = None


class SymbolKind(IntEnum):
    FILE = 1
    MODULE = 2
    NAMESPACE = 3
    PACKAGE = 4
    CLASS = 5
    METHOD = 6
    PROPERTY = 7
    FIELD = 8
    CONSTRUCTOR = 9
    ENUM = 10
    INTERFACE = 11
    FUNCTION = 12
    VARIABLE = 13
    CONSTANT = 14
    STRING = 15
    NUMBER = 16
    BOOLEAN = 17
    ARRAY = 18
    OBJECT = 19
    KEY = 20
    NULL = 21
    ENUMMEMBER = 22
    STRUCT = 23
    EVENT = 24
    OPERATOR = 25
    TYPEPARAMETER = 26

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


class MarkupKind(Enum):
    PLAINTEXT = "plaintext"
    MARKDOWN = "markdown"

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


class CompletionItemTag(IntEnum):
    DEPRECATED = 1

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


class SymbolTag(IntEnum):
    DEPRECATED = 1

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


class InsertTextMode(IntEnum):
    AS_IS = 1
    ADJUST_INDENTATION = 2

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


class InsertTextFormat(Enum):
    PLAINTEXT = 1
    SNIPPET = 2

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class WorkspaceSymbolClientCapabilitiesSymbolKind(Model):
    value_set: List[SymbolKind]


@dataclass
class WorkspaceSymbolClientCapabilitiesTagSupport(Model):
    value_set: List[SymbolTag]


@dataclass
class WorkspaceSymbolClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    symbol_kind: Optional[WorkspaceSymbolClientCapabilitiesSymbolKind] = None
    tag_support: Optional[WorkspaceSymbolClientCapabilitiesTagSupport] = None


class CompletionItemKind(IntEnum):
    TEXT = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    FIELD = 5
    VARIABLE = 6
    CLASS = 7
    INTERFACE = 8
    MODULE = 9
    PROPERTY = 10
    UNIT = 11
    VALUE = 12
    ENUM = 13
    KEYWORD = 14
    SNIPPET = 15
    COLOR = 16
    FILE = 17
    REFERENCE = 18
    FOLDER = 19
    ENUM_MEMBER = 20
    CONSTANT = 21
    STRUCT = 22
    EVENT = 23
    OPERATOR = 24
    TYPE_PARAMETER = 25

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class CompletionClientCapabilitiesCompletionItemTagSupport(Model):
    value_set: List[CompletionItemTag]


@dataclass
class CompletionClientCapabilitiesCompletionItemResolveSupport(Model):
    properties: List[str]


@dataclass
class CompletionClientCapabilitiesCompletionItemInsertTextModeSupport(Model):
    value_set: List[InsertTextMode]


@dataclass
class CompletionClientCapabilitiesCompletionItem(Model):
    snippet_support: Optional[bool] = None
    commit_characters_support: Optional[bool] = None
    documentation_format: Optional[List[MarkupKind]] = None
    deprecated_support: Optional[bool] = None
    preselect_support: Optional[bool] = None
    tag_support: Optional[CompletionClientCapabilitiesCompletionItemTagSupport] = None
    insert_replace_support: Optional[bool] = None
    resolve_support: Optional[CompletionClientCapabilitiesCompletionItemResolveSupport] = None
    insert_text_mode_support: Optional[CompletionClientCapabilitiesCompletionItemInsertTextModeSupport] = None


@dataclass
class CompletionClientCapabilitiesCompletionItemKind(Model):
    value_set: Optional[List[CompletionItemKind]] = None


@dataclass
class CompletionClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    completion_item: Optional[CompletionClientCapabilitiesCompletionItem] = None
    completion_item_kind: Optional[CompletionClientCapabilitiesCompletionItemKind] = None
    context_support: Optional[bool] = None


@dataclass
class HoverClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    content_format: Optional[List[MarkupKind]] = None


@dataclass
class SignatureHelpClientCapabilitiesSignatureInformationParameterInformation(Model):
    label_offset_support: Optional[bool] = None


@dataclass
class SignatureHelpClientCapabilitiesSignatureInformation(Model):
    documentation_format: Optional[List[MarkupKind]] = None
    parameter_information: Optional[SignatureHelpClientCapabilitiesSignatureInformationParameterInformation] = None
    active_parameter_support: Optional[bool] = None


@dataclass
class SignatureHelpClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    signature_information: Optional[SignatureHelpClientCapabilitiesSignatureInformation] = None
    context_support: Optional[bool] = None


@dataclass
class DeclarationClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    link_support: Optional[bool] = None


@dataclass
class DefinitionClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    link_support: Optional[bool] = None


@dataclass
class TypeDefinitionClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    link_support: Optional[bool] = None


@dataclass
class ImplementationClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    link_support: Optional[bool] = None


@dataclass
class ReferenceClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class DocumentHighlightClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class DocumentSymbolClientCapabilitiesSymbolKind(Model):
    value_set: Optional[List[SymbolKind]] = None


@dataclass
class DocumentSymbolClientCapabilitiesTagSupport(Model):
    value_set: List[SymbolTag]


@dataclass
class DocumentSymbolClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    symbol_kind: Optional[DocumentSymbolClientCapabilitiesSymbolKind] = None
    hierarchical_document_symbol_support: Optional[bool] = None
    tag_support: Optional[DocumentSymbolClientCapabilitiesTagSupport] = None
    label_support: Optional[bool] = None


class CodeActionKinds:
    EMPTY = ""
    QUICKFIX = "quickfix"
    REFACTOR = "refactor"
    REFACTOR_EXTRACT = "refactor.extract"
    REFACTOR_INLINE = "refactor.inline"
    REFACTOR_REWRITE = "refactor.rewrite"
    SOURCE = "source"
    SOURCE_ORGANIZE_IMPORTS = "source.organizeImports"
    SOURCE_FIX_ALL = "source.fixAll"


CodeActionKind = str


@dataclass
class CodeActionClientCapabilitiesCodeActionLiteralSupportCodeActionKind(Model):
    value_set: Optional[List[CodeActionKind]] = None


@dataclass
class CodeActionClientCapabilitiesCodeActionLiteralSupport(Model):
    code_action_kind: CodeActionClientCapabilitiesCodeActionLiteralSupportCodeActionKind


@dataclass
class CodeActionClientCapabilitiesResolveSupport(Model):
    properties: List[str]


@dataclass
class CodeActionClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    code_action_literal_support: Optional[CodeActionClientCapabilitiesCodeActionLiteralSupport] = None
    is_preferred_support: Optional[bool] = None
    disabled_support: Optional[bool] = None
    data_support: Optional[bool] = None
    resolve_support: Optional[CodeActionClientCapabilitiesResolveSupport] = None
    honors_change_annotations: Optional[bool] = None


@dataclass
class CodeLensClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class DocumentLinkClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    tooltip_support: Optional[bool] = None


@dataclass
class DocumentColorClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class DocumentFormattingClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class DocumentRangeFormattingClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class DocumentOnTypeFormattingClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class PrepareSupportDefaultBehavior(IntEnum):
    Identifier = 1

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class RenameClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    prepare_support: Optional[bool] = None
    prepare_support_default_behavior: Optional[PrepareSupportDefaultBehavior] = None
    honors_change_annotations: Optional[bool] = None


class DiagnosticTag(IntEnum):
    Unnecessary = 1
    Deprecated = 2

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class PublishDiagnosticsClientCapabilitiesTagSupport(Model):
    value_set: List[DiagnosticTag]


@dataclass
class PublishDiagnosticsClientCapabilities(Model):
    related_information: Optional[bool] = None
    tag_support: Optional[PublishDiagnosticsClientCapabilitiesTagSupport] = None
    version_support: Optional[bool] = None
    code_description_support: Optional[bool] = None
    data_support: Optional[bool] = None


class FoldingRangeKind(Enum):
    COMMENT = "comment"
    IMPORTS = "imports"
    REGION = "region"

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class FoldingRangeClientCapabilitiesFoldingRangeKind(Model):
    value_set: Optional[List[FoldingRangeKind]]


@dataclass
class FoldingRangeClientCapabilitiesFoldingRange(Model):
    collapsed_text: Optional[bool] = None


@dataclass
class FoldingRangeClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    range_limit: Optional[int] = None
    line_folding_only: Optional[bool] = None
    folding_range_kind: Optional[FoldingRangeClientCapabilitiesFoldingRangeKind] = None
    folding_range: Optional[FoldingRangeClientCapabilitiesFoldingRange] = None


@dataclass
class SelectionRangeClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class LinkedEditingRangeClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class CallHierarchyClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


class TokenFormat(Enum):
    Relative = "relative"

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class SemanticTokensClientCapabilitiesRequestsFull(Model):
    delta: Optional[bool] = None


@dataclass
class SemanticTokensClientCapabilitiesRequests(Model):
    range: Union[bool, Dict[Any, Any], None] = None
    full: Union[SemanticTokensClientCapabilitiesRequestsFull, bool, None] = None


@dataclass
class SemanticTokensClientCapabilities(Model):
    requests: SemanticTokensClientCapabilitiesRequests
    token_types: List[str]
    token_modifiers: List[str]
    formats: List[TokenFormat]
    overlapping_token_support: Optional[bool] = None
    multiline_token_support: Optional[bool] = None
    server_cancel_support: Optional[bool] = None
    augments_syntax_tokens: Optional[bool] = None
    dynamic_registration: Optional[bool] = None


@dataclass
class MonikerClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class InlayHintClientCapabilitiesResolveSupport(Model):
    properties: List[str]


@dataclass
class InlayHintClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    resolve_support: Optional[InlayHintClientCapabilitiesResolveSupport] = None


@dataclass
class InlineValueClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None


@dataclass
class DiagnosticClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    related_document_support: Optional[bool] = None


@dataclass
class TextDocumentClientCapabilities(Model):
    synchronization: Optional[TextDocumentSyncClientCapabilities] = None
    completion: Optional[CompletionClientCapabilities] = None
    hover: Optional[HoverClientCapabilities] = None
    signature_help: Optional[SignatureHelpClientCapabilities] = None
    declaration: Optional[DeclarationClientCapabilities] = None
    definition: Optional[DefinitionClientCapabilities] = None
    type_definition: Optional[TypeDefinitionClientCapabilities] = None
    implementation: Optional[ImplementationClientCapabilities] = None
    references: Optional[ReferenceClientCapabilities] = None
    document_highlight: Optional[DocumentHighlightClientCapabilities] = None
    document_symbol: Optional[DocumentSymbolClientCapabilities] = None
    code_action: Optional[CodeActionClientCapabilities] = None
    code_lens: Optional[CodeLensClientCapabilities] = None
    document_link: Optional[DocumentLinkClientCapabilities] = None
    color_provider: Optional[DocumentColorClientCapabilities] = None
    formatting: Optional[DocumentFormattingClientCapabilities] = None
    range_formatting: Optional[DocumentRangeFormattingClientCapabilities] = None
    on_type_formatting: Optional[DocumentOnTypeFormattingClientCapabilities] = None
    rename: Optional[RenameClientCapabilities] = None
    publish_diagnostics: Optional[PublishDiagnosticsClientCapabilities] = None
    folding_range: Optional[FoldingRangeClientCapabilities] = None
    selection_range: Optional[SelectionRangeClientCapabilities] = None
    linked_editing_range: Optional[LinkedEditingRangeClientCapabilities] = None
    call_hierarchy: Optional[CallHierarchyClientCapabilities] = None
    semantic_tokens: Optional[SemanticTokensClientCapabilities] = None
    moniker: Optional[MonikerClientCapabilities] = None
    # TODO typeHierarchy?: TypeHierarchyClientCapabilities;
    inline_value: Optional[InlineValueClientCapabilities] = None
    inlay_hint: Optional[InlayHintClientCapabilities] = None
    diagnostic: Optional[DiagnosticClientCapabilities] = None


@dataclass
class ShowMessageRequestClientCapabilitiesMessageActionItem(Model):
    additional_properties_support: Optional[bool] = None


@dataclass
class ShowMessageRequestClientCapabilities(Model):
    message_action_item: Optional[ShowMessageRequestClientCapabilitiesMessageActionItem] = None


@dataclass
class ShowDocumentClientCapabilities(Model):
    support: bool


@dataclass
class RegularExpressionsClientCapabilities(Model):
    engine: str
    version: Optional[str] = None


@dataclass
class MarkdownClientCapabilities(Model):
    parser: str
    version: Optional[str] = None
    allowed_tags: Optional[List[str]] = None


@dataclass
class ClientCapabilitiesWorkspaceFileOperationsWorkspaceClientCapabilities(Model):
    dynamic_registration: Optional[bool] = None
    did_create: Optional[bool] = None
    will_create: Optional[bool] = None
    did_rename: Optional[bool] = None
    will_rename: Optional[bool] = None
    did_delete: Optional[bool] = None
    will_delete: Optional[bool] = None


@dataclass
class InlineValueWorkspaceClientCapabilities(Model):
    refresh_support: Optional[bool] = None


@dataclass
class InlayHintWorkspaceClientCapabilities(Model):
    refresh_support: Optional[bool] = None


@dataclass
class DiagnosticWorkspaceClientCapabilities(Model):
    refresh_support: Optional[bool] = None


@dataclass
class ClientCapabilitiesWorkspace(Model):
    apply_edit: Optional[bool] = None
    workspace_edit: Optional[WorkspaceEditClientCapabilities] = None
    did_change_configuration: Optional[DidChangeConfigurationClientCapabilities] = None
    did_change_watched_files: Optional[DidChangeWatchedFilesClientCapabilities] = None
    symbol: Optional[WorkspaceSymbolClientCapabilities] = None
    execute_command: Optional[ExecuteCommandClientCapabilities] = None
    workspace_folders: Optional[bool] = None
    configuration: Optional[bool] = None
    semantic_tokens: Optional[SemanticTokensWorkspaceClientCapabilities] = None
    code_lens: Optional[CodeLensWorkspaceClientCapabilities] = None
    file_operations: Optional[ClientCapabilitiesWorkspaceFileOperationsWorkspaceClientCapabilities] = None
    inline_value: Optional[InlineValueWorkspaceClientCapabilities] = None
    inlay_hint: Optional[InlayHintWorkspaceClientCapabilities] = None
    diagnostics: Optional[DiagnosticWorkspaceClientCapabilities] = None


@dataclass
class ClientCapabilitiesWindow(Model):
    work_done_progress: Optional[bool] = None
    show_message: Optional[ShowMessageRequestClientCapabilities] = None
    show_document: Optional[ShowDocumentClientCapabilities] = None


PositionEncodingKind = str

UTF8: PositionEncodingKind = "utf-8"
UTF16: PositionEncodingKind = "utf-16"
UTF32: PositionEncodingKind = "utf-32"


@dataclass
class ClientCapabilitiesGeneral(Model):
    regular_expressions: Optional[RegularExpressionsClientCapabilities] = None
    markdown: Optional[MarkdownClientCapabilities] = None
    position_encodings: Optional[List[PositionEncodingKind]] = None


@dataclass
class ClientCapabilities(Model):
    workspace: Optional[ClientCapabilitiesWorkspace] = None
    text_document: Optional[TextDocumentClientCapabilities] = None
    window: Optional[ClientCapabilitiesWindow] = None
    general: Optional[ClientCapabilitiesGeneral] = None
    experimental: Optional[Any] = None


@dataclass
class _InitializeParams:
    capabilities: ClientCapabilities
    process_id: Optional[int] = None
    client_info: Optional[ClientInfo] = None
    locale: Optional[str] = None
    root_path: Optional[str] = None
    root_uri: Optional[DocumentUri] = None
    initialization_options: Optional[Any] = None
    trace: Optional[TraceValue] = None
    workspace_folders: Optional[List[WorkspaceFolder]] = None


@dataclass
class InitializeParams(WorkDoneProgressParams, _InitializeParams):
    pass


@dataclass
class InitializeError(Model):
    retry: bool


@dataclass
class WorkspaceFoldersServerCapabilities(Model):
    supported: Optional[bool] = None
    change_notifications: Union[str, bool, None] = None


class FileOperationPatternKind(Enum):
    FILE = "file"
    FOLDER = "folder"

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class FileOperationPatternOptions(Model):
    ignore_case: Optional[bool] = None


@dataclass
class FileOperationPattern(Model):
    glob: str
    matches: Optional[FileOperationPatternKind] = None
    options: Optional[FileOperationPatternOptions] = None


@dataclass
class FileOperationFilter(Model):
    pattern: FileOperationPattern
    scheme: Optional[str] = None


@dataclass
class FileOperationRegistrationOptions(Model):
    filters: List[FileOperationFilter]


class TextDocumentSyncKind(Enum):
    NONE = 0
    FULL = 1
    INCREMENTAL = 2

    def __repr__(self) -> str:
        return super().__str__()


@dataclass
class SaveOptions(Model):
    include_text: Optional[bool]


@dataclass
class TextDocumentSyncOptions(Model):
    open_close: Optional[bool] = None
    change: Optional[TextDocumentSyncKind] = None
    will_save: Optional[bool] = None
    will_save_wait_until: Optional[bool] = None
    save: Union[bool, SaveOptions, None] = None


@dataclass
class WorkDoneProgressOptions(Model):
    work_done_progress: Optional[bool] = None


@dataclass
class DocumentFilter(Model):
    language: Optional[str] = None
    scheme: Optional[str] = None
    pattern: Optional[str] = None


DocumentSelector = List[DocumentFilter]


@dataclass
class TextDocumentRegistrationOptions(Model):
    document_selector: Optional[DocumentSelector] = None


@dataclass
class StaticRegistrationOptions(Model):
    id: Optional[str] = None


@dataclass
class TextDocumentChangeRegistrationOptions(TextDocumentRegistrationOptions):
    sync_kind: TextDocumentSyncKind = TextDocumentSyncKind.FULL


@dataclass
class FoldingRangeOptions(WorkDoneProgressOptions):
    pass


@dataclass
class FoldingRangeRegistrationOptions(StaticRegistrationOptions, TextDocumentRegistrationOptions, FoldingRangeOptions):
    pass


@dataclass
class DefinitionOptions(WorkDoneProgressOptions):
    pass


@dataclass
class DeclarationOptions(WorkDoneProgressOptions):
    pass


@dataclass
class DeclarationRegistrationOptions(DeclarationOptions, TextDocumentRegistrationOptions, StaticRegistrationOptions):
    pass


@dataclass
class ImplementationOptions(WorkDoneProgressOptions):
    pass


@dataclass
class ImplementationRegistrationOptions(DeclarationOptions, TextDocumentRegistrationOptions, StaticRegistrationOptions):
    pass


@dataclass
class HoverOptions(WorkDoneProgressOptions):
    pass


@dataclass
class WorkspaceSymbolOptions(WorkDoneProgressOptions):
    pass


@dataclass
class DocumentSymbolOptions(WorkDoneProgressOptions):
    label: Optional[str] = None


@dataclass
class DocumentSymbolRegistrationOptions(TextDocumentRegistrationOptions, DocumentSymbolOptions):
    pass


@dataclass
class ServerCapabilitiesWorkspaceFileOperations(Model):
    did_create: Optional[FileOperationRegistrationOptions] = None
    will_create: Optional[FileOperationRegistrationOptions] = None
    did_rename: Optional[FileOperationRegistrationOptions] = None
    will_rename: Optional[FileOperationRegistrationOptions] = None
    did_delete: Optional[FileOperationRegistrationOptions] = None
    will_delete: Optional[FileOperationRegistrationOptions] = None


@dataclass
class ServerCapabilitiesWorkspace(Model):
    workspace_folders: Optional[WorkspaceFoldersServerCapabilities] = None
    file_operations: Optional[ServerCapabilitiesWorkspaceFileOperations] = None


@dataclass
class CompletionOptions(WorkDoneProgressOptions):
    trigger_characters: Optional[List[str]] = None
    all_commit_characters: Optional[List[str]] = None
    resolve_provider: Optional[bool] = None


@dataclass
class CompletionRegistrationOptions(TextDocumentRegistrationOptions, CompletionOptions):
    pass


@dataclass
class SignatureHelpOptions(WorkDoneProgressOptions):
    trigger_characters: Optional[List[str]] = None
    retrigger_characters: Optional[List[str]] = None


@dataclass
class CodeLensOptions(WorkDoneProgressOptions):
    resolve_provider: Optional[bool] = None


@dataclass
class DocumentFormattingOptions(WorkDoneProgressOptions):
    pass


@dataclass
class DocumentFormattingRegistrationOptions(TextDocumentRegistrationOptions, DocumentFormattingOptions):
    pass


@dataclass
class DocumentRangeFormattingOptions(WorkDoneProgressOptions):
    pass


@dataclass
class DocumentRangeFormattingRegistrationOptions(TextDocumentRegistrationOptions, DocumentRangeFormattingOptions):
    pass


@dataclass
class _ExecuteCommandOptions:
    commands: List[str]


@dataclass
class ExecuteCommandOptions(WorkDoneProgressOptions, _ExecuteCommandOptions):
    pass


@dataclass
class ExecuteCommandRegistrationOptions(ExecuteCommandOptions):
    pass


@dataclass
class _ExecuteCommandParams:
    command: str
    arguments: Optional[List[LSPAny]] = None


@dataclass
class ExecuteCommandParams(WorkDoneProgressParams, _ExecuteCommandParams):
    pass


@dataclass
class SemanticTokensLegend(Model):
    token_types: List[str]
    token_modifiers: List[str]


@dataclass
class SemanticTokensOptionsFull(Model):
    delta: Optional[bool] = None


@dataclass
class SemanticTokensOptionsRange(Model):
    pass


@dataclass
class _SemanticTokensOptions:
    legend: SemanticTokensLegend
    range: Union[bool, SemanticTokensOptionsRange, None] = None
    full: Union[bool, SemanticTokensOptionsFull, None] = None


@dataclass
class SemanticTokensOptions(WorkDoneProgressOptions, _SemanticTokensOptions):
    pass


@dataclass
class SemanticTokensRegistrationOptions(
    TextDocumentRegistrationOptions, StaticRegistrationOptions, SemanticTokensOptions
):
    pass


@dataclass
class ReferenceOptions(WorkDoneProgressOptions):
    pass


@dataclass
class ReferenceRegistrationOptions(TextDocumentRegistrationOptions, ReferenceOptions):
    pass


@dataclass
class DocumentHighlightOptions(WorkDoneProgressOptions):
    pass


@dataclass
class DocumentHighlightRegistrationOptions(TextDocumentRegistrationOptions, DocumentHighlightOptions):
    pass


@dataclass
class LinkedEditingRangeOptions(WorkDoneProgressOptions):
    pass


@dataclass
class LinkedEditingRangeRegistrationOptions(
    LinkedEditingRangeOptions, StaticRegistrationOptions, TextDocumentRegistrationOptions
):
    pass


@dataclass
class SelectionRangeOptions(WorkDoneProgressOptions):
    pass


@dataclass
class SelectionRangeRegistrationOptions(
    TextDocumentRegistrationOptions, SelectionRangeOptions, StaticRegistrationOptions
):
    pass


@dataclass
class RenameOptions(WorkDoneProgressOptions):
    prepare_provider: Optional[bool] = None


@dataclass
class RenameRegistrationOptions(RenameOptions, StaticRegistrationOptions, TextDocumentRegistrationOptions):
    pass


@dataclass
class InlineValueOptions(WorkDoneProgressOptions):
    pass


@dataclass
class InlineValueRegistrationOptions(TextDocumentRegistrationOptions, StaticRegistrationOptions, InlineValueOptions):
    pass


@dataclass
class _DiagnosticOptions:
    inter_file_dependencies: bool
    workspace_diagnostics: bool
    identifier: Optional[str] = None


@dataclass
class DiagnosticOptions(WorkDoneProgressOptions, _DiagnosticOptions):
    pass


@dataclass
class DiagnosticRegistrationOptions(TextDocumentRegistrationOptions, StaticRegistrationOptions, DiagnosticOptions):
    pass


@dataclass
class _CodeActionOptions:
    code_action_kinds: Optional[List[CodeActionKind]] = None
    resolve_provider: Optional[bool] = None


@dataclass
class CodeActionOptions(WorkDoneProgressOptions, _CodeActionOptions):
    pass


@dataclass
class _InlayHintOptions:
    resolve_provider: Optional[bool] = None


@dataclass
class InlayHintOptions(WorkDoneProgressOptions, _InlayHintOptions):
    pass


@dataclass
class InlayHintRegistrationOptions(InlayHintOptions, TextDocumentRegistrationOptions, StaticRegistrationOptions):
    pass


@dataclass
class ServerCapabilities(Model):
    position_encoding: Optional[PositionEncodingKind] = None
    text_document_sync: Union[TextDocumentSyncOptions, TextDocumentSyncKind, None] = None
    completion_provider: Optional[CompletionOptions] = None
    hover_provider: Union[bool, HoverOptions, None] = None
    signature_help_provider: Optional[SignatureHelpOptions] = None
    declaration_provider: Union[bool, DeclarationOptions, DeclarationRegistrationOptions, None] = None
    definition_provider: Union[bool, DefinitionOptions, None] = None
    implementation_provider: Union[bool, ImplementationOptions, ImplementationRegistrationOptions, None] = None
    references_provider: Union[bool, ReferenceOptions, None] = None
    document_highlight_provider: Union[bool, DocumentHighlightOptions, None] = None
    document_symbol_provider: Union[bool, DocumentSymbolOptions, None] = None
    code_action_provider: Union[bool, CodeActionOptions, None] = None
    code_lens_provider: Optional[CodeLensOptions] = None
    # TODO document_link_provider: Optional[DocumentLinkOptions] = None
    # TODO color_provider: Union[bool, DocumentColorOptions, DocumentColorRegistrationOptions, None] = None
    document_formatting_provider: Union[bool, DocumentFormattingOptions, None] = None
    document_range_formatting_provider: Union[bool, DocumentRangeFormattingOptions, None] = None
    # TODO document_on_type_formatting_provider: Optional[DocumentOnTypeFormattingOptions] = None
    rename_provider: Union[bool, RenameOptions, None] = None
    folding_range_provider: Union[bool, FoldingRangeOptions, FoldingRangeRegistrationOptions, None] = None
    execute_command_provider: Optional[ExecuteCommandOptions] = None
    selection_range_provider: Union[bool, SelectionRangeOptions, SelectionRangeRegistrationOptions, None] = None
    linked_editing_range_provider: Union[
        bool, LinkedEditingRangeOptions, LinkedEditingRangeRegistrationOptions, None
    ] = None
    # TODO call_hierarchy_provider: Union[boolean, CallHierarchyOptions, CallHierarchyRegistrationOptions, None] = None
    semantic_tokens_provider: Union[SemanticTokensOptions, SemanticTokensRegistrationOptions, None] = None
    # TODO moniker_provider: Union[bool, MonikerOptions, MonikerRegistrationOptions, None] = None

    # TODO typeHierarchyProvider?: boolean | TypeHierarchyOptions | TypeHierarchyRegistrationOptions;
    inline_value_provider: Union[bool, InlineValueOptions, InlineValueRegistrationOptions, None] = None
    inlay_hint_provider: Union[bool, InlayHintOptions, InlayHintRegistrationOptions, None] = None
    diagnostic_provider: Union[DiagnosticOptions, DiagnosticRegistrationOptions, None] = None

    workspace_symbol_provider: Union[bool, WorkspaceSymbolOptions, None] = None
    workspace: Optional[ServerCapabilitiesWorkspace] = None
    experimental: Optional[Any] = None


@dataclass
class InitializeResultServerInfo(Model):
    name: str
    version: Optional[str] = None


@dataclass
class InitializeResult(Model):
    capabilities: ServerCapabilities
    server_info: Optional[InitializeResultServerInfo] = None


@dataclass
class InitializedParams(Model):
    pass


@dataclass
class DidChangeConfigurationParams(Model):
    settings: Any


@dataclass
class Position(Model):
    line: int
    character: int

    def __ge__(self, other: "Position") -> bool:
        line_gt = self.line > other.line

        if line_gt:
            return True

        if self.line == other.line:
            return self.character >= other.character

        return False

    def __gt__(self, other: "Position") -> bool:
        line_gt = self.line > other.line

        if line_gt:
            return True

        if self.line == other.line:
            return self.character > other.character

        return False

    def __le__(self, other: "Position") -> bool:
        line_lt = self.line < other.line

        if line_lt:
            return True

        if self.line == other.line:
            return self.character <= other.character

        return False

    def __lt__(self, other: "Position") -> bool:
        line_lt = self.line < other.line

        if line_lt:
            return True

        if self.line == other.line:
            return self.character < other.character

        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __iter__(self) -> Iterator[int]:
        return iter((self.line, self.character))

    def is_in_range(self, range: "Range", include_end: bool = True) -> bool:
        if include_end:
            return range.start <= self <= range.end

        return range.start <= self < range.end

    def __hash__(self) -> int:
        return hash((self.line, self.character))


@dataclass
class Range(Model):
    start: Position
    end: Position

    def __iter__(self) -> Iterator[Position]:
        return iter((self.start, self.end))

    @staticmethod
    def zero() -> "Range":
        return Range(
            start=Position(
                line=0,
                character=0,
            ),
            end=Position(
                line=0,
                character=0,
            ),
        )

    @staticmethod
    def invalid() -> "Range":
        return Range(
            start=Position(
                line=-1,
                character=-1,
            ),
            end=Position(
                line=-1,
                character=-1,
            ),
        )

    def extend(self, start_line: int = 0, start_character: int = 0, end_line: int = 0, end_character: int = 0) -> Range:
        return Range(
            start=Position(line=self.start.line + start_line, character=self.start.character + start_character),
            end=Position(line=self.end.line + end_line, character=self.end.character + end_character),
        )

    def __contains__(self, x: object) -> bool:
        if isinstance(x, (Position, Range)):
            return x.is_in_range(self)
        return False

    def is_in_range(self, range: Range) -> bool:
        return self.start.is_in_range(range) and self.end.is_in_range(range)

    def __hash__(self) -> int:
        return hash((self.start, self.end))


@dataclass
class TextDocumentItem(Model):
    uri: DocumentUri
    language_id: str
    version: int
    text: str


@dataclass
class DidOpenTextDocumentParams(Model):
    text_document: TextDocumentItem


@dataclass
class TextDocumentIdentifier(Model):
    uri: DocumentUri


@dataclass
class OptionalVersionedTextDocumentIdentifier(TextDocumentIdentifier):
    version: Optional[int]


@dataclass
class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    version: int


@dataclass
class DidCloseTextDocumentParams(Model):
    text_document: TextDocumentIdentifier


@dataclass
class TextDocumentContentRangeChangeEvent(Model):
    range: Range
    text: str
    range_length: Optional[int] = None


@dataclass
class TextDocumentContentTextChangeEvent(Model):
    text: str


TextDocumentContentChangeEvent = Union[TextDocumentContentRangeChangeEvent, TextDocumentContentTextChangeEvent]


@dataclass
class DidChangeTextDocumentParams(Model):
    text_document: VersionedTextDocumentIdentifier
    content_changes: List[TextDocumentContentChangeEvent]


@dataclass
class ConfigurationItem(Model):
    scope_uri: Optional[DocumentUri]
    section: Optional[str]


@dataclass
class ConfigurationParams(Model):
    items: List[ConfigurationItem]


class MessageType(IntEnum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    LOG = 4

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class ShowMessageParams(Model):
    type: MessageType
    message: str


@dataclass
class LogMessageParams(Model):
    type: MessageType
    message: str


@dataclass
class MessageActionItem(Model):
    title: str


@dataclass
class ShowMessageRequestParams(ShowMessageParams):
    actions: Optional[List[MessageActionItem]] = None


@dataclass
class ShowDocumentParams(Model):
    uri: URI
    external: Optional[bool] = None
    take_focus: Optional[bool] = None
    selection: Optional[Range] = None


@dataclass
class ShowDocumentResult(Model):
    success: bool


class TextDocumentSaveReason(IntEnum):
    Manual = 1
    AfterDelay = 2
    FocusOut = 3

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class WillSaveTextDocumentParams(Model):
    text_document: TextDocumentIdentifier
    reason: TextDocumentSaveReason


@dataclass
class TextEdit(Model):
    range: Range
    new_text: str


@dataclass
class DidSaveTextDocumentParams(Model):
    text_document: TextDocumentIdentifier
    text: Optional[str] = None


class DiagnosticSeverity(Enum):
    ERROR = 1
    WARNING = 2
    INFORMATION = 3
    HINT = 4

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class CodeDescription(Model):
    href: URI


@dataclass
class Location(Model):
    uri: DocumentUri
    range: Range

    def __hash__(self) -> int:
        return hash((self.uri, self.range))


@dataclass
class LocationLink(Model):
    origin_selection_range: Optional[Range]
    target_uri: DocumentUri
    target_range: Range
    target_selection_range: Range


@dataclass
class DiagnosticRelatedInformation(Model):
    location: Location
    message: str


@dataclass
class Diagnostic(Model):
    range: Range
    message: str
    severity: Optional[DiagnosticSeverity] = None
    code: Union[int, str, None] = None
    code_description: Optional[CodeDescription] = None
    source: Optional[str] = None
    tags: Optional[List[DiagnosticTag]] = None
    related_information: Optional[List[DiagnosticRelatedInformation]] = None
    data: Optional[Any] = None


@dataclass
class PublishDiagnosticsParams(Model):
    uri: DocumentUri
    diagnostics: List[Diagnostic]
    version: Optional[int] = None


@dataclass
class SetTraceParams(Model):
    value: TraceValue


@dataclass
class _FoldingRangeParams:
    text_document: TextDocumentIdentifier


@dataclass
class FoldingRangeParams(WorkDoneProgressParams, _FoldingRangeParams):
    pass


@dataclass
class FoldingRange(Model):
    start_line: int
    end_line: int
    start_character: Optional[int] = None
    end_character: Optional[int] = None
    kind: Union[FoldingRangeKind, str, None] = None
    collapsed_text: Optional[str] = None


@dataclass
class FileCreate(Model):
    uri: str


@dataclass
class CreateFilesParams(Model):
    files: List[FileCreate]


@dataclass
class FileRename(Model):
    old_uri: str
    new_uri: str


@dataclass
class RenameFilesParams(Model):
    files: List[FileRename]


@dataclass
class FileDelete(Model):
    uri: str


@dataclass
class DeleteFilesParams(Model):
    files: List[FileDelete]


ChangeAnnotationIdentifier = str


@dataclass
class CreateFileOptions(Model):
    overwrite: Optional[bool] = None
    ignore_if_exists: Optional[bool] = None


@dataclass
class CreateFile(Model):
    kind: Literal["create"]
    uri: DocumentUri
    options: Optional[CreateFileOptions]
    annotation_id: ChangeAnnotationIdentifier


@dataclass
class RenameFileOptions(Model):
    overwrite: Optional[bool] = None
    ignore_if_exists: Optional[bool] = None


@dataclass
class RenameFile(Model):
    kind: Literal["rename"]
    old_uri: DocumentUri
    new_uri: DocumentUri
    options: Optional[RenameFileOptions]
    annotation_id: ChangeAnnotationIdentifier


@dataclass
class DeleteFileOptions(Model):
    recursive: Optional[bool] = None
    ignore_if_exists: Optional[bool] = None


@dataclass
class DeleteFile(Model):
    kind: Literal["delete"]
    uri: DocumentUri
    options: Optional[DeleteFileOptions]
    annotation_id: ChangeAnnotationIdentifier


@dataclass
class AnnotatedTextEdit(TextEdit):
    annotation_id: ChangeAnnotationIdentifier


@dataclass
class TextDocumentEdit(Model):
    text_document: OptionalVersionedTextDocumentIdentifier
    edits: List[Union[TextEdit, AnnotatedTextEdit]]


@dataclass
class ChangeAnnotation(Model):
    label: str
    needs_confirmation: Optional[bool] = None
    description: Optional[str] = None


@dataclass
class WorkspaceEdit(Model):
    changes: Optional[Dict[DocumentUri, List[TextEdit]]] = None
    document_changes: Optional[List[Union[TextDocumentEdit, CreateFile, RenameFile, DeleteFile]]] = None
    change_annotations: Optional[Dict[ChangeAnnotationIdentifier, ChangeAnnotation]] = None


@dataclass
class PartialResultParams(Model):
    partial_result_token: Optional[ProgressToken] = None


@dataclass
class TextDocumentPositionParams(Model):
    text_document: TextDocumentIdentifier
    position: Position


@dataclass
class DefinitionParams(WorkDoneProgressParams, PartialResultParams, TextDocumentPositionParams):
    pass


@dataclass
class DeclarationParams(WorkDoneProgressParams, PartialResultParams, TextDocumentPositionParams):
    pass


@dataclass
class ImplementationParams(WorkDoneProgressParams, PartialResultParams, TextDocumentPositionParams):
    pass


@dataclass
class HoverParams(WorkDoneProgressParams, TextDocumentPositionParams):
    pass


@dataclass
class MarkedStringType(Model):
    language: str
    value: str


MarkedString = Union[str, MarkedStringType]


@dataclass
class MarkupContent(Model):
    kind: MarkupKind
    value: str


@dataclass
class Hover(Model):
    contents: Union[MarkedString, List[MarkedString], MarkupContent]
    range: Optional[Range] = None


@dataclass
class WorkspaceFoldersChangeEvent(Model):
    added: List[WorkspaceFolder]
    removed: List[WorkspaceFolder]


@dataclass
class DidChangeWorkspaceFoldersParams(Model):
    event: WorkspaceFoldersChangeEvent


@dataclass
class Registration(Model):
    id: str
    method: str
    register_options: Optional[Any]


@dataclass
class RegistrationParams(Model):
    registrations: List[Registration]


@dataclass
class Unregistration(Model):
    id: str
    method: str


@dataclass
class UnregistrationParams(Model):
    unregisterations: List[Unregistration]


class WatchKind(IntFlag):
    CREATE = 1
    CHANGE = 2
    DELETE = 4


@dataclass
class FileSystemWatcher(Model):
    glob_pattern: str
    kind: Optional[WatchKind]


@dataclass
class DidChangeWatchedFilesRegistrationOptions(Model):
    watchers: List[FileSystemWatcher]


class FileChangeType(IntEnum):
    CREATED = 1
    CHANGED = 2
    DELETED = 3

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class FileEvent(Model):
    uri: DocumentUri
    type: FileChangeType


@dataclass
class DidChangeWatchedFilesParams(Model):
    changes: List[FileEvent]


@dataclass
class Command(Model):
    title: str
    command: str
    arguments: Optional[List[Any]] = None


class CompletionTriggerKind(Enum):
    INVOKED = 1
    TRIGGERCHARACTER = 2
    TRIGGERFORINCOMPLETECOMPLETIONS = 3

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class CompletionContext(Model):
    trigger_kind: CompletionTriggerKind
    trigger_character: Optional[str] = None


@dataclass
class CompletionParams(WorkDoneProgressParams, PartialResultParams, TextDocumentPositionParams):
    context: Optional[CompletionContext] = None


@dataclass
class InsertReplaceEdit(Model):
    new_text: str
    insert: Range
    replace: Range


@dataclass
class CompletionItem(Model):
    label: str
    kind: Optional[CompletionItemKind] = None
    tags: Optional[List[CompletionItemTag]] = None
    detail: Optional[str] = None
    documentation: Union[str, MarkupContent, None] = None
    deprecated: Optional[bool] = None
    preselect: Optional[bool] = None
    sort_text: Optional[str] = None
    filter_text: Optional[str] = None
    insert_text: Optional[str] = None
    insert_text_format: Optional[InsertTextFormat] = None
    insert_text_mode: Optional[InsertTextMode] = None
    text_edit: Union[TextEdit, InsertReplaceEdit, None] = None
    additional_text_edits: Optional[List[TextEdit]] = None
    commit_characters: Optional[List[str]] = None
    command: Optional[Command] = None
    data: Optional[Any] = None


@dataclass
class CompletionList(Model):
    is_incomplete: bool
    items: List[CompletionItem]


class SignatureHelpTriggerKind(Enum):
    INVOKED = 1
    TRIGGERCHARACTER = 2
    CONTENTCHANGE = 3

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class ParameterInformation(Model):
    label: Union[str, Tuple[int, int]]
    documentation: Union[str, MarkupContent, None] = None


@dataclass
class SignatureInformation(Model):
    label: str
    documentation: Union[str, MarkupContent, None] = None
    parameters: Optional[List[ParameterInformation]] = None
    active_parameter: Optional[int] = None


@dataclass
class SignatureHelp(Model):
    signatures: List[SignatureInformation]
    active_signature: Optional[int] = None
    active_parameter: Optional[int] = None


@dataclass
class SignatureHelpContext(Model):
    trigger_kind: SignatureHelpTriggerKind
    trigger_character: Optional[str] = None
    is_retrigger: bool = False
    active_signature_help: Optional[SignatureHelp] = None


@dataclass
class SignatureHelpParams(WorkDoneProgressParams, TextDocumentPositionParams):
    context: Optional[SignatureHelpContext] = None


@dataclass
class _CodeLensParams:
    text_document: TextDocumentIdentifier


@dataclass
class CodeLensParams(WorkDoneProgressParams, PartialResultParams, _CodeLensParams):
    pass


@dataclass
class CodeLens(Model):
    range: Range
    command: Optional[Command] = None
    data: Optional[Any] = None


@dataclass
class CodeLensRegistrationOptions(TextDocumentRegistrationOptions, CodeLensOptions):
    pass


@dataclass
class _DocumentSymbolParams:
    text_document: TextDocumentIdentifier


@dataclass
class DocumentSymbolParams(WorkDoneProgressParams, PartialResultParams, _DocumentSymbolParams):
    pass


@dataclass
class DocumentSymbol(Model):
    name: str
    kind: SymbolKind
    range: Range
    selection_range: Range
    detail: Optional[str] = None
    tags: Optional[List[SymbolTag]] = None
    deprecated: Optional[bool] = None
    children: Optional[List[DocumentSymbol]] = None


@dataclass
class SymbolInformation(Model):
    name: str
    kind: SymbolKind
    location: Location
    tags: Optional[List[SymbolTag]] = None
    deprecated: Optional[bool] = None
    container_name: Optional[str] = None


@dataclass
class FormattingOptions(Model):
    tab_size: int
    insert_spaces: bool
    trim_trailing_whitespace: Optional[bool] = None
    insert_final_newline: Optional[bool] = None
    trim_final_newlines: Optional[bool] = None


@dataclass
class _DocumentFormattingParams:
    text_document: TextDocumentIdentifier
    options: FormattingOptions


@dataclass
class DocumentFormattingParams(WorkDoneProgressParams, _DocumentFormattingParams):
    pass


@dataclass
class _DocumentRangeFormattingParams:
    text_document: TextDocumentIdentifier
    range: Range
    options: FormattingOptions


@dataclass
class DocumentRangeFormattingParams(WorkDoneProgressParams, _DocumentRangeFormattingParams):
    pass


@dataclass
class _SemanticTokensParams:
    text_document: TextDocumentIdentifier


@dataclass
class SemanticTokensParams(WorkDoneProgressParams, PartialResultParams, _SemanticTokensParams):
    pass


@dataclass
class SemanticTokens(Model):
    data: List[int]
    result_id: Optional[str] = None


@dataclass
class SemanticTokensPartialResult(Model):
    data: List[int]


@dataclass
class _SemanticTokensDeltaParams:
    text_document: TextDocumentIdentifier
    previous_result_id: str


@dataclass
class SemanticTokensDeltaParams(WorkDoneProgressParams, PartialResultParams, _SemanticTokensDeltaParams):
    pass


@dataclass
class SemanticTokensEdit(Model):
    start: int
    delete_count: int
    data: Optional[List[int]] = None


@dataclass
class SemanticTokensDelta(Model):
    edits: List[SemanticTokensEdit]
    result_id: Optional[str] = None


@dataclass
class SemanticTokensDeltaPartialResult(Model):
    edits: List[SemanticTokensEdit]


@dataclass
class _SemanticTokensRangeParams:
    text_document: TextDocumentIdentifier
    range: Range


@dataclass
class SemanticTokensRangeParams(WorkDoneProgressParams, PartialResultParams, _SemanticTokensRangeParams):
    pass


class SemanticTokenTypes(Enum):
    NAMESPACE = "namespace"
    TYPE = "type"
    CLASS = "class"
    ENUM = "enum"
    INTERFACE = "interface"
    STRUCT = "struct"
    TYPE_PARAMETER = "typeParameter"
    PARAMETER = "parameter"
    VARIABLE = "variable"
    PROPERTY = "property"
    ENUM_MEMBER = "enumMember"
    EVENT = "event"
    FUNCTION = "function"
    METHOD = "method"
    MACRO = "macro"
    KEYWORD = "keyword"
    MODIFIER = "modifier"
    COMMENT = "comment"
    STRING = "string"
    NUMBER = "number"
    REGEXP = "regexp"
    OPERATOR = "operator"
    DECORATOR = "decorator"

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


class SemanticTokenModifiers(Enum):
    DECLARATION = "declaration"
    DEFINITION = "definition"
    READONLY = "readonly"
    STATIC = "static"
    DEPRECATED = "deprecated"
    ABSTRACT = "abstract"
    ASYNC = "async"
    MODIFICATION = "modification"
    DOCUMENTATION = "documentation"
    DEFAULT_LIBRARY = "defaultLibrary"

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class ReferenceContext(Model):
    include_declaration: bool


@dataclass
class _ReferenceParams:
    context: ReferenceContext


@dataclass
class ReferenceParams(WorkDoneProgressParams, PartialResultParams, TextDocumentPositionParams, _ReferenceParams):
    pass


@dataclass
class _DocumentHighlightParams:
    pass


@dataclass
class DocumentHighlightParams(
    WorkDoneProgressParams, PartialResultParams, TextDocumentPositionParams, _DocumentHighlightParams
):
    pass


class DocumentHighlightKind(Enum):
    TEXT = 1
    READ = 2
    WRITE = 3


@dataclass
class DocumentHighlight(Model):
    range: Range
    kind: Optional[DocumentHighlightKind] = None


@dataclass
class LinkedEditingRangeParams(WorkDoneProgressParams, TextDocumentPositionParams):
    pass


@dataclass
class LinkedEditingRanges(Model):
    ranges: List[Range]
    word_pattern: Optional[str] = None


@dataclass
class _SelectionRangeParams:
    text_document: TextDocumentIdentifier
    positions: List[Position]


@dataclass
class SelectionRangeParams(WorkDoneProgressParams, PartialResultParams, _SelectionRangeParams):
    pass


@dataclass
class SelectionRange(Model):
    range: Range
    parent: Optional[SelectionRange] = None


@dataclass
class ProgressParams(Model):
    token: ProgressToken
    value: Any


@dataclass
class WorkDoneProgressCreateParams(Model):
    token: ProgressToken


@dataclass
class WorkDoneProgressCancelParams(Model):
    token: ProgressToken


@dataclass
class WorkDoneProgressBase(Model):
    kind: Literal["begin", "end", "report"]


@dataclass
class _WorkDoneProgressCommon:
    title: str
    message: Optional[str] = None
    percentage: Optional[int] = None
    cancellable: Optional[bool] = None


@dataclass
class WorkDoneProgressBegin(WorkDoneProgressBase, _WorkDoneProgressCommon):
    kind: Literal["begin"] = "begin"


@dataclass
class WorkDoneProgressReport(WorkDoneProgressBase, _WorkDoneProgressCommon):
    kind: Literal["report"] = "report"


@dataclass
class _WorkDoneProgressEnd:
    message: Optional[str] = None


@dataclass
class WorkDoneProgressEnd(WorkDoneProgressBase, _WorkDoneProgressEnd):
    kind: Literal["end"] = "end"


@dataclass
class _RenameParams:
    new_name: str


@dataclass
class RenameParams(WorkDoneProgressParams, TextDocumentPositionParams, _RenameParams):
    pass


@dataclass
class PrepareRenameParams(TextDocumentPositionParams):
    pass


@dataclass
class PrepareRenameResultWithPlaceHolder(Model):
    range: Range
    placeholder: str


@dataclass
class PrepareRenameResultWithDefaultBehavior(Model):
    default_behavior: bool


PrepareRenameResult = Union[Range, PrepareRenameResultWithPlaceHolder, PrepareRenameResultWithDefaultBehavior]


@dataclass
class InlineValueContext(Model):
    frame_id: int
    stopped_location: Range


@dataclass
class _InlineValueParams:
    text_document: TextDocumentIdentifier
    range: Range
    context: InlineValueContext


@dataclass
class InlineValueParams(WorkDoneProgressParams, _InlineValueParams):
    pass


@dataclass
class InlineValueText(Model):
    range: Range
    text: str


@dataclass
class InlineValueVariableLookup(Model):
    range: Range
    variable_name: Optional[str]
    case_sensitive_lookup: bool


@dataclass
class InlineValueEvaluatableExpression(Model):
    range: Range
    expression: Optional[str]


InlineValue = Union[InlineValueText, InlineValueVariableLookup, InlineValueEvaluatableExpression]


@dataclass
class _DocumentDiagnosticParams:
    text_document: TextDocumentIdentifier
    identifier: Optional[str] = None
    previous_result_id: Optional[str] = None


@dataclass
class DocumentDiagnosticParams(WorkDoneProgressParams, PartialResultParams, _DocumentDiagnosticParams):
    pass


class DocumentDiagnosticReportKind(Enum):
    FULL = "full"
    UNCHANGED = "unchanged"


@dataclass
class FullDocumentDiagnosticReport(Model):
    items: List[Diagnostic]
    result_id: Optional[str] = None
    kind: Literal[DocumentDiagnosticReportKind.FULL] = DocumentDiagnosticReportKind.FULL


@dataclass
class UnchangedDocumentDiagnosticReport(Model):
    result_id: str
    kind: DocumentDiagnosticReportKind = DocumentDiagnosticReportKind.UNCHANGED


@dataclass
class RelatedFullDocumentDiagnosticReport(FullDocumentDiagnosticReport):
    related_documents: Optional[
        Dict[DocumentUri, Union[FullDocumentDiagnosticReport, UnchangedDocumentDiagnosticReport]]
    ] = None


@dataclass
class RelatedUnchangedDocumentDiagnosticReport(UnchangedDocumentDiagnosticReport):
    related_documents: Optional[
        Dict[DocumentUri, Union[FullDocumentDiagnosticReport, UnchangedDocumentDiagnosticReport]]
    ] = None


DocumentDiagnosticReport = Union[RelatedFullDocumentDiagnosticReport, RelatedUnchangedDocumentDiagnosticReport]


@dataclass
class DocumentDiagnosticReportPartialResult(Model):
    related_documents: Optional[
        Dict[DocumentUri, Union[FullDocumentDiagnosticReport, UnchangedDocumentDiagnosticReport]]
    ] = None


@dataclass
class DiagnosticServerCancellationData(Model):
    retrigger_request: bool


@dataclass
class PreviousResultId(Model):
    uri: DocumentUri
    value: str


@dataclass
class _WorkspaceDiagnosticParams:
    previous_result_ids: List[PreviousResultId]
    identifier: Optional[str] = None


@dataclass
class WorkspaceDiagnosticParams(WorkDoneProgressParams, PartialResultParams, _WorkspaceDiagnosticParams):
    pass


@dataclass
class _WorkspaceFullDocumentDiagnosticReport:
    uri: DocumentUri
    version: Optional[int]


@dataclass
class WorkspaceFullDocumentDiagnosticReport(FullDocumentDiagnosticReport, _WorkspaceFullDocumentDiagnosticReport):
    pass


@dataclass
class _WorkspaceUnchangedDocumentDiagnosticReport:
    uri: DocumentUri
    version: Optional[int]


@dataclass
class WorkspaceUnchangedDocumentDiagnosticReport(
    UnchangedDocumentDiagnosticReport, _WorkspaceUnchangedDocumentDiagnosticReport
):
    pass


WorkspaceDocumentDiagnosticReport = Union[
    WorkspaceFullDocumentDiagnosticReport, WorkspaceUnchangedDocumentDiagnosticReport
]


@dataclass
class WorkspaceDiagnosticReportPartialResult(Model):
    items: List[WorkspaceDocumentDiagnosticReport]


@dataclass
class WorkspaceDiagnosticReport(Model):
    items: List[WorkspaceDocumentDiagnosticReport]


@dataclass
class _CodeActionParams:
    text_document: TextDocumentIdentifier
    range: Range
    context: CodeActionContext


@dataclass
class CodeActionParams(WorkDoneProgressParams, PartialResultParams, _CodeActionParams):
    pass


class CodeActionTriggerKind(IntEnum):
    INVOKED = 1
    AUTOMATIC = 2


@dataclass
class CodeActionContext(Model):
    diagnostics: List[Diagnostic]
    only: Optional[List[CodeActionKind]] = None
    trigger_kind: Optional[CodeActionTriggerKind] = None


@dataclass
class CodeActionDisabled:
    reason: str


@dataclass
class CodeAction:
    title: str
    kind: Optional[CodeActionKind] = None
    diagnostics: Optional[List[Diagnostic]] = None
    is_preferred: Optional[bool] = None
    disabled: Optional[CodeActionDisabled] = None
    edit: Optional[WorkspaceEdit] = None
    command: Optional[Command] = None
    data: Any = None


@dataclass
class ApplyWorkspaceEditParams(Model):
    edit: WorkspaceEdit
    label: Optional[str] = None


@dataclass
class ApplyWorkspaceEditResult(Model):
    applied: bool
    failure_reason: Optional[str] = None
    failed_change: Optional[int] = None


@dataclass
class _InlayHintParams:
    text_document: TextDocumentIdentifier
    range: Range


@dataclass
class InlayHintParams(WorkDoneProgressParams, _InlayHintParams):
    pass


@dataclass
class InlayHintLabelPart(Model):
    value: str
    tooltip: Union[str, MarkupContent]
    location: Optional[Location] = None
    command: Optional[Command] = None


class InlayHintKind(IntEnum):
    TYPE = 1
    PARAMETER = 2

    def __repr__(self) -> str:  # pragma: no cover
        return super().__str__()


@dataclass
class InlayHint(Model):
    position: Position
    label: Union[str, List[InlayHintLabelPart]]
    kind: Optional[InlayHintKind] = None
    text_edits: Optional[List[TextEdit]] = None
    tooltip: Union[str, MarkupContent, None] = None
    padding_left: Optional[bool] = None
    padding_right: Optional[bool] = None
    data: LSPAny = None
