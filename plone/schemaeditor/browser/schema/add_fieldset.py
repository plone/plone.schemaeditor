# -*- coding: utf-8 -*-
from plone.schemaeditor import _
from plone.schemaeditor.interfaces import INewFieldset
from plone.schemaeditor.utils import SchemaModifiedEvent
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import WidgetActionExecutionError
from zope.container.contained import notifyContainerModified
from zope.event import notify
from zope.interface import Invalid


class FieldsetAddForm(form.AddForm):

    fields = field.Fields(INewFieldset)
    label = _('Add new fieldset')
    id = 'add-fieldset-form'

    def create(self, data):
        return Fieldset(**data)

    def add(self, new_fieldset):
        schema = self.context.schema
        fieldsets = schema.queryTaggedValue(FIELDSETS_KEY, [])

        for fieldset in fieldsets:
            if fieldset.__name__ == new_fieldset.__name__:
                msg = _(
                    u'Please select a fieldset name that is not already used.'
                )
                raise WidgetActionExecutionError(
                    '__name__',
                    Invalid(msg)
                )

        fieldsets.append(new_fieldset)
        schema.setTaggedValue(FIELDSETS_KEY, fieldsets)
        notifyContainerModified(schema)
        notify(SchemaModifiedEvent(self.context))
        IStatusMessage(self.request).addStatusMessage(
            _(u"Fieldset added successfully."), type='info')

    def nextURL(self):
        return '@@add-fieldset'


FieldsetAddFormPage = wrap_form(
    FieldsetAddForm,
    index=ViewPageTemplateFile('add.pt')
)
