# -*- coding: utf-8 -*-
from plone.autoform.form import AutoExtensibleForm
from plone.memoize.instance import memoize
from plone.schemaeditor import _
from plone.schemaeditor.interfaces import IFieldFactory
from plone.schemaeditor.utils import SchemaModifiedEvent
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.z3cform.layout import FormWrapper
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import form
from z3c.form.interfaces import IEditForm
from zope.component import queryUtility
from zope.event import notify
from zope.interface import implementer


try:
    from plone.protect.utils import addTokenToUrl
except ImportError:
    # plone.protect < 3.x, e.g. in Plone 4.3
    addTokenToUrl = None


@implementer(IEditForm)
class SchemaListing(AutoExtensibleForm, form.Form):

    ignoreContext = True
    ignoreRequest = True
    showEmptyGroups = True
    template = ViewPageTemplateFile('schema_listing.pt')
    ignoreRequiredOnExtract = True

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
        field_identifier = u'{0}.{1}'.format(
            field.__module__,
            field.__class__.__name__,
        )
        allowedFields = getattr(self.context, "allowedFields", None)
        if allowedFields is not None:
            if field_identifier not in allowedFields:
                return None
        return queryUtility(IFieldFactory, name=field_identifier)

    def field_type(self, field):
        field_factory = self._field_factory(field)
        if field_factory is not None:
            return field_factory.title
        else:
            return field.__class__.__name__

    def protected_field(self, field):
        field_identifier = u'{0}.{1}'.format(
            field.__module__,
            field.__class__.__name__,
        )
        field_factory = queryUtility(IFieldFactory, name=field_identifier)
        return field_factory and field_factory.protected(field)

    def edit_url(self, field):
        field_factory = self._field_factory(field)
        if field_factory is not None and field_factory.editable(field):
            return '{0}/{1}'.format(
                self.context.absolute_url(),
                field.__name__,
            )

    def can_delete_fieldset(self, fieldset):
        can_delete = False
        if fieldset != self:
            added_fieldsets = self.context.schema.queryTaggedValue(FIELDSETS_KEY, [])
            for custom_fieldset in added_fieldsets:
                if custom_fieldset.__name__ == fieldset.__name__:
                    can_delete = True
                    break
        return can_delete

    def delete_url(self, field):
        if field.__name__ in self.context.fieldsWhichCannotBeDeleted:
            return
        url = '{0}/{1}/@@delete'.format(
            self.context.absolute_url(),
            field.__name__,
        )
        if addTokenToUrl:
            url = addTokenToUrl(url, self.request)
        return url

    @button.buttonAndHandler(
        _(u'Done'),
    )
    def handleDone(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(
        _(u'Save Defaults'),
        condition=lambda form: getattr(form.context, 'showSaveDefaults', True)
    )
    def handleSaveDefaults(self, action):
        for group in self.groups:
            group.ignoreRequiredOnExtract = self.ignoreRequiredOnExtract
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        for widget in self._iterateOverWidgets():
            widget_name = widget.field.getName()
            if (widget.field.interface is self.context.schema and
                    widget_name in data):
                self.context.schema[widget_name].default = data[widget_name]
        notify(SchemaModifiedEvent(self.context))

        # update widgets to take the new defaults into account
        self.updateWidgets()

    def updateActions(self):
        super().updateActions()
        for a in self.actions:
            # ignore validation
            self.actions[a].ignoreRequiredOnValidation = True


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
