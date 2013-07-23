from Products.Five import BrowserView
from plone.schemaeditor.interfaces import IEditableSchema
from zope.container.contained import notifyContainerModified
from zope.event import notify
from zope.lifecycleevent import ObjectRemovedEvent
from plone.schemaeditor.utils import SchemaModifiedEvent, sortedFields
from plone.schemaeditor.utils import FieldRemovedEvent
from plone.supermodel.interfaces import FIELDSETS_KEY


class FieldOrderView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.field = context.field
        self.schema = context.field.interface

    def move(self, pos):
        """ AJAX method to change field position within its schema.
        The position is relative to the fieldset.
        """
        schema = IEditableSchema(self.schema)
        fieldname = self.field.__name__
        pos = int(pos)


        ordered_field_ids = [name for (name, field) in sortedFields(self.schema)]
        for fieldset in self.schema.getTaggedValue(FIELDSETS_KEY):
            # if we are in a fieldset, pos is the position relative to the fieldset
            if fieldname in fieldset.fields:
                old_field_of_position = fieldset.fields[pos]
                absolute_position = ordered_field_ids.index(old_field_of_position)
                break
        else:
            # in default fieldset, the relative position == the absolute position
            fieldset = None
            absolute_position = pos

        schema.moveField(fieldname, absolute_position)
        # if field is in a fieldset, also reorder fieldset tagged value
        ordered_field_ids = [name for (name, field) in sortedFields(self.schema)]
        if fieldset is not None:
            fieldset.fields = sorted(fieldset.fields,
                                     key=lambda x: ordered_field_ids.index(x))

        notifyContainerModified(self.schema)
        notify(SchemaModifiedEvent(self.aq_parent.aq_parent))

    def delete(self):
        """
        AJAX method to delete a field
        """
        schema = IEditableSchema(self.schema)
        schema.removeField(self.field.getName())
        notify(ObjectRemovedEvent(self.field, self.schema))
        notify(FieldRemovedEvent(self.aq_parent.aq_parent, self.field))
        self.request.response.setHeader('Content-Type', 'text/html')
