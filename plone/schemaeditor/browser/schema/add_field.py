# -*- coding: utf-8 -*-
from plone.autoform.form import AutoExtensibleForm
from plone.schemaeditor import _
from plone.schemaeditor import interfaces
from plone.schemaeditor.utils import FieldAddedEvent
from plone.schemaeditor.utils import get_fieldset_from_index
from plone.schemaeditor.utils import IEditableSchema
from plone.schemaeditor.utils import new_field_position
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import NO_VALUE
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

        # remove fieldset_id from data
        if 'fieldset_id' in data:
            fieldset_id = data.pop('fieldset_id')

        # split regular attributes and extra ones
        for key in list(data.keys()):
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

    def add(self, new_field):
        schema = self.context.schema
        fieldset_id = int(self.request.form.get('fieldset_id', 0))

        if self.widgets:
            fieldset_widget = self.widgets.get('fieldset_id')
            if fieldset_widget:
                fieldset_id = int(fieldset_widget.extract())
            position = new_field_position(schema, fieldset_id, new_field=True)
        else:
            position = new_field_position(schema, fieldset_id)

        editable_schema = IEditableSchema(schema)
        try:
            editable_schema.addField(new_field)
        except ValueError:
            raise WidgetActionExecutionError(
                '__name__',
                Invalid(
                    u'Please select a field name that is not already used.'
                )
            )
        if fieldset_id:
            fieldset = get_fieldset_from_index(schema, fieldset_id)
            editable_schema.changeFieldFieldset(new_field.__name__, fieldset)
        editable_schema.moveField(new_field.__name__, position)

        notify(ObjectAddedEvent(new_field, schema))
        notify(FieldAddedEvent(self.context, new_field))
        IStatusMessage(self.request).addStatusMessage(
            _(u'Field added successfully.'), type='info')

    def updateWidgets(self):
        super(FieldAddForm, self).updateWidgets()
        fieldset_id_widget = self.widgets.get('fieldset_id')
        if fieldset_id_widget:
            if not fieldset_id_widget.value or fieldset_id_widget.value == NO_VALUE:
                fieldset_id = int(self.request.form.get('fieldset_id', 0))
                fieldset_id_widget.value = fieldset_id
            fieldset_id_widget.mode = HIDDEN_MODE

    def nextURL(self):
        return '@@add-field'


FieldAddFormPage = wrap_form(
    FieldAddForm,
    index=ViewPageTemplateFile('add.pt')
)
