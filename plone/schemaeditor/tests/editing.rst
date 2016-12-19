Note that for the sake of the test, the test setup has installed a dummy schema
context that will allow us to demonstrate editing a dummy IDummySchema schema, via the
/schemaeditor URL.  It also registers an event handler for various schema events that
will print out the event, so that we can make sure events are getting raised properly.

Let's set up the test browser::

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = 'http://nohost'
    >>> browser.handleErrors = False


Navigating to a schema
----------------------

If we try to access the schema editor without logging in, we should get an Unauthorized
error::

    >>> browser.open(portal_url + '/@@schemaeditor')
    Traceback (most recent call last):
    ...
    Unauthorized: ...You are not authorized to access this resource...

We need to log in as a manager, because by default only managers get the 'Manage Schemata' permission::

    >>> user = self.app.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])
    >>> browser.addHeader('Authorization', 'Basic root:secret')

Now we should be able to navigate to the IDummySchema schema in the browser::

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> 'Edit @@schemaeditor' in browser.contents
    True


Adding a field
--------------

Let's add a 'favorite-color' field to the IDummySchema schema::

    >>> browser.getLink('Add new field').click()
    >>> browser.getControl('Title').value = 'Favorite Color'
    >>> browser.getControl('Short Name').value = 'favorite_color'
    >>> browser.getControl(name='form.widgets.description').value = 'Select your favorite color'
    >>> browser.getControl('Field type').displayValue = ['Text line (String)']
    >>> browser.getControl(name='form.widgets.required').value = ['true']
    >>> browser.getControl('Add').click()
    [event: ObjectAddedEvent on TextLine]
    [event: FieldAddedEvent on DummySchemaContext]
    >>> browser.url
    'http://nohost/@@schemaeditor/@@add-field'

Now the actual IDummySchema schema should have the new field (the field id is a
normalized form of the title)::

    >>> from plone.schemaeditor.tests.fixtures import IDummySchema
    >>> 'favorite_color' in IDummySchema
    True
    >>> from zope.schema import TextLine
    >>> isinstance(IDummySchema['favorite_color'], TextLine)
    True
    >>> IDummySchema['favorite_color'].title
    u'Favorite Color'
    >>> IDummySchema['favorite_color'].required
    True
    >>> IDummySchema['favorite_color'].description
    u'Select your favorite color'


Editing a schema field attribute
--------------------------------

Let's navigate to the 'favorite-color' field we just created::

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='favorite_color').click()
    >>> browser.url
    'http://nohost/@@schemaeditor/favorite_color'
    >>> "Edit Field 'favorite_color'" in browser.contents
    True

Now we can change various attributes.  For instance, let's change the help text
for the 'color' field::

    >>> browser.getControl('Description').value = 'Enter your favorite color.'

And now click the button to save the change.  This should take us back to the list
of schema fields, which should reflect the change::

    >>> browser.getControl('Save').click()
    [event: ObjectModifiedEvent on TextLine]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> browser.url
    'http://nohost/@@schemaeditor/favorite_color/@@edit'

Let's confirm that the new default value was correctly saved to the actual schema::

    >>> IDummySchema['favorite_color'].description
    u'Enter your favorite color.'

If the schema is edited to have internationalized attributes::

    >>> from zope.i18nmessageid import Message
    >>> IDummySchema['favorite_color'].description = Message(
    ...    'favorite_color', domain='plone')

Then editing the schema will preserve those values and only update their
default values::

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='favorite_color').click()
    >>> browser.url
    'http://nohost/@@schemaeditor/favorite_color'
    >>> "Edit Field 'favorite_color'" in browser.contents
    True
    >>> browser.getControl('Description').value
    'favorite_color'
    >>> browser.getControl('Description').value = 'Enter your favorite color.'
    >>> browser.getControl('Save').click()
    [event: ObjectModifiedEvent on TextLine]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> browser.url
    'http://nohost/@@schemaeditor/favorite_color/@@edit'

