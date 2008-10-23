import Acquisition
from OFS.SimpleItem import Item

from zope.interface import Interface, implements
from zope.component import provideAdapter, adapts
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.pagetemplate import viewpagetemplatefile
from zope import schema
from zope.schema.interfaces import IField
from zope.event import notify
from zope.app.container.contained import ObjectAddedEvent, ObjectRemovedEvent, ObjectMovedEvent

from z3c.form import field
from plone.z3cform.crud import crud
from plone.z3cform import layout

from plone.schemaeditor.interfaces import ISchemaContext, IEditableSchema
from plone.schemaeditor.browser.field.edit import FieldContext
from plone.schemaeditor.utils import sorted_fields

# We need this interface and adapter so that we can get/set the __name__
# attribute of a schema field.

class IFieldNameSchema(Interface):
    
    __name__ = schema.TextLine(title=u'ID')

class FieldNameAdapter(object):
    adapts(IField)
    implements(IFieldNameSchema)
    
    def __init__(self, field):
        self.field = field
    
    @apply
    def __name__():
        def get(self):
            return getattr(self.field, '__name__', None)
        def set(self, value):
            self.field.__name__ = value
        return property(get, set)
provideAdapter(FieldNameAdapter)


class FieldSubForm(crud.EditSubForm):
#    template = viewpagetemplatefile.ViewPageTemplateFile('schema-row.pt')
    pass


class FieldEditForm(crud.EditForm):
    label = None
#    template = viewpagetemplatefile.ViewPageTemplateFile('schema-table.pt')
    
    editsubform_factory = FieldSubForm

class SchemaListing(crud.CrudForm):
    """ A plone.z3cform CRUD form for editing a zope 3 schema.
    """
    update_schema = IFieldNameSchema
    view_schema = field.Fields(IField).select('title', 'description')
    addform_factory = crud.NullForm
    editform_factory = FieldEditForm
    
    def __init__(self, context, request):
        super(SchemaListing, self).__init__(context, request)
        self.schema = context.schema

    def get_items(self):
        return sorted_fields(self.schema)

    def add(self, data):
        """ Add field to schema
        """
        
        # XXX create the field based on the form data!
        
        schema = IEditableSchema(self.schema)
        schema.add_field(field)
        notify(ObjectAddedEvent(field, self.schema))

    def remove(self, (id, field)):
        """ Remove field from schema
        """
        schema = IEditableSchema(self.schema)
        schema.remove_field(id)
        notify(ObjectRemovedEvent(field, self.schema))

    def before_update(self, field, data):
        """ Handle field renaming
        """
        oldname = field.__name__
        newname = data['__name__']
        if newname != oldname:
            schema = IEditableSchema(self.schema)
            schema.remove_field(oldname)
            schema.add_field(field, name=newname)
            # (You might expect us to update the __name__ attribute on the field
            # also, but the z3c.form update handler will take care of that --
            # and this will ensure that the user sees the correct form status message.)
            notify(ObjectMovedEvent(field, self.schema, oldname, self.schema, newname))

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
