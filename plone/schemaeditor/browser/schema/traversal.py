from zope.interface import implements
from zope.publisher.interfaces.browser import IBrowserPublisher
from ZPublisher.BaseRequest import DefaultPublishTraverse
from OFS.SimpleItem import SimpleItem

from plone.schemaeditor.browser.field.traversal import FieldContext
from plone.schemaeditor.interfaces import ISchemaContext

class SchemaContext(SimpleItem):
    """ This is a transient item that allows us to traverse through (a wrapper
        of) a zope 3 schema to (a wrapper of) a zope 3 schema field.
    """
    # Implementing IBrowserPublisher tells the Zope 2 publish traverser to pay attention
    # to the publishTraverse and browserDefault methods.
    implements(ISchemaContext, IBrowserPublisher)
    
    schemaEditorView = None
    additionalSchemata = ()
    
    def __init__(self, context, request, name=u'schema', title=None):
        super(SchemaContext, self).__init__(context, request)
        self.schema = context
        self.request = request
        
        # make sure absolute_url and breadcrumbs are correct
        self.id = None
        self.__name__ = name
        if title is None:
            title = name
        self.Title = lambda: title
    
    def publishTraverse(self, request, name):
        """ Look up the field whose name matches the next URL path element, and wrap it.
        """
        try:
            return FieldContext(self.schema[name], self.request).__of__(self)
        except KeyError:
            return DefaultPublishTraverse(self, request).publishTraverse(request, name)
    
    def browserDefault(self, request):
        """ If not traversing through the schema to a field, show the SchemaListingPage.
        """
        return self, ('@@edit',)
