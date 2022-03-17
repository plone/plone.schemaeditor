# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.autoform.form import AutoExtensibleForm
from plone.schemaeditor import _
from plone.schemaeditor import interfaces
from plone.schemaeditor.interfaces import IFieldEditForm
from plone.schemaeditor.utils import SchemaModifiedEvent
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.datamanager import AttributeField
from z3c.form.interfaces import IDataManager
from zope import schema
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import adapter
from zope.component import getAdapters
from zope.event import notify
from zope.i18nmessageid import Message
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.declarations import getObjectSpecification
from zope.interface.declarations import ObjectSpecificationDescriptor
from zope.schema.interfaces import IField
from zope.security.interfaces import ForbiddenAttribute


import six


_marker = object()


class IFieldTitle(Interface):
    title = schema.TextLine(
        title=schema.interfaces.ITextLine['title'].title,
        description=schema.interfaces.ITextLine['title'].description,
        default=u'',
        required=True,
    )


@implementer(IFieldTitle)
@adapter(IField)
class FieldTitleAdapter(object):

    def __init__(self, field):
        self.field = field

    def _read_title(self):
        return self.field.title

    def _write_title(self, value):
        self.field.title = value
    title = property(_read_title, _write_title)


class IFieldProxy(Interface):
    """Marker interface for field being edited by schemaeditor"""


class FieldProxySpecification(ObjectSpecificationDescriptor):

    def __get__(self, inst, cls=None):
        if inst is None:
            return getObjectSpecification(cls)
        else:
            return inst.__provides__


@implementer(IFieldProxy)
class FieldProxy(object):

    __providedBy__ = FieldProxySpecification()

    def __init__(self, context):
        self.__class__ = type(context.__class__.__name__,
                              (self.__class__, context.__class__), {})
        self.__dict__ = context.__dict__


@implementer(IDataManager)
@adapter(IFieldProxy, IField)
class FieldDataManager(AttributeField):

    def get(self):
        value = super(FieldDataManager, self).get()
        if isinstance(value, Message) and value.default:
            return value.default
        return value

    def set(self, value):
        try:
            old_value = super(FieldDataManager, self).get()
        except (AttributeError, ForbiddenAttribute):
            old_value = None
        if isinstance(old_value, Message):
            value = Message(six.text_type(old_value),
                            domain=old_value.domain,
                            default=value,
                            mapping=old_value.mapping)
        super(FieldDataManager, self).set(value)


@implementer(IFieldEditForm)
class FieldEditForm(AutoExtensibleForm, form.EditForm):
    id = 'edit-field-form'

    def __init__(self, context, request):
        super(form.EditForm, self).__init__(context, request)
        self.field = FieldProxy(context.field)

    def getContent(self):
        return self.field

    # This is a trick: we want autoform to handle the additionalSchemata,
    # but want to provide our own base schema below in updateFields.
    schema = Interface

    @lazy_property
    def _schema(self):
        return interfaces.IFieldEditFormSchema(self.field)

    @lazy_property
    def additionalSchemata(self):
        schema_context = self.context.__parent__
        return [v for k, v in getAdapters((schema_context, self.field),
                                          interfaces.IFieldEditorExtender)]

    @lazy_property
    def label(self):
        return _(u"Edit Field '${fieldname}'",
                 mapping={'fieldname': self.field.__name__})

    def updateFields(self):
        # use a custom 'title' field to make sure it is required
        fields = field.Fields(IFieldTitle)

        # omit the order attribute since it's managed elsewhere
        fields += field.Fields(self._schema).omit(
            'order', 'title', 'default', 'missing_value', 'readonly')
        self.fields = fields

        if "required" in self.fields:
            # XXX somehow the `required` BooleanField is required which
            # should not be
            self.fields["required"].field.required = False

        self.updateFieldsFromSchemata()

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # clear current min/max to avoid range errors
        if 'min' in data:
            self.field.min = None
        if 'max' in data:
            self.field.max = None

        changes = self.applyChanges(data)

        if changes:
            IStatusMessage(self.request).addStatusMessage(
                self.successMessage, type='info')
        else:
            IStatusMessage(self.request).addStatusMessage(
                self.noChangesMessage, type='info')

        notify(SchemaModifiedEvent(self.context.__parent__))

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        self.redirectToParent()

    def redirectToParent(self):
        parent = aq_inner(self.context).__parent__
        url = parent.absolute_url()
        if hasattr(parent, 'schemaEditorView') and parent.schemaEditorView:
            url += '/@@' + parent.schemaEditorView

        self.request.response.redirect(url)


EditView = wrap_form(
    FieldEditForm,
    index=ViewPageTemplateFile('edit.pt')
)
