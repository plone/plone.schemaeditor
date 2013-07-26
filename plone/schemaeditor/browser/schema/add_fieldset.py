from zope.event import notify
from zope.interface import Invalid
from zope.lifecycleevent import ObjectAddedEvent
from zope.container.contained import notifyContainerModified

from z3c.form import form, field
from z3c.form.interfaces import WidgetActionExecutionError
from plone.z3cform.layout import wrap_form

from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor.interfaces import INewFieldset
from plone.schemaeditor.utils import IEditableSchema, non_fieldset_fields,\
    sortedFields, SchemaModifiedEvent
from plone.schemaeditor.utils import FieldAddedEvent
from plone.supermodel.model import Fieldset
from plone.supermodel.interfaces import FIELDSETS_KEY


class FieldsetAddForm(form.AddForm):

    fields = field.Fields(INewFieldset)
    label = _("Add new fieldset")
    id = 'add-fieldset-form'

    def create(self, data):
        return Fieldset(**data)

    def add(self, new_fieldset):
        schema = self.context.schema
        fieldsets = schema.getTaggedValue(FIELDSETS_KEY)

        for fieldset in fieldsets:
            if fieldset.__name__ == new_fieldset.__name__:
                raise WidgetActionExecutionError('__name__',
                    Invalid(_(u'Please select a fieldset name that is not already used.')))

        fieldsets.append(new_fieldset)
        schema.setTaggedValue(FIELDSETS_KEY, fieldsets)
        notifyContainerModified(schema)
        notify(SchemaModifiedEvent(self.context))
        self.status = _(u"Fieldset added successfully.")

    def nextURL(self):
        url = self.context.absolute_url()
        if getattr(self.context, 'schemaEditorView', None) is not None:
            url += '/@@' + self.context.schemaEditorView

        return url

FieldsetAddFormPage = wrap_form(FieldsetAddForm)