Let's confirm that the message value was preserved and only its default
value was set::

    >>> type(IDummySchema['favorite_color'].description)
    <... 'zope.i18nmessageid.message.Message'>
    >>> IDummySchema['favorite_color'].description
    u'favorite_color'
    >>> IDummySchema['favorite_color'].description.domain
    'plone'
    >>> IDummySchema['favorite_color'].description.default
    u'Enter your favorite color.'

Let's also check that the support for editing i18n Message values does not
persist its marker interface::

    >>> from plone.schemaeditor.browser.field.edit import IFieldProxy
    >>> IFieldProxy.providedBy(IDummySchema['favorite_color'])
    False

Let's go back and try to make an invalid change.  The form won't let us::

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink(url='favorite_color').click()
    >>> browser.url
    'http://nohost/@@schemaeditor/favorite_color'
    >>> browser.getControl('Minimum length').value = 'asdf'
    >>> browser.getControl('Save').click()
    >>> browser.url
    'http://nohost/@@schemaeditor/favorite_color/@@edit'
    >>> 'The entered value is not a valid integer literal.' in browser.contents
    True

We also cannot set the field title to an empty string, even though the field is
not required in zope.schema.interfaces.IField::

    >>> browser.open('http://nohost/@@schemaeditor/favorite_color')
    >>> browser.getControl('Title').value = ''
    >>> browser.getControl('Save').click()
    >>> browser.url
    'http://nohost/@@schemaeditor/favorite_color/@@edit'
    >>> 'Required input is missing.' in browser.contents
    True

We can give up and hit the Cancel button, which should take us back to the schema listing,
without trying to save changes::

    >>> browser.getControl('Cancel').click()
    >>> browser.url
    'http://nohost/@@schemaeditor'


Re-ordering a field
-------------------

The field we added was created in a position following the 5 existing fields on the
interface::

    >>> from zope.schema import getFieldsInOrder
    >>> getFieldsInOrder(IDummySchema)[5][0]
    'favorite_color'

Fields can be reordered via drag-and-drop.  Let's simulate the AJAX request that would
result from dragging the 'favorite_color' field to the 3rd position (since the
testbrowser doesn't support Javascript)::

    >>> browser.open('http://nohost/@@schemaeditor/favorite_color/@@order?pos=2&fieldset_index=0')
    [event: ContainerModifiedEvent on InterfaceClass]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> browser.contents
    ''

Now the field should be the third field of the schema::

    >>> getFieldsInOrder(IDummySchema)[2][0]
    'favorite_color'

Now let's move it to be the first field (as there is an edge case in the ordering
algorithm that we need to test)::

    >>> browser.open('http://nohost/@@schemaeditor/favorite_color/@@order?pos=0&fieldset_index=0')
    [event: ContainerModifiedEvent on InterfaceClass]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> getFieldsInOrder(IDummySchema)[0][0]
    'favorite_color'


Moving a field to an other fieldset
-----------------------------------

Fields can be moved from a fieldset to an other one.
They are moved to the end of the new fieldset::

    >>> browser.open('http://nohost/@@schemaeditor/favorite_color/@@changefieldset?fieldset_index=1')
    [event: ContainerModifiedEvent on InterfaceClass]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> browser.contents
    ''

Now the field should be the seventh field of the schema::

    >>> getFieldsInOrder(IDummySchema)[6][0]
    'favorite_color'
    >>> from plone.schemaeditor.utils import get_field_fieldset
    >>> get_field_fieldset(IDummySchema, 'favorite_color')
    <Fieldset 'alpha'...of fieldA, favorite_color>

They can be ordered into a fieldset::

    >>> browser.open('http://nohost/@@schemaeditor/favorite_color/@@order?pos=0&fieldset_index=1')
    [event: ContainerModifiedEvent on InterfaceClass]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> browser.contents
    ''
    >>> get_field_fieldset(IDummySchema, 'favorite_color')
    <Fieldset 'alpha'...of favorite_color, fieldA>

