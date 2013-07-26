from zope.event import notify
from zope.interface import Invalid
from zope.lifecycleevent import ObjectAddedEvent
from z3c.form import form, field
from z3c.form.interfaces import WidgetActionExecutionError
from plone.z3cform.layout import wrap_form

from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor.interfaces import INewField
from plone.schemaeditor.utils import IEditableSchema, non_fieldset_fields,\
    sortedFields
from plone.schemaeditor.utils import FieldAddedEvent


class FieldAddForm(form.AddForm):

    fields = field.Fields(INewField)
    label = _("Add new field")
    id = 'add-field-form'

    def create(self, data):
        factory = data.pop('factory')
        return factory(**data)

    def add(self, field):
        context = self.context
        schema = IEditableSchema(context.schema)

        # move it after the last field that is not in a fieldset
        ordered_fields = [name for (name, f) in sortedFields(context.schema)]
        last_non_fieldset_field = non_fieldset_fields(context.schema)[-1]
        position = ordered_fields.index(last_non_fieldset_field) + 1

        try:
            schema.addField(field)
        except ValueError:
            raise WidgetActionExecutionError('__name__',
                Invalid(u'Please select a field name that is not already used.'))

        schema.moveField(field.__name__, position)
        notify(ObjectAddedEvent(field, context.schema))
        notify(FieldAddedEvent(context, field))
        self.status = _(u"Field added successfully.")

    def nextURL(self):
        url = self.context.absolute_url()
        if getattr(self.context, 'schemaEditorView', None) is not None:
            url += '/@@' + self.context.schemaEditorView
        return url

FieldAddFormPage = wrap_form(FieldAddForm)
