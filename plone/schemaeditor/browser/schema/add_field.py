from zope.component import getUtility
from zope.event import notify
from zope.app.container.contained import ObjectAddedEvent
from z3c.form import form, field
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.z3cform.layout import wrap_form

from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor.interfaces import INewField
from plone.schemaeditor.utils import IEditableSchema

class FieldAddForm(form.AddForm):

    fields = field.Fields(INewField)
    label = "Add new field"
    id = 'add-field-form'

    def create(self, data):
        id = getUtility(IIDNormalizer).normalize(data['title'])
        id = id.replace('-', '_')
        # XXX validation

        data['__name__'] = id
        factory = data.pop('factory')
        return factory(**data)

    def add(self, field):
        schema = IEditableSchema(self.context.schema)
        schema.addField(field)
        notify(ObjectAddedEvent(field, self.context.schema))
        self.status = _(u"Field added successfully.")

    def nextURL(self):
        return self.context.absolute_url()

FieldAddFormPage = wrap_form(FieldAddForm)
