# -*- coding: utf-8 -*-
from plone.autoform.form import AutoExtensibleForm
from plone.schemaeditor import _
from plone.schemaeditor import interfaces
from plone.schemaeditor.utils import FieldAddedEvent
from plone.schemaeditor.utils import IEditableSchema
from plone.schemaeditor.utils import non_fieldset_fields
from plone.schemaeditor.utils import sortedFields
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import WidgetActionExecutionError
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import getAdapters
from zope.event import notify
from zope.interface import Interface
from zope.interface import Invalid
from zope.lifecycleevent import ObjectAddedEvent


class FieldAddForm(AutoExtensibleForm, form.AddForm):

    fields = field.Fields(interfaces.INewField)
    label = _('Add new field')
    id = 'add-field-form'

    # This is a trick: we want autoform to handle the additionalSchemata,
    # but want to provide our own base schema below in updateFields.
    schema = Interface

    @lazy_property
    def _schema(self):
        return interfaces.INewField

    @lazy_property
    def additionalSchemata(self):
        return [v for k, v in getAdapters((self.context, ),
                                          interfaces.IFieldEditorExtender)]

    def create(self, data):
        extra = {}
        factory = data.pop('factory')
        all = data.keys()

        # split regular attributes and extra ones
        for key in all:
            if key not in self._schema:
                extra[key] = data[key]
                data.pop(key)

        # create the field with regular attributes
        field_obj = factory(**data)

        # set the extra attributes using the proper adapter
        for schemata in self.additionalSchemata:
            for key in extra:
                (interface_name, property_name) = key.split('.')
                if interface_name != schemata.__name__:
                    continue
                setattr(schemata(field_obj), property_name, extra[key])

        return field_obj

    def add(self, field):
        context = self.context
        schema = IEditableSchema(context.schema)

        # move it after the last field that is not in a fieldset
        # or at top if there is no field yet in "default" fieldset
        ordered_fields = [name for (name, f) in sortedFields(context.schema)]
        default_fields = non_fieldset_fields(context.schema)
        if len(default_fields) > 0:
            position = ordered_fields.index(default_fields[-1]) + 1
        else:
            position = 0

        try:
            schema.addField(field)
        except ValueError:
            raise WidgetActionExecutionError(
                '__name__',
                Invalid(
                    u'Please select a field name that is not already used.'
                )
            )

        schema.moveField(field.__name__, position)
        notify(ObjectAddedEvent(field, context.schema))
        notify(FieldAddedEvent(context, field))
        IStatusMessage(self.request).addStatusMessage(
            _(u"Field added successfully."), type='info')

    def nextURL(self):
        return '@@add-field'


FieldAddFormPage = wrap_form(
    FieldAddForm,
    index=ViewPageTemplateFile('add.pt')
)
