from Products.Five import BrowserView
from plone.schemaeditor.interfaces import IEditableSchema
from zope.app.container.contained import notifyContainerModified

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
        schema.move_field(fieldname, int(pos))
        notifyContainerModified(self.schema)
