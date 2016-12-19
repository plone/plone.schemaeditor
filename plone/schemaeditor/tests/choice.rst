.. -*-doctest-*-

==========================================
Choice Fields with Vocabularies or Sources
==========================================

The schema editor allows the user to add Choice fields while also
specifying a vocabulary or source of the values which can be
selected.

Log in as a user who can edit content type schemata and open the
schema editor.

    >>> user = app.acl_users.userFolderAddUser(
    ...     'root', 'secret', ['Manager'], [])

    >>> from Products.Five import testbrowser
    >>> browser = testbrowser.Browser()
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic root:secret')

Open the schema editor in the browser.

    >>> portal_url = 'http://nohost'
    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> 'Edit @@schemaeditor' in browser.contents
    True

Add a Choice field.

    >>> browser.getLink('Add new field').click()
    >>> browser.getControl('Title').value = 'Country'
    >>> browser.getControl('Short Name').value = 'country'
    >>> browser.getControl('Field type').getControl(
    ...     value='label_choice_field').selected = True
    >>> browser.getControl('Add').click()
    [event: ObjectAddedEvent on Choice]
    [event: FieldAddedEvent on DummySchemaContext]
    >>> browser.url
    'http://nohost/@@schemaeditor/@@add-field'

Open the new fields edit form.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='country').click()

The edit form for choice fields includes a widget for specifying the
vocabulary.

    >>> ctl = browser.getControl('Possible values')
    >>> ctl
    <Control name='form.widgets.values' type='textarea'>

If duplicate values are entered an error is raised.

    >>> ctl.value = '\n'.join(
    ...     ['Alaska', 'Russia', 'United States', 'United States',
    ...      'Other'])
    >>> browser.getControl('Save').click()
    >>> print browser.contents
    <...
      <div class="error">The 'United States' vocabulary value conflicts with 'United States'.</div>
    ...

Enter valid values and save the field settings.

    >>> browser.getControl('Possible values').value = '\n'.join(
    ...     ['Alaska', 'Russia', 'United States', "C\xc3\xb4te d'Ivoire", 'Other'])
    >>> browser.getControl('Save').click()
    [event: ObjectModifiedEvent on Choice]
    [event: SchemaModifiedEvent on DummySchemaContext]

When the edit form for the content type is loaded, the vocabulary
values specified can be selected.

    >>> browser.open(portal_url + '/@@contexteditor')
    >>> ctl = browser.getControl('Country')
    >>> item = ctl.getControl('Russia')
    >>> item
    <ItemControl name='form.widgets.country:list' type='select'
    optionValue='Russia' selected=False>
    >>> item.selected = True
    >>> ctl.value
    ['Russia']
    >>> item = ctl.getControl('Alaska')
    >>> item.selected
    False
    >>> item.selected = True
    >>> ctl.getControl('Russia').selected
    False
    >>> ctl.value
    ['Alaska']


We can select a vocabulary factory instead of values.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='country').click()
    >>> browser.getControl('Possible values').value = ""
    >>> voc_name_ctl = browser.getControl('Vocabulary name')
    >>> voc_name_ctl.getControl('plone.schemaeditor.test.Countries').selected = True
    >>> browser.getControl('Save').click()
    [event: ObjectModifiedEvent on Choice]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> browser.open(portal_url + '/@@contexteditor')

    >>> '<option id="form-widgets-country-0" value="fr">France' in browser.contents
    True
    >>> '<option id="form-widgets-country-1" value="uk">United Kingdom' in browser.contents
    True
    >>> '<option id="form-widgets-country-2" value="es">Spain' in browser.contents
    True

We can't set a vocabulary name AND values.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='country').click()
    >>> browser.getControl('values').value = "oups"
    >>> browser.getControl('Save').click()
    >>> print browser.contents
    <...
      <div class="error">You can not set a vocabulary name AND vocabulary values....
    ...


Multiple Choice
===============

A vocabulary of simple values can also be used with a multiple
selection field.

Open the schema editor in the browser.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> 'Edit @@schemaeditor' in browser.contents
    True

Add a Choice field.

    >>> browser.getLink('Add new field').click()
    >>> browser.getControl('Title').value = 'Categories'
    >>> browser.getControl('Short Name').value = 'categories'
    >>> browser.getControl('Field type').getControl(
    ...     'Multiple Choice').selected = True
    >>> browser.getControl('Add').click()
    [event: ObjectAddedEvent on Set]
    [event: FieldAddedEvent on DummySchemaContext]
    >>> browser.url
    'http://nohost/@@schemaeditor/@@add-field'

Open the new fields edit form.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='categories').click()

The edit form for choice fields includes a widget for specifying the
vocabulary.

    >>> ctl = browser.getControl('Possible values')
    >>> ctl
    <Control name='form.widgets.values' type='textarea'>

If duplicate values are entered an error is raised.

    >>> ctl.value = '\n'.join(
    ...     ['Lisp', 'Plone', 'Python', 'Lisp'])
    >>> browser.getControl('Save').click()
    >>> print browser.contents
    <...
      <div class="error">The 'Lisp' vocabulary value conflicts with 'Lisp'.</div>
    ...

Enter unique values and save the field settings.

    >>> browser.getControl('Possible values').value = '\n'.join(
    ...     ['Plone', 'Python', 'Lisp'])
    >>> browser.getControl('Save').click()
    [event: ObjectModifiedEvent on Set]
    [event: SchemaModifiedEvent on DummySchemaContext]

When the edit form for the content type is loaded, the vocabulary
values specified can be selected.

    >>> browser.open(portal_url + '/@@contexteditor')
    >>> browser.getControl('Categories').getControl('Python').selected = True
    >>> browser.getControl('Categories').value
    ['Python']


We can select a vocabulary factory instead of values.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='categories').click()
    >>> browser.getControl('Possible values').value = ""
    >>> voc_name_ctl = browser.getControl('Vocabulary name')
    >>> voc_name_ctl.getControl('plone.schemaeditor.test.Categories').selected = True
    >>> browser.getControl('Save').click()
    [event: ObjectModifiedEvent on Set]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> browser.open(portal_url + '/@@contexteditor')
    >>> '<option id="form-widgets-categories-0" value="php">PHP' in browser.contents
    True
    >>> '<option id="form-widgets-categories-1" value="c">C' in browser.contents
    True
    >>> '<option id="form-widgets-categories-2" value="ruby">Ruby' in browser.contents
    True

Back to the edit form, vocabulary name is selected.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='categories').click()
    >>> print browser.contents
    <...
    ... selected>plone.schemaeditor.test.Categories</option...
    ...
