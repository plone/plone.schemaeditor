*** Settings ***

Resource    plone/app/robotframework/browser.robot

Library    Remote    ${PLONE_URL}/RobotRemote

Test Setup    Run Keywords    Plone test setup
Test Teardown    Run keywords    Plone test teardown


*** Variables ***

${ADD_FIELDSET_SELECTOR}    //a[@id="add-fieldset"]
${ADD_FIELD_SELECTOR}       //a[@id="add-field"]



*** Test Cases ***

Scenario: Add a content type

    Given a site owner
     When I go to dexterity types configuration
      and I add a new Content Type    New style Article    new_style_article
     Then the overlay is closed
      and the new Content Type is created    New style Article


Scenario: Add a choice field with a named vocabulary

    Given a site owner
     When I go to dexterity types configuration
      and I add a new Content Type    Curriculum vitae    curriculum_vitae
      and I go to fields configuration    curriculum_vitae
      and I add a new field    Languages    languages    Multiple Choice
     Then the overlay is closed
      and the new Field is created    languages

     When I configure the language field
     Then the overlay is closed
      and I see the list of portal languages

Scenario: Add a choice field with vocabulary values

    Given a site owner
     When I go to dexterity types configuration
      and I add a new Content Type    My page    my_page
      and I go to fields configuration    my_page
      and I add a new field    Hobbies    hobbies    Multiple Choice
     Then the overlay is closed
      and the new Field is created    hobbies

     When I configure the hobbies field
     Then the overlay is closed
      and I see the list of hobbies

Scenario: Try to add a choice field with a named vocabulary and vocabulary values

    Given a site owner
     When I go to dexterity types configuration
      and I add a new Content Type    My other page    my_other_page
      and I go to fields configuration    my_other_page
      and I add a new field    Hobbies    hobbies    Multiple Choice
      and I configure the hobbies field with wrong values
     Then I see an errormessage in the dialog

Scenario: Add accented field

    Given a site owner
     When I go to dexterity types configuration
      and I add a new Content Type    Person    person
      and I go to fields configuration    person
      and I add a new field    Prénom    prenom    Text line (String)
     Then the overlay is closed
      and the new Field is created    prenom

Scenario: Add a fieldSet and move a field into this fieldset

    Given a site owner
    When I go to dexterity types configuration
     and I add a new Content Type    Contact info    contact_info
     and I go to fields configuration    contact_info
     and I add a new field    Address    address    Text
     and I add a new fieldset    Personal information    personal_information
    Then the overlay is closed
     and the new fieldset is created    Personal information

Scenario: Add a fieldSet and add a field into this fieldset

    Given a site owner
    When I go to dexterity types configuration
     and I add a new Content Type    Contact info    contact_info
     and I go to fields configuration    contact_info
     and I add a new fieldset    Personal information    personal_information
     and I got to fieldset    Personal information
     and I add a new field    Address    address    Text
    Then the field is added to fieldset    Personal information    Address

Scenario: Delete field

    Given a site owner
    When I go to dexterity types configuration
     and I add a new Content Type    Somebody    somebody
     and I go to fields configuration    somebody
     and I add a new field    Phone    phone    Text line (String)
    Then the overlay is closed
     and the new Field is created    phone

    When I delete field    phone
    Then the field is removed    phone


*** Keywords ***

# Given

a site owner

    Enable autologin as    Manager

# When

I go to dexterity types configuration

    Go to    ${PLONE_URL}/@@dexterity-types

I go to fields configuration
    [Arguments]    ${CONTENT_TYPE_ID}

    Click    //a[contains(@class, "contenttype-${CONTENT_TYPE_ID}")]
    Click    //a[contains(@href,"/${CONTENT_TYPE_ID}/@@fields")]

I got to fieldset
    [Arguments]    ${FIELD_LABEL}

    Click    //*[contains(@class, "autotoc-nav")]//a[contains(text(),"${FIELD_LABEL}")]


I add a new Content Type
    [Arguments]    ${CONTENT_TYPE_NAME}    ${CONTENT_TYPE_ID}
    [Documentation]    Add a new dexterity content type

    Click Modal Link   //article[@id="content"]//button[contains(text(),'Add New Content Type…')]
    Type Text    //input[@name="form.widgets.title"]    ${CONTENT_TYPE_NAME}
    Focus    //input[@name="form.widgets.id"]
    Get Text    //input[@name="form.widgets.id"]    should be    ${CONTENT_TYPE_ID}
    Click    //div[contains(@class,"modal-footer")]//button[@id="form-buttons-add"]

I add a new field
    [Arguments]    ${FIELD_LABEL}     ${FIELD_ID}     ${FIELD_TYPE}
    [Documentation]    Add field in current dexterity content type

    Wait For Element Click Events    ${ADD_FIELD_SELECTOR}
    Click Modal Link    ${ADD_FIELD_SELECTOR}
    Type Text    //input[@name="form.widgets.title"]    ${FIELD_LABEL}
    Focus    //input[@name="form.widgets.__name__"]
    Get Text    //input[@name="form.widgets.__name__"]    should be    ${FIELD_ID}
    Get Property   //input[@name="form.widgets.__name__"]    value    should be     ${FIELD_ID}
    Get Text    //input[@name="form.widgets.__name__"]    should be    ${FIELD_ID}
    Type Text    //textarea[@name="form.widgets.description"]    my description of the field
    Select Options By    //select[@name="form.widgets.factory:list"]    label    ${FIELD_TYPE}
    Click    //div[contains(@class,"modal-footer")]//button[@id="form-buttons-add"]

