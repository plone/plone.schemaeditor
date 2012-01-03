from zope.component import queryUtility
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.event import notify
from zope.interface import implements
from z3c.form import button, form
from z3c.form.interfaces import IEditForm, DISPLAY_MODE

from plone.z3cform.layout import FormWrapper
from plone.memoize.instance import memoize
from plone.autoform.form import AutoExtensibleForm

from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor.interfaces import IFieldFactory
from plone.schemaeditor.utils import SchemaModifiedEvent


class SchemaListing(AutoExtensibleForm, form.Form):
    implements(IEditForm)
    
    ignoreContext = True
    ignoreRequest = True
    template = ViewPageTemplateFile('schema_listing.pt')

    @property
    def schema(self):
        return self.context.schema

    @property
    def additionalSchemata(self):
        return self.context.additionalSchemata

    def _iterateOverWidgets(self):
        for widget in self.widgets.values():
            yield widget
        for group in self.groups:
            for widget in group.widgets.values():
                yield widget
    
    def render(self):
        for widget in self._iterateOverWidgets():
            # disable fields from behaviors
            if widget.field.interface is not self.context.schema:
                widget.disabled = 'disabled'

            # limit size of the preview for text areas
            if hasattr(widget, 'rows'):
                if widget.rows is None or widget.rows > 5:
                    widget.rows = 5

        return super(SchemaListing, self).render()

    @memoize
    def _field_factory(self, field):
        field_identifier = u'%s.%s' % (field.__module__, field.__class__.__name__)
        return queryUtility(IFieldFactory, name=field_identifier)

    def field_type(self, field):
        field_factory = self._field_factory(field)
        if field_factory is not None:
            return field_factory.title
        else:
            return field.__class__.__name__

    def edit_url(self, field):
        field_factory = self._field_factory(field)
        if field_factory is not None:
            return '%s/%s' % (self.context.absolute_url(), field.__name__)

    def delete_url(self, field):
        return '%s/%s/@@delete' % (self.context.absolute_url(), field.__name__)

    @button.buttonAndHandler(_(u'Save Defaults'))
    def handleSaveDefaults(self, action):
        # ignore fields from behaviors by setting their widgets' modes
        # to the display mode while we extract the form values (hack!)
        widget_modes = {}
        for widget in self._iterateOverWidgets():
            if widget.field.interface is not self.context.schema:
                widget_modes[widget] = widget.mode
                widget.mode = DISPLAY_MODE
        
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        for fname, value in data.items():
            self.context.schema[fname].default = value
        notify(SchemaModifiedEvent(self.context))

        # restore the actual widget modes so they render a preview
        for widget, mode in widget_modes.items():
            widget.mode = mode
        
        # update widgets to take the new defaults into account
        self.updateWidgets()


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
            return _(u'Edit ${title} (${name})',
                     mapping={'title': self.context.Title(),
                              'name': self.context.__name__})
        else:
            return _(u'Edit ${name}', mapping={'name': self.context.__name__})
