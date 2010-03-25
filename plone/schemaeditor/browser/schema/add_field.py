from zope.event import notify
from zope.interface import Invalid
from zope.app.container.contained import ObjectAddedEvent
from z3c.form import form, field
from z3c.form.interfaces import WidgetActionExecutionError
from plone.z3cform.layout import wrap_form

from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor.interfaces import INewField
from plone.schemaeditor.utils import IEditableSchema

class FieldAddForm(form.AddForm):

    fields = field.Fields(INewField)
    label = "Add new field"
    id = 'add-field-form'

    def create(self, data):
        factory = data.pop('factory')
        return factory(**data)

    def add(self, field):
        schema = IEditableSchema(self.context.schema)
        try:
            schema.addField(field)
        except ValueError:
            raise WidgetActionExecutionError('__name__',
                Invalid(u'Please select a field name that is not already used.'))
        notify(ObjectAddedEvent(field, self.context.schema))
        self.status = _(u"Field added successfully.")

    def nextURL(self):
        return self.context.absolute_url()

FieldAddFormPage = wrap_form(FieldAddForm)