I add a new fieldset
    [Arguments]    ${FIELDSET_LABEL}    ${FIELDSET_ID}
    [Documentation]    Add fieldset in current dexterity content type

    Wait For Element Click Events    ${ADD_FIELDSET_SELECTOR}
    Click Modal Link    ${ADD_FIELDSET_SELECTOR}
    Type Text    //input[@name="form.widgets.label"]    ${FIELDSET_LABEL}
    Focus    //input[@name="form.widgets.__name__"]
    Get Property   //input[@name="form.widgets.__name__"]    value    should be     ${FIELDSET_ID}
    Get Text    //input[@name="form.widgets.__name__"]    should be    ${FIELDSET_ID}
    Click    //div[contains(@class,"modal-footer")]//button[@id="form-buttons-add"]

I configure the language field

    Click Modal Link    //div[@data-field_id="languages"]//a[contains(text(),'Settings…')]
    Select Options By    //select[@name="form.widgets.vocabularyName:list"]    value    plone.app.vocabularies.AvailableContentLanguages
    Click    //div[contains(@class,"modal-footer")]//button[@id="form-buttons-save"]

I configure the hobbies field

    Click Modal Link    //div[@data-field_id="hobbies"]//a[contains(text(),'Settings…')]
    Type Text    //textarea[@name="form.widgets.values"]    Chess    clear=False
    Press Keys    //textarea[@name="form.widgets.values"]    Enter
    Type Text    //textarea[@name="form.widgets.values"]    Soccer    clear=False
    Press Keys    //textarea[@name="form.widgets.values"]    Enter
    Type Text    //textarea[@name="form.widgets.values"]    Baseball    clear=False
    Press Keys    //textarea[@name="form.widgets.values"]    Enter
    Type Text    //textarea[@name="form.widgets.values"]    Video games    clear=False
    Press Keys    //textarea[@name="form.widgets.values"]    Enter
    Click    //div[contains(@class,"modal-footer")]//button[@id="form-buttons-save"]

I configure the hobbies field with wrong values

    Click Modal Link    //div[@data-field_id="hobbies"]//a[contains(text(),'Settings…')]
    Type Text    //textarea[@name="form.widgets.values"]    Chess    clear=False
    Press Keys    //textarea[@name="form.widgets.values"]    Enter
    Type Text    //textarea[@name="form.widgets.values"]    Soccer    clear=False
    Press Keys    //textarea[@name="form.widgets.values"]    Enter
    Type Text    //textarea[@name="form.widgets.values"]    Baseball    clear=False
    Press Keys    //textarea[@name="form.widgets.values"]    Enter
    Type Text    //textarea[@name="form.widgets.values"]    Video games    clear=False
    Press Keys    //textarea[@name="form.widgets.values"]    Enter
    Select Options By    //select[@name="form.widgets.vocabularyName:list"]    value    plone.app.vocabularies.AvailableContentLanguages
    Click    //div[contains(@class,"modal-footer")]//button[@id="form-buttons-save"]

I delete field
    [Arguments]    ${FIELD_ID}

    Handle Future Dialogs    action=accept
    Click    //div[@data-field_id="${FIELD_ID}"]//a[@title="Delete field"]

# Then

the overlay is closed
    Wait For Condition    Element Count    //div[contains(@class,"modal-wrapper")]    ==    0    timeout=5s

the new Content Type is created
    [Arguments]        ${CONTENT_TYPE_NAME}

    Get Text    //div[@class="crud-form"]/form/table    contains    ${CONTENT_TYPE_NAME}

the new Field is created
    [Arguments]        ${FIELD_ID}

    Get Text    //*[@id="global_statusmessage"]    contains    Field added successfully.
    Get Element Count    //div[@data-field_id="${FIELD_ID}"]//a[contains(text(),'Settings…')]    should be    1

I see the list of portal languages

    Get Element Count    //select[@name="form.widgets.languages:list"]/option    greater than    0

I see the list of hobbies

    Get Element Count    //select[@name="form.widgets.hobbies:list"]/option    greater than    0

I see an errormessage in the dialog

    Get Text    //div[contains(@class,"modal-body")]//div[contains(@class,"statusmessage")]    contains    There were some errors.
    Get Text    //div[@id="formfield-form-widgets-vocabularyName"]//div[@class="invalid-feedback"]    contains    You can not set a vocabulary name AND vocabulary values. Please clear values field or set no value here.

the new fieldset is created
    [Arguments]    ${FIELDSET_LABEL}

    Get Text    //*[@id="global_statusmessage"]    contains    Fieldset added successfully.
    Get Element Count    //form[@id="form"]//fieldset/legend[contains(text(),"${FIELDSET_LABEL}")]    should be    1

the field is added to fieldset
    [Arguments]    ${FIELDSET_LABEL}    ${FIELD_LABEL}

    Get Text    //*[@id="global_statusmessage"]    contains    Field added successfully.
    Get Element Count    //form[@id="form"]//fieldset/legend[contains(text(),"${FIELDSET_LABEL}")]/following-sibling::div[@data-field_id="address"]    should be    1

the field is removed
    [Arguments]    ${FIELD_ID}

    Get Element Count    //div[@data-field_id="${FIELD_ID}"]    should be    0


Click Modal Link
    [Arguments]    ${SELECTOR}

    Click    ${SELECTOR}
    Wait For Condition    Element States    //div[contains(@class,"modal-dialog")]    contains    visible
    # Wait For Condition    Element States    //div[@class="modal-wrapper"]    contains    attached    visible
    Wait For Condition    Classes    //body    contains    modal-open
    Wait For Condition    Classes    //div[@class="modal-wrapper"]/div/div    contains    show


Wait For Element Click Events
    [Arguments]    ${SELECTOR}
    [Documentation]    Wait for an element to have jQuery click events attached before proceeding

    Wait For Function    () => { const el = document.evaluate(`${SELECTOR}`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return el && window.jQuery._data(el, 'events').click; }