Now the field should be the sixth field of the schema::

    >>> getFieldsInOrder(IDummySchema)[5][0]
    'favorite_color'


Moving a field into an other fieldset and directly set the position
-------------------------------------------------------------------

If form tabbing is disabled, you can move a field from a fieldset directly to
a position in the new fieldset.

    >>> browser.open('http://nohost/@@schemaeditor/favorite_color/@@order?pos=1&fieldset_index=0')
    [event: ContainerModifiedEvent on InterfaceClass]
    [event: SchemaModifiedEvent on DummySchemaContext]

Now the field should be the second field of the schema, in the default fieldset ::

    >>> getFieldsInOrder(IDummySchema)[1][0]
    'favorite_color'


Removing a field
----------------

We can also remove a field::

    >>> browser.open('http://nohost/@@schemaeditor')
    >>> browser.getLink(url='favorite_color/@@delete').click()
    [event: ObjectRemovedEvent on TextLine]
    [event: FieldRemovedEvent on DummySchemaContext]

And confirm that the real schema was updated::

    >>> 'favorite_color' in IDummySchema
    False
    >>> from plone.supermodel.interfaces import FIELDSETS_KEY
    >>> 'favorite_color' in [i for f in IDummySchema.getTaggedValue(FIELDSETS_KEY) for i in f.fields]
    False


Removing a field in other fieldset
----------------------------------

Let's add a 'other_set' field to the IDummySchema schema,
move it into an other fieldset and remove it::

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink('Add new field').click()
    >>> browser.getControl('Title').value = 'Other Set'
    >>> browser.getControl('Short Name').value = 'other_set'
    >>> browser.getControl('Field type').displayValue = ['Text line (String)']
    >>> browser.getControl('Add').click()
    [event: ObjectAddedEvent on TextLine]
    [event: FieldAddedEvent on DummySchemaContext]
    >>> IDummySchema['other_set'].required
    False
    >>> browser.open('http://nohost/@@schemaeditor/other_set/@@changefieldset?fieldset_index=1')
    [event: ContainerModifiedEvent on InterfaceClass]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> browser.contents
    ''
    >>> browser.open('http://nohost/@@schemaeditor')
    >>> browser.getLink(url='other_set/@@delete').click()
    [event: ObjectRemovedEvent on TextLine]
    [event: FieldRemovedEvent on DummySchemaContext]

And confirm that the real schema was updated::

    >>> 'other_set' in IDummySchema
    False
    >>> from plone.supermodel.interfaces import FIELDSETS_KEY
    >>> 'other_set' in [i for f in IDummySchema.getTaggedValue(FIELDSETS_KEY) for i in f.fields]
    False


Adding a fieldset
-----------------

Let's add a 'extra-info' fieldset to the IDummySchema schema::

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink('Add new fieldset').click()
    >>> browser.getControl('Title').value = 'Extra information'
    >>> browser.getControl('Short Name').value = 'extra-info'
    >>> browser.getControl('Add').click()
    >>> browser.contents
    '<...Please use only letters, numbers and the following characters...'
    >>> browser.getControl('Short Name').value = 'extra_info'
    >>> browser.getControl('Add').click()
    [event: ContainerModifiedEvent on InterfaceClass]
    [event: SchemaModifiedEvent on DummySchemaContext]
    >>> browser.url
    'http://nohost/@@schemaeditor/@@add-fieldset'

Now the actual IDummySchema schema should have the new fieldset ::

    >>> from plone.supermodel.interfaces import FIELDSETS_KEY
    >>> IDummySchema.getTaggedValue(FIELDSETS_KEY)
    [<Fieldset 'alpha'...of fieldA>, <Fieldset 'extra_info'...of >]


Miscellaneous field types
-------------------------

