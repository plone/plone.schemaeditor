*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers

*** Variables ***

*** Keywords ***

Wait overlay is closed
   Wait until keyword succeeds  60  1  Page should not contain element  css=div.overlay


Add a content type
    [Arguments]    ${title}
    [Documentation]    Add a dexterity content type

    Go to  ${PLONE_URL}/@@dexterity-types
    Click Overlay Button  Add New Content Type…
    Input text  form-widgets-title  ${title}
    Focus  form-widgets-id
    Click button  form-buttons-add
    Wait until page contains  Fields


Add a field
    [Arguments]    ${field_title}    ${field_type}
    [Documentation]    Add a field in current dexterity content type

    Click Overlay Button  Add new field…
    Input text  form-widgets-title  ${field_title}
    Focus  form-widgets-__name__
    Select from list  form-widgets-factory  ${field_type}
    Click button  form-buttons-add
    Wait overlay is closed


*** Test cases ***

Add fields

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
    Focus  form-widgets-__name__
    Textfield Value Should Be  form-widgets-__name__  languages
    Select from list  form-widgets-factory  Multiple Choice
    Click button  form-buttons-add
    Wait until page contains element  css=#fieldset-0 #form-widgets-languages

    Click Overlay Link  ${PLONE_URL}/dexterity-types/curriculum_vitae/languages
    Select from list  form-widgets-vocabularyName  plone.app.vocabularies.AvailableContentLanguages
    Click Button  Save
	Wait overlay is closed
    Page should contain  French

	Add a field  Hobbies  Multiple Choice
    Click Overlay Link  ${PLONE_URL}/dexterity-types/curriculum_vitae/hobbies
    Input text  form-widgets-values  Chess\nSoccer\nBaseball\nVideo games
    Select from list  form-widgets-vocabularyName  Multiple Choice  plone.app.vocabularies.AvailableContentLanguages
    Click Button  Save
    Wait until page contains element  css=#formfield-form-widgets-vocabularyName.error
    Select from list  form-widgets-vocabularyName  No value
    Click Button  Save

    Wait until page contains element  form-widgets-hobbies-3


Add a fieldSet and move a field into this fieldset

    Log in as site owner

	Add a content type  Contact info

	Add a field  Address  Text

    Click Overlay Button  Add new fieldset…
    Input Text  form-widgets-label  Personal information
    Focus  form-widgets-__name__
    Textfield Value Should Be  form-widgets-__name__  personal_information
    Click Button  form-buttons-add
    Wait overlay is closed
	Wait until page contains  Personal information

	Set Selenium Speed  1 seconds

	Drag And Drop  xpath=//*[@data-field_id="address"]  xpath=//*[@data-fieldset_drag_id="1"]

	Click Element  css=.formTab[data-fieldset_drag_id="1"]
	Wait Until Keyword Succeeds  60  1  Element should be visible  css=.fieldPreview[data-field_id="address"]

	Comment  PAUSE