from zope.component import queryUtility
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from z3c.form import form, field, button
from plone.z3cform.layout import FormWrapper

from plone.schemaeditor.interfaces import IFieldFactory

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


class ReadOnlySchemaListing(SchemaListing):
    buttons = button.Buttons()
    
    def edit_url(self, field):
        return
    delete_url = edit_url

class SchemaListingPage(FormWrapper):
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
