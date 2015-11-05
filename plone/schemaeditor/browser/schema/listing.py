from zope.component import queryUtility
from zope.event import notify
from zope.interface import implements
from z3c.form import button, form
from z3c.form.interfaces import IEditForm, DISPLAY_MODE

from plone.z3cform.layout import FormWrapper
from plone.memoize.instance import memoize
from plone.autoform.form import AutoExtensibleForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.schemaeditor import _
from plone.schemaeditor.interfaces import IFieldFactory
from plone.schemaeditor.utils import SchemaModifiedEvent

try:
    from plone.protect.utils import addTokenToUrl
except ImportError:
    # plone.protect < 3.x, e.g. in Plone 4.3
    addTokenToUrl = None



class SchemaListing(AutoExtensibleForm, form.Form):
    implements(IEditForm)

    ignoreContext = True
    ignoreRequest = True
    showEmptyGroups = True
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
        field_identifier = u'%s.%s' % (
            field.__module__, field.__class__.__name__)
        if self.context.allowedFields is not None:
            if field_identifier not in self.context.allowedFields:
                return None
        return queryUtility(IFieldFactory, name=field_identifier)

    def field_type(self, field):
        field_factory = self._field_factory(field)
        if field_factory is not None:
            return field_factory.title
        else:
            return field.__class__.__name__

    def protected_field(self, field):
        field_identifier = u'%s.%s' % (
            field.__module__, field.__class__.__name__)
        field_factory = queryUtility(IFieldFactory, name=field_identifier)
        return field_factory and field_factory.protected(field)

    def edit_url(self, field):
        field_factory = self._field_factory(field)
        if field_factory is not None and field_factory.editable(field):
            return '%s/%s' % (self.context.absolute_url(), field.__name__)

    def delete_url(self, field):

        if field.__name__ in self.context.fieldsWhichCannotBeDeleted:
            return
        url = '%s/%s/@@delete' % (self.context.absolute_url(), field.__name__)
        if addTokenToUrl:
            url = addTokenToUrl(url, self.request)
        return url

    @button.buttonAndHandler(
        _(u'Save Defaults'),
        condition=lambda form: getattr(form.context, 'showSaveDefaults', True)
    )
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
        """ In a dexterity schema editing context, we need to
            construct a label that will specify the field being
            edited. Outside that context (e.g., plone.app.users),
            we should respect the label if specified.
        """

        context_label = getattr(self.context, 'label', None)
        if context_label is not None:
            return context_label
        if self.context.Title() != self.context.__name__:
            return _(u'Edit ${title} (${name})',
                     mapping={'title': self.context.Title(),
                              'name': self.context.__name__})
        else:
            return _(u'Edit ${name}', mapping={'name': self.context.__name__})
