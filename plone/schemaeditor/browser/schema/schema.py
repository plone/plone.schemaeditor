from plone.z3cform.crud import crud
from zope.schema.interfaces import IField
from plone.z3cform import layout
from zope.interface import Interface, implements
from zope.component import getMultiAdapter
from zope import schema
from zope.publisher.browser import BrowserPage
import Acquisition
from Acquisition import aq_parent, aq_inner
from plone.schemaeditor.interfaces import ISchemaEditingContext
from z3c.form import field

class SchemaListing(crud.CrudForm):
    
    view_schema = field.Fields(IField).select('title', 'description')
    addform_factory = crud.NullForm
    
    def __init__(self, context, request):
        super(SchemaListing, self).__init__(context, request)
        self.__name__
    
    def get_items(self):
        schema = self.context.schema
        return [(name, schema[name]) for name in schema.names()]
        
    def add(self, data):
        return None
        
    def remove(self, (id, item)):
        return None
        
    def link(self, item, field):
        if field == 'title':
            return '%s/%s' % (self.context.absolute_url(), item.__name__)
        else:
            return None

SchemaListingPage = layout.wrap_form(SchemaListing)

class SchemaListingContext(Acquisition.Implicit, BrowserPage):
    implements(ISchemaEditingContext)
    
    __allow_access_to_unprotected_subobjects__ = 1
    
    def __init__(self, context, request):
        super(SchemaListingContext, self).__init__(context, request)
        self.schema = context
    
    def publishTraverse(self, traverse, name):
        return getMultiAdapter((self.schema[name], self.request), name=u'field').__of__(self)
    
    def browserDefault(self, request):
        return self, ('@@edit',)

    def absolute_url(self):
        parent_url = aq_parent(aq_inner(self)).absolute_url()
        return "%s/%s" % (parent_url, self.__name__)
