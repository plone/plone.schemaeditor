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
    Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-id  curriculum_vitae
    Click button  form-buttons-add
    Wait until page contains  Fields

    Click Overlay Button  Add new field…
    Input text for sure  form-widgets-title  Languages
    Input text for sure  form-widgets-description  Spoken languages
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
    Select from list  form-widgets-vocabularyName  plone.app.vocabularies.AvailableContentLanguages
    Click Button  Save
    Wait until page contains element  css=#formfield-form-widgets-vocabularyName.error
    Select from list  form-widgets-vocabularyName  No value
    Click Button  Save
    Wait until page contains element  form-widgets-hobbies-3


Add accented field
    Log in as site owner
    Add a content type  Person
    Click Overlay Button  Add new field…
    Input text  form-widgets-title  Prénom
    Focus  form-widgets-__name__
    Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-__name__  prenom


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

    #Mouse Down  xpath=//*[@data-field_id="address"][1]
    #Mouse Over  css=.formTab[data-fieldset_drag_id="1"]
    #Mouse Up  xpath=//*[@data-fieldset_drag_id="1"][1]
    #Wait Until Keyword Succeeds  10  1  Element should not be visible  css=.fieldPreview[data-field_id="address"]
    
    #Click Element  css=.formTab[data-fieldset_drag_id="1"]
    #Wait Until Keyword Succeeds  10  1  Element should be visible  css=.fieldPreview[data-field_id="address"]


Delete field
    Log in as site owner
    Add a content type  Somebody
    Add a field  Phone  Text line (String)
    Wait until page contains element  css=#fieldset-0 #formfield-form-widgets-phone
    Click link  css=div.fieldControls .schemaeditor-delete-field
    Confirm Action
    Page Should Not Contain Element  css=#formfield-form-widgets-phone


#~ Reorder field
    #~ Log in as site owner
    #~ Add a content type  
    #~ Add a field  Lastname  Text line (String)
    #~ Wait until page contains element  css=#fieldset-0 #formfield-form-widgets-lastname
    #~ Add a field  Firstname  Text line (String)
    #~ Wait until page contains element  css=#fieldset-0 #formfield-form-widgets-firstname
    
    #~ /html/body/div/div[2]/div/div[2]/div[2]/div/div/form/fieldset/div[3]/div/span
    #~ Mouse Down  xpath=//div[@data-field_id='phone']/div/span[@class='draghandle']
    #~ Mouse Over    xpath=//div[@data-field_id='firstname']
    #~ Mouse Out   xpath=//div[@data-field_id='phone']/div/span[@class='draghandle']

