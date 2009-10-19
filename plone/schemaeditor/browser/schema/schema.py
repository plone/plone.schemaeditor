from OFS.SimpleItem import SimpleItem

from zope.interface import Interface, implements
from zope.component import provideAdapter, adapts, queryUtility, getUtilitiesFor, getUtility
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.i18n import translate
from zope import schema
from zope.schema.interfaces import IField
from zope.schema.vocabulary import SimpleVocabulary
from zope.event import notify
from zope.app.container.contained import ObjectAddedEvent, ObjectRemovedEvent, ObjectMovedEvent
from plone.i18n.normalizer.interfaces import IIDNormalizer

from z3c.form import field, button
from plone.z3cform.crud import crud

from plone.schemaeditor.interfaces import ISchemaContext, IFieldFactory, IEditableSchema, IJavascriptForm
from plone.schemaeditor.browser.field.edit import FieldContext
from plone.schemaeditor.browser.jsform.jsform import JavascriptFormWrapper
from plone.schemaeditor.utils import sortedFields

# We need this interface and adapter so that we can get/set the __name__
# attribute of a schema field.

class IFieldNameSchema(Interface):
    
    __name__ = schema.ASCIILine(title=u'ID')

class FieldNameProperty(object):
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
provideAdapter(FieldNameProperty)

def FieldsVocabularyFactory(context):
    field_factories = getUtilitiesFor(IFieldFactory)
    titled_factories = [(translate(factory.title), factory) for (id, factory) in field_factories]
    items = sorted(titled_factories, key=lambda x: x[0])
    return SimpleVocabulary.fromItems(items)

class IFieldFactorySchema(Interface):
    
    title = schema.TextLine(
        title = u'Field title',
        required=True
        )
    
    factory =  schema.Choice(
        title=u"Field type",
        vocabulary="Fields",
        required=True
        )

class FieldSubForm(crud.EditSubForm):
    template = ViewPageTemplateFile('schema-row.pt')
    
    def type_url(self):
        """
        pretty weird to do it this way....  Is there a better way?
        this is how its wrapped: self -> FieldEditForm -> SchemaListing -> SchemaContext
        """
        return self.context.context.context.absolute_url()
    
    def applyChanges(self, data):
        """ Wrapper of the normal applyChanges to tweak the subform id
            if the field was renamed. """
        if '_schemaeditor_newname' in data:
            self.content_id = data['_schemaeditor_newname']
            self.updateWidgets()
            del data['_schemaeditor_newname']
        return super(FieldSubForm, self).applyChanges(data)
    
    @property
    def editable(self):
        # make sure ReadOnlySchemaListings are immutable
        return isinstance(self.context.context, SchemaListing)

class FieldAddForm(crud.AddForm):
    """ Just a normal CRUD add form with a custom template to show a form title.
    """

    label = u'Add Field'
    template = ViewPageTemplateFile('../titledform.pt')

class FieldEditForm(crud.EditForm):
    label = None
    template = ViewPageTemplateFile('schema-table.pt')
    
    editsubform_factory = FieldSubForm

class SchemaListing(crud.CrudForm):
    """ A plone.z3cform CRUD form for editing a zope 3 schema.
    """
    implements(IJavascriptForm)
    
    javascript = ViewPageTemplateFile('schema-js.pt')
    
    label = u'Schema'
    add_schema = IFieldFactorySchema
    update_schema = IFieldNameSchema
    view_schema = field.Fields(IField).select('title', 'description')
    addform_factory = FieldAddForm
    editform_factory = FieldEditForm
    
    def __init__(self, context, request):
        super(SchemaListing, self).__init__(context, request)
        self.schema = context.schema

    def get_items(self):
        return sortedFields(self.schema)

    def add(self, data):
        """ Add field to schema
        """
 
        id = getUtility(IIDNormalizer).normalize(data['title'])
        # XXX validation
        data['__name__'] = id
        factory = data.pop('factory')
        field = factory(**data)
        
        schema = IEditableSchema(self.schema)
        schema.addField(field)
        notify(ObjectAddedEvent(field, self.schema))

    def remove(self, (id, field)):
        """ Remove field from schema
        """
        schema = IEditableSchema(self.schema)
        schema.removeField(id)
        notify(ObjectRemovedEvent(field, self.schema))

    def before_update(self, field, data):
        """ Handle field renaming
        """
        oldname = field.__name__
        newname = data['__name__']
        if newname != oldname:
            schema = IEditableSchema(self.schema)
            schema.removeField(oldname)
            schema.addField(field, name=newname)
            # (You might expect us to update the __name__ attribute on the field
            # also, but the z3c.form update handler will take care of that --
            # and this will ensure that the user sees the correct form status message.)
            notify(ObjectMovedEvent(field, self.schema, oldname, self.schema, newname))
            
            # annotate the data dict so the subform's applyChanges method can
            # tweak the subform's id
            data['_schemaeditor_newname'] = newname

    def link(self, item, field):
        """ Generate a link to the edit page for each field.
        """
        field_identifier = u'%s.%s' % (item.__module__, item.__class__.__name__)
        field_factory = queryUtility(IFieldFactory, name=field_identifier)
        if field == 'title' and field_factory is not None:
            return '%s/%s' % (self.context.absolute_url(), item.__name__)
        else:
            return None

class ReadOnlyFieldEditForm(FieldEditForm):
    buttons = button.Buttons()

class ReadOnlySchemaListing(crud.CrudForm):
    view_schema = field.Fields(IField).select('title', 'description')
    editform_factory = ReadOnlyFieldEditForm
    addform_factory = crud.NullForm
    buttons = button.Buttons()
    
    def __init__(self, context, request):
        super(ReadOnlySchemaListing, self).__init__(context, request)
        self.schema = context.schema

    def get_items(self):
        return sortedFields(self.schema)

class SchemaListingPage(JavascriptFormWrapper):
    """ Form wrapper so we can get a form with layout.
    
        We define an explicit subclass rather than using the wrap_form method
        from plone.z3cform.layout so that we can inject the schema name into
        the form label.
    """
    form = SchemaListing
    
    @property
    def label(self):
        return u'Edit %s' % self.context.__name__

class SchemaContext(SimpleItem):
    """ This is a transient item that allows us to traverse through (a wrapper
        of) a zope 3 schema to (a wrapper of) a zope 3 schema field.
    """
    # Implementing IBrowserPublisher tells the Zope 2 publish traverser to pay attention
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
