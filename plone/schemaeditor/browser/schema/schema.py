from OFS.SimpleItem import SimpleItem

from zope.interface import implements
from zope.component import queryUtility
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from z3c.form import form, field, button

from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor.interfaces import ISchemaContext, IFieldFactory
from plone.schemaeditor.browser.field.edit import FieldContext
from plone.schemaeditor.browser.jsform.jsform import JavascriptFormWrapper

class SchemaListing(form.Form):
    ignoreContext = True
    ignoreRequest = True
    template = ViewPageTemplateFile('schema_listing.pt')
    
    @property
    def fields(self):
        return field.Fields(self.context.schema)
    
    def updateWidgets(self):
        super(SchemaListing, self).updateWidgets()
        for widget in self.widgets.values():
            widget.disabled = 'disabled'
    
    def edit_url(self, field):
        field_identifier = u'%s.%s' % (field.__module__, field.__class__.__name__)
        field_factory = queryUtility(IFieldFactory, name=field_identifier)
        if field_factory is not None:
            return '%s/%s' % (self.context.absolute_url(), field.__name__)
    
    def delete_url(self, field):
        return '%s/%s/@@delete' % (self.context.absolute_url(), field.__name__)
    
    @button.buttonAndHandler(_(u"Add Field"))
    def handleAddField(self, action):
        url = self.context.absolute_url() + '/@@add-field'
        self.request.response.redirect(url)

class ReadOnlySchemaListing(SchemaListing):
    buttons = button.Buttons()
    
    def edit_url(self, field):
        return
    delete_url = edit_url

class SchemaListingPage(JavascriptFormWrapper):
    """ Form wrapper so we can get a form with layout.
    
        We define an explicit subclass rather than using the wrap_form method
        from plone.z3cform.layout so that we can inject the schema name into
        the form label.
    """
    form = SchemaListing
    
    @property
    def label(self):
        if self.context.Title() != self.context.__name__:
            return u'Edit %s (%s)' % (self.context.Title(), self.context.__name__)
        else:
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
