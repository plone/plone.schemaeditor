# -*- coding: utf-8 -*-
from plone.schemaeditor.interfaces import IEditableSchema
from plone.schemaeditor.utils import FieldRemovedEvent
from plone.schemaeditor.utils import SchemaModifiedEvent
from plone.schemaeditor.utils import sortedFields
from plone.supermodel.interfaces import FIELDSETS_KEY
from Products.Five import BrowserView
from zope.container.contained import notifyContainerModified
from zope.event import notify
from zope.lifecycleevent import ObjectRemovedEvent


class FieldOrderView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.field = context.field
        self.schema = context.field.interface

    def move(self, pos, fieldset_index):
        """ AJAX method to change field position within its schema.
        The position is relative to the fieldset.
        """
        schema = IEditableSchema(self.schema)
        fieldname = self.field.__name__
        pos = int(pos)
        fieldset_index = int(fieldset_index)
        fieldset_index -= 1  # index 0 is default fieldset

        fieldsets = self.schema.queryTaggedValue(FIELDSETS_KEY, [])
        new_fieldset = fieldset_index >= 0 and fieldsets[
            fieldset_index] or None
        schema.changeFieldFieldset(fieldname, new_fieldset)

        ordered_field_ids = [info[0] for info in sortedFields(self.schema)]
        if new_fieldset:
            old_field_of_position = new_fieldset.fields[pos]
            new_absolute_position = ordered_field_ids.index(
                old_field_of_position)
        else:
            new_absolute_position = pos

        # if fieldset changed, update fieldsets
        schema.moveField(fieldname, new_absolute_position)

        notifyContainerModified(self.schema)
        notify(SchemaModifiedEvent(self.__parent__.__parent__))

    def delete(self):
        """
        AJAX method to delete a field
        """
        schema = IEditableSchema(self.schema)
        schema.removeField(self.field.getName())
        notify(ObjectRemovedEvent(self.field, self.schema))
        notify(FieldRemovedEvent(self.__parent__.__parent__, self.field))
        self.request.response.setHeader('Content-Type', 'application/json')
