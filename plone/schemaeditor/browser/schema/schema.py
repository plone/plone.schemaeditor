import Acquisition
from Acquisition import aq_parent, aq_inner
from OFS.SimpleItem import Item

from zope.interface import Interface, implements
from zope.component import getMultiAdapter
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.pagetemplate import viewpagetemplatefile
from zope.schema.interfaces import IField
from zope.schema import getFieldsInOrder

from z3c.form import field
from plone.z3cform.crud import crud
from plone.z3cform import layout

from plone.schemaeditor.interfaces import ISchemaContext
from plone.schemaeditor.browser.field.edit import FieldContext


class FieldSubForm(crud.EditSubForm):
    template = viewpagetemplatefile.ViewPageTemplateFile('schema-row.pt')


class FieldEditForm(crud.EditForm):
    label = None
    template = viewpagetemplatefile.ViewPageTemplateFile('schema-table.pt')
    
    editsubform_factory = FieldSubForm

class SchemaListing(crud.CrudForm):
    """ A plone.z3cform CRUD form for editing a zope 3 schema.
    """
    template = viewpagetemplatefile.ViewPageTemplateFile('schema-master.pt')
    
    view_schema = field.Fields(IField).select('title', 'description')
    addform_factory = crud.NullForm
    editform_factory = FieldEditForm
    
    def __init__(self, context, request):
        super(SchemaListing, self).__init__(context, request)
    
    def get_items(self):
        return getFieldsInOrder(self.context.schema)
        
    def add(self, data):
        return None
        # XXX implement me
        
    def remove(self, (id, item)):
        return None
        # XXX implement me
        
    def link(self, item, field):
        """ Generate a link to the edit page for each field.
        """
        if field == 'title':
            return '%s/%s' % (self.context.absolute_url(), item.__name__)
        else:
            return None

class SchemaListingPage(layout.FormWrapper):
    """ Form wrapper so we can get a form with layout.
    
        We define an explicit subclass rather than using the wrap_form method
        from plone.z3cform.layout so that we can inject the schema name into
        the form label.
    """
    form = SchemaListing
    
    @property
    def label(self):
        return u'Edit %s' % self.context.__name__

class SchemaContext(Item, Acquisition.Implicit):
    """ This is a transient item that allows us to traverse through (a wrapper of) a zope 3 schema
        to (a wrapper of) a zope 3 schema field.
    """
    # Implementing IBrowserPublisher tells the Zope 2 traverser to pay attention
    # to the publishTraverse and browserDefault methods.
    implements(ISchemaContext, IBrowserPublisher)
    
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
    
    def publishTraverse(self, traverse, name):
        """ Look up the field whose name matches the next URL path element, and wrap it.
        """
        return FieldContext(self.schema[name], self.request).__of__(self)
    
    def browserDefault(self, request):
        """ If not traversing through the schema to a field, show the SchemaListingPage.
        """
        return self, ('@@edit',)
