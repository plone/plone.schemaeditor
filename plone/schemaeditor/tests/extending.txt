Extending the schema editor
---------------------------

The schema editor is designed to be extensible so that add-ons can support
editing additional pieces of field metadata.

This can be accomplished by registering an IFieldEditorExtender adapter.
The schema returned when this adapter is looked up can provide additional
fields and autoform hints that will be used by the for for editing a field's
settings.

For example, let's add a setting so that a different color can be specified
for each field. First we need an interface that provides that setting::

  >>> from zope.interface import Interface
  >>> from zope import schema
  >>> class IFieldColor(Interface):
  ...     color = schema.TextLine(title = u'Color')

We could register this schema directly as a named adapter providing
IFieldEditorExtender. But if we want to do any additional filtering for which
fields should have the new setting available, we can instead register a
separate callable (an "adapter factory") which returns the schema only
if those filters succeed.  In this case, we limit the extender to
fields that have 'field' in their name::

  >>> from zope.component import provideAdapter, adapter, adapts
  >>> from zope.schema.interfaces import IField
  >>> from plone.schemaeditor.interfaces import ISchemaContext
  >>> @adapter(ISchemaContext, IField)
  ... def get_color_schema(schema_context, field):
  ...     if 'field' in field.__name__:
  ...         return IFieldColor

  >>> from plone.schemaeditor.interfaces import IFieldEditorExtender
  >>> provideAdapter(get_color_schema, provides=IFieldEditorExtender, name='plone.schemaeditor.color')

In order to actually get and set values for this field on content items,
we need an adapter that provides the IFieldColor interface::

  >>> class FieldColorAdapter(object):
  ...     adapts(IField)
  ...
  ...     def __init__(self, field):
  ...         self.field = field
  ...
  ...     def _get_color(self):
  ...         colors = self.field.interface.queryTaggedValue('color', {})
  ...         return colors.get(self.field.__name__)
  ...     def _set_color(self, value):
  ...         colors = self.field.interface.queryTaggedValue('color', {})
  ...         colors[self.field.__name__] = value
  ...         self.field.interface.setTaggedValue('color', colors)
  ...     color = property(_get_color, _set_color)
  >>> provideAdapter(FieldColorAdapter, provides=IFieldColor)

Now we can bring up the edit form for one of the test fields, and it should
have the additional 'color' setting::

  >>> from Products.Five.testbrowser import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> user = self.app.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])
  >>> browser.addHeader('Authorization', 'Basic root:secret')

  >>> browser.open('http://nohost/@@schemaeditor/field1')
  >>> color_textbox = browser.getControl('Color')

We can save a color and confirm that it ends up in the schema's tagged values::

  >>> color_textbox.value = 'green'
  >>> browser.getControl('Title').value = 'test'
  >>> browser.getControl('Save').click()
  [event: ObjectModifiedEvent on TextLine]
  [event: SchemaModifiedEvent on DummySchemaContext]
  >>> from plone.schemaeditor.tests.fixtures import IDummySchema
  >>> IDummySchema.getTaggedValue('color')
  {'field1': u'green'}
