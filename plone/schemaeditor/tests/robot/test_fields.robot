*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers

*** Variables ***

*** Keywords ***

Wait overlay is closed
   Wait until keyword succeeds  60  1  Page should not contain element  css=div.overlay

Overlay is opened
   Wait Until Page Contains Element  css=.overlay
   
*** Test cases ***

Add field
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
    Select from list  form-widgets-vocabularyName  plone.app.vocabularies.AvailableContentLanguages
    Click Button  Save
	Wait overlay is closed
    Page should contain  French

    Click Overlay Button  Add new field…
    Input text  form-widgets-title  Hobbies
    Focus  form-widgets-__name__
    Textfield Value Should Be  form-widgets-__name__  hobbies
    Input Text  form-widgets-description  Check what you are fond of
    Select From List  form-widgets-factory  Multiple Choice
    Click Button  Add
    Wait until page contains element  css=#fieldset-0 #form-widgets-hobbies

    Click Overlay Link  ${PLONE_URL}/dexterity-types/curriculum_vitae/hobbies
    Input text  form-widgets-values  Chess\nSoccer\nBaseball\nVideo games
    Select from list  form-widgets-vocabularyName  Multiple Choice  plone.app.vocabularies.AvailableContentLanguages
    Click Button  Save
    Wait until page contains element  css=#formfield-form-widgets-vocabularyName.error
    Select from list  form-widgets-vocabularyName  No value
    Click Button  Save

    Wait until page contains element  form-widgets-hobbies-3

Add a fieldSet
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
    Wait overlay is closed

    comment  PAUSE