Demonstrate that all the registered field types can be added edited
and saved.

    >>> from zope import component
    >>> from plone.schemaeditor import interfaces
    >>> schema = IDummySchema
    >>> start_field_count = len(IDummySchema.names())
    >>> for name, factory in sorted(component.getUtilitiesFor(
    ...     interfaces.IFieldFactory)):
    ...     browser.open(portal_url + '/@@schemaeditor')
    ...     browser.getLink('Add new field').click()
    ...     browser.getControl('Title').value = name
    ...     field_id = name.replace('-', '_')
    ...     browser.getControl('Short Name').value = field_id
    ...     browser.getControl('Field type').value = [factory.title]
    ...     browser.getControl('Add').click()
    ...     assert browser.url == portal_url + '/@@schemaeditor/@@add-field', (
    ...         'Failed to create %r' % name)
    ...     assert field_id in schema, '%r not in %r' % (
    ...         field_id, schema)
    ...     assert factory.fieldcls._type is None or isinstance(
    ...         schema[field_id], factory.fieldcls
    ...         ), '%r is not an instance of %r' % (
    ...             schema[field_id], factory.fieldcls)
    ...     browser.open(portal_url + '/@@schemaeditor')
    ...     browser.getLink(url=field_id).click()
    ...     browser.getControl('Title').value += ' '
    ...     browser.getControl('Save').click()
    [event: ObjectAddedEvent on Bool]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: SchemaModifiedEvent on DummySchemaContext]
    [event: ObjectAddedEvent on Int]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: SchemaModifiedEvent on DummySchemaContext]
    [event: ObjectAddedEvent on Password]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: SchemaModifiedEvent on DummySchemaContext]
    [event: ObjectAddedEvent on Text]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: SchemaModifiedEvent on DummySchemaContext]
    [event: ObjectAddedEvent on TextLine]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: SchemaModifiedEvent on DummySchemaContext]
    [event: ObjectAddedEvent on Choice]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: ObjectModifiedEvent on Choice]
    [event: SchemaModifiedEvent on DummySchemaContext]
    [event: ObjectAddedEvent on Date]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: SchemaModifiedEvent on DummySchemaContext]
    [event: ObjectAddedEvent on Datetime]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: SchemaModifiedEvent on DummySchemaContext]
    [event: ObjectAddedEvent on Float]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: SchemaModifiedEvent on DummySchemaContext]
    [event: ObjectAddedEvent on Set]
    [event: FieldAddedEvent on DummySchemaContext]
    [event: ObjectModifiedEvent on Set]
    [event: SchemaModifiedEvent on DummySchemaContext]



Reserved field names
--------------------

Since fields are accessible by names as attributes of a content item, we
reserve some field names that are already in use by Dublin Core metadata
attributes. Users cannot add fields with these names.

    >>> for fname in ("subject", "format", "language",
    ...               "creators", "contributors", "rights",
    ...               "effective_date", "expiration_date"):
    ...     browser.open(portal_url + '/@@schemaeditor')
    ...     browser.getLink('Add new field').click()
    ...     browser.getControl('Title').value = fname
    ...     browser.getControl('Short Name').value = fname
    ...     browser.getControl('Add').click()
    ...     assert 'is a reserved field name' in browser.contents

The ``title`` and ``description`` field names are also reserved, but since
it's a common need to customize the wording of the label and help text for
these fields, they are allowed as long as the field is of the correct type.

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> browser.getLink('Add new field').click()
    >>> browser.getControl('Title').value = 'title'
    >>> browser.getControl('Short Name').value = 'title'
    >>> browser.getControl('Field type').getControl('Integer').selected = True
    >>> browser.getControl('Add').click()
    >>> browser.url
    'http://nohost/@@schemaeditor/@@add-field'
    >>> browser.getControl('Field type').getControl('String').selected = True
    >>> browser.getControl('Add').click()
    [event: ObjectAddedEvent on TextLine]
    [event: FieldAddedEvent on DummySchemaContext]
    >>> browser.url
    'http://nohost/@@schemaeditor/@@add-field'
