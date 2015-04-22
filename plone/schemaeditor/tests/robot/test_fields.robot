*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Variables ***

*** Test Cases ***

Add a content type

    Go to dexterity types configuration
    Click Overlay Button  Add New Content Type…
    Input text for sure  form-widgets-title  New style Article
    Focus  form-widgets-id
    Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-id  new_style_article
    Click button  css=.plone-modal-footer #form-buttons-add
    Wait until page contains  New style Article


Add a choice field with a named vocabulary

    Go to dexterity types configuration
    Add content type  Curriculum vitae  curriculum_vitae
    Click Overlay Button  Add new field…
    Input text for sure  form-widgets-title  Languages
    Focus  form-widgets-__name__
    Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-__name__  languages
    Input text for sure  form-widgets-description  Spoken languages
    Select from list  form-widgets-factory  Multiple Choice
    Click button  css=.plone-modal-footer #form-buttons-add
    Wait until page contains element  css=div[data-field_id="languages"] a.fieldSettings

    Open field settings  languages
    Select from list  form-widgets-vocabularyName  plone.app.vocabularies.AvailableContentLanguages
    Click button  css=.plone-modal-footer #form-buttons-save
    Wait overlay is closed
    Page should contain  Français


Add a choice field with vocabulary values

    Go to dexterity types configuration
    Add content type  My page  my_page
    Add field  Hobbies  hobbies  Multiple Choice
    Open field settings  hobbies
    Input text  form-widgets-values  Chess\nSoccer\nBaseball\nVideo games
    Click button  css=.plone-modal-footer #form-buttons-save
    Wait until page contains element  form-widgets-hobbies-3

#fail on jenkins
#We get an error if we try to select vocabulary name and vocabulary values

#    Go to dexterity types configuration
#    Add content type  My other page  my_other_page
#    Add field  Hobbies  hobbies  Multiple Choice
#    Open field settings  hobbies
#    Input text  form-widgets-values  Chess\nSoccer\nBaseball\nVideo games
#    Select from list  form-widgets-vocabularyName  plone.app.vocabularies.AvailableContentLanguages
#    Click Button  Save
#    Wait until page contains element  css=#formfield-form-widgets-vocabularyName.error
#

Add accented field

    Go to dexterity types configuration
    Add content type  Person  person
    Click Overlay Button  Add new field…
    Input text for sure  form-widgets-title  Prénom
    Focus  form-widgets-__name__
    Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-__name__  prenom


Add a fieldSet and move a field into this fieldset

    Go to dexterity types configuration
    Add content type  Contact info  contact_info
    Add field  Address  address  Text
    Click Overlay Button  Add new fieldset…
    Input text for sure  form-widgets-label  Personal information
    Focus  form-widgets-__name__
    Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-__name__  personal_information
    Click button  css=.plone-modal-footer #form-buttons-add
    Wait overlay is closed
    Wait until page contains  Personal information

    #Mouse Down  xpath=//*[@data-field_id="address"][1]
    #Mouse Over  css=.formTab[data-fieldset_drag_id="1"]
    #Mouse Up  xpath=//*[@data-fieldset_drag_id="1"][1]
    #Wait Until Keyword Succeeds  10  1  Element should not be visible  css=.fieldPreview[data-field_id="address"]

    #Click Element  css=.formTab[data-fieldset_drag_id="1"]
    #Wait Until Keyword Succeeds  10  1  Element should be visible  css=.fieldPreview[data-field_id="address"]


Delete field
    Go to dexterity types configuration
    Add content type  Somebody  somebody
    Add field  Phone  phone  Text line (String)
    Wait until page contains element  css=#fieldset-0 #formfield-form-widgets-phone
    Click link  css=div.fieldControls .schemaeditor-delete-field
    Confirm Action
    Wait Until Keyword Succeeds  10  1  Page Should Not Contain Element  css=#formfield-form-widgets-phone
    # Make sure it actually got deleted
    Go to  ${PLONE_URL}/@@dexterity-types/somebody/@@fields
    Wait Until Keyword Succeeds  10  1  Page Should Not Contain Element  css=#formfield-form-widgets-phone


#~ Reorder field
    #~ Log in as site owner
    #~ Add content type
    #~ Add field  Lastname  lastname  Text line (String)
    #~ Wait until page contains element  css=#fieldset-0 #formfield-form-widgets-lastname
    #~ Add field  Firstname  firstname  Text line (String)
    #~ Wait until page contains element  css=#fieldset-0 #formfield-form-widgets-firstname

    #~ /html/body/div/div[2]/div/div[2]/div[2]/div/div/form/fieldset/div[3]/div/span
    #~ Mouse Down  xpath=//div[@data-field_id='phone']/div/span[@class='draghandle']
    #~ Mouse Over    xpath=//div[@data-field_id='firstname']
    #~ Mouse Out   xpath=//div[@data-field_id='phone']/div/span[@class='draghandle']


*** Keywords ***

Wait overlay is closed
    Wait until keyword succeeds  60  1  Page should not contain element  css=div.overlay

Go to dexterity types configuration
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@dexterity-types

Add content type
    [Arguments]    ${title}    ${id}
    [Documentation]    Add a dexterity content type

    Click Overlay Button  Add New Content Type…
    Input text for sure  form-widgets-title  ${title}
    Focus  form-widgets-id
    Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-id  ${id}
    Click button  css=.plone-modal-footer #form-buttons-add
    Wait until page contains  ${title}
    Go to  ${PLONE_URL}/@@dexterity-types/${id}/@@fields
    Wait until page contains  Fields

Add field
    [Arguments]    ${field_title}    ${field_id}    ${field_type}
    [Documentation]    Add field in current dexterity content type

    Click Overlay Button  Add new field…
    Input text for sure  form-widgets-title  ${field_title}
    Focus  form-widgets-__name__
    Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-__name__  ${field_id}
    Select from list  form-widgets-factory  ${field_type}
    Click button  css=.plone-modal-footer #form-buttons-add
    Wait overlay is closed

Open field settings
    [Arguments]    ${field_id}
    Click Overlay Link  xpath=//div[@data-field_id='${field_id}']//a[@class='fieldSettings pat-plone-modal']
