from Products.Five import BrowserView
from plone.schemaeditor.interfaces import IEditableSchema
from zope.app.container.contained import notifyContainerModified
from zope.event import notify
from zope.app.container.contained import ObjectRemovedEvent
from plone.schemaeditor.utils import SchemaModifiedEvent


class FieldOrderView(BrowserView):
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.field = context.field
        self.schema = context.field.interface
    
    def move(self, pos):
        """ AJAX method to change field position within its schema.
        """
        
        schema = IEditableSchema(self.schema)
        fieldname = self.field.__name__
        schema.moveField(fieldname, int(pos))
        notifyContainerModified(self.schema)
        notify(SchemaModifiedEvent(self.aq_parent.aq_parent))

    def delete(self):
        """
        AJAX method to delete a field
        """
        schema = IEditableSchema(self.schema)
        schema.removeField(self.field.getName())
        notify(ObjectRemovedEvent(self.field, self.schema))
        notify(SchemaModifiedEvent(self.aq_parent.aq_parent))
        self.request.response.setHeader('Content-Type', 'text/html')
