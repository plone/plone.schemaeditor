from zope.component import provideAdapter, adapter, adapts
from zope.interface import Interface
from zope.schema.interfaces import IField
from zope import schema
from plone.schemaeditor.interfaces import ISchemaContext
from plone.schemaeditor.interfaces import IFieldEditorExtender


# This is a new schema which provides an additional field, color.
class IFieldColor(Interface):
	color = schema.TextLine(title = u'Color')


# This is the adapter which can actually get/set the color for a field.
class FieldColorAdapter(object):
	adapts(IField)

	def __init__(self, field):
		self.field = field

	def _get_color(self):
		colors = self.context.interface.queryTaggedValue('color', {})
		return colors.get(self.field.__name__)
	def _set_color(self, value):
		colors = self.context.interface.queryTaggedValue('color', {})
		colors[self.field.__name__] = value
		self.context.setTaggedValue('color', colors)


# IFieldColor could be registered directly as a named adapter providing IFieldEditorExtender
# for ISchemaContext and IField. But we can also register a separate callable which returns
# the schema only if additional conditions pass:
@adapter(ISchemaContext, IField)
def get_color_schema(schema_context, field):
	if field.__name__ == 'asdf':
		return IFieldColor


# Register the callable which makes the field edit form know about the new schema:
provideAdapter(get_color_schema, provides=IFieldEditorExtender, name='plone.schemaeditor.color')
# And the adapter for getting/setting the value.
provideAdapter(FieldColorAdapter, provides=IFieldColor)
