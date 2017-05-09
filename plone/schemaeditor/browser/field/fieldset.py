# -*- coding: utf-8 -*-
from plone.schemaeditor.interfaces import IEditableSchema
from plone.schemaeditor.utils import new_field_position
from plone.schemaeditor.utils import get_fieldset_from_index
from plone.schemaeditor.utils import SchemaModifiedEvent
from Products.Five import BrowserView
from zope.container.contained import notifyContainerModified
from zope.event import notify


class ChangeFieldsetView(BrowserView):

    def change(self, fieldset_index):
        """ AJAX method to change the fieldset of a field
        """
        schema = self.context.field.interface
        field_name = self.context.field.__name__
        fieldset = get_fieldset_from_index(schema, fieldset_index)
        position = new_field_position(schema, fieldset_index)

        editable_schema = IEditableSchema(schema)
        editable_schema.changeFieldFieldset(field_name, fieldset)
        editable_schema.moveField(field_name, position)

        notifyContainerModified(schema)
        notify(SchemaModifiedEvent(self.__parent__.__parent__))
