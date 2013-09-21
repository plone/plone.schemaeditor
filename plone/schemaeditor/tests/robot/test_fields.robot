*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers

*** Variables ***

*** Keywords ***

*** Test cases ***

Add a field
    [Documentation]  Log in as site owner
    Log in as site owner

    Go to  ${PLONE_URL}/@@dexterity-types
    Click Overlay Button  Add New Content Type…
    Input text  form-widgets-title  Curriculum vitae
    Focus  form-widgets-id
    Textfield Value Should Be  form-widgets-id  curriculum_vitae
    Click button  form-buttons-add
    Wait until page contains  Fields

    Click Overlay Button  Add new field…
    Input text  form-widgets-title  Languages
    Input text  form-widgets-description  Spoken languages
    Select from list  form-widgets-factory  Multiple Choice
    Click button  form-buttons-add
    Wait until page contains element  css=#fieldset-0 #form-widgets-languages

    Click Overlay Link  ${PLONE_URL}/dexterity-types/curriculum_vitae/languages
    Select from list  form-widgets-vocabularyName  Multiple Choice  plone.app.vocabularies.AvailableContentLanguages
    Click Button  Save
    Wait until page contains  French
