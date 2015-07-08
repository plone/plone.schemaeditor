.. -*-doctest-*-

=========================
Numeric fields with range
=========================

Let's make sure that if a numeric field is configured with a range,
the endpoints of the range can be adjusted to values outside the
current range.

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

Add an Int field.

    >>> browser.getLink('Add new field').click()
    >>> browser.getControl('Title').value = 'Age'
    >>> browser.getControl('Short Name').value = 'age'
    >>> browser.getControl('Field type').getControl('Integer').selected = True
    >>> browser.getControl('Add').click()
    [event: ObjectAddedEvent on Int]
    [event: FieldAddedEvent on DummySchemaContext]
    >>> browser.url
    'http://nohost/@@schemaeditor/@@add-field'

Open the new fields edit form.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='age').click()

Set the range to 13 to 100.

    >>> browser.getControl(name='form.widgets.min').value = '13'
    >>> browser.getControl(name='form.widgets.max').value = '100'
    >>> browser.getControl('Save').click()
    [event: ObjectModifiedEvent on Int]
    [event: SchemaModifiedEvent on DummySchemaContext]

Return to the form and set the range to values outside the current range.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='age').click()
    >>> browser.getControl(name='form.widgets.min').value = '0'
    >>> browser.getControl(name='form.widgets.max').value = '200'
    >>> browser.getControl('Save').click()
    [event: ObjectModifiedEvent on Int]
    [event: SchemaModifiedEvent on DummySchemaContext]

This should complete without error.
