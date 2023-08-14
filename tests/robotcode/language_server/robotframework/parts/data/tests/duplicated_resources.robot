*** Settings ***

Resource          ../resources/folder_a/duplicated.resource
Resource          ../resources/folder_b/duplicated.resource
Resource          folder_b/duplicated.resource

Library   alibrary.py
Library    alibrary

Variables    myvariables
Variables   myvariables.py

*** Test Cases ***
first
    a resource keyword A
    a resource keyword B
    duplicated keyword
    duplicated.a resource keyword A
    duplicated.a resource keyword B
    duplicated.duplicated keyword
