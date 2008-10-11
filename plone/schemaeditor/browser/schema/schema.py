from plone.z3cform.crud import crud
from zope.schema.interfaces import IField
from plone.z3cform import layout
from zope.interface import Interface, implements
from zope import schema
from zope.publisher.browser import BrowserPage
import Acquisition
from plone.schemaeditor.interfaces import ISchemaEditingContext
    
class SchemaListing(crud.CrudForm):
    
    view_schema = Interface
    addform_factory = crud.NullForm
    
    def __init__(self, context, request):
        super(SchemaListing, self).__init__(context, request)
    
    def get_items(self):
        import pdb; pdb.set_trace( )
        return []
        
    def add(self, data):
        pass
        
    def remove(self, (id, item)):
        pass
        

SchemaListingPage = layout.wrap_form(SchemaListing)

class SchemaListingContext(Acquisition.Implicit, BrowserPage):
    implements(ISchemaEditingContext)
    
    __allow_access_to_unprotected_subobjects__ = 1
    
    def __init__(self, context, request):
        super(SchemaListingContext, self).__init__(context, request)
        self.schema = context
        self.__name__ = self.schema.__class__
    
    def publishTraverse(self, traverse, name):
        #...
        pass
    
    def browserDefault(self, request):
        return self, ('@@edit',)
