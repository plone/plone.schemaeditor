from Acquisition import aq_parent, aq_inner

from zope.interface import implements, Interface, declarations
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import adapts, getAdapters
from zope.event import notify
from zope.schema.interfaces import IField
from zope.security.interfaces import ForbiddenAttribute
from zope import schema
from zope.i18nmessageid import Message
from zope.i18nmessageid import MessageFactory

from z3c.form import form, field, button
from z3c.form.interfaces import IDataManager
from z3c.form.datamanager import AttributeField
from plone.z3cform import layout
from plone.autoform.form import AutoExtensibleForm

from plone.schemaeditor.interfaces import IFieldEditForm
from plone.schemaeditor import interfaces
from plone.schemaeditor.utils import SchemaModifiedEvent
from plone.schemaeditor import SchemaEditorMessageFactory as _


PMF = MessageFactory('plone')

_marker = object()


class IFieldTitle(Interface):
    title = schema.TextLine(
        title=schema.interfaces.ITextLine['title'].title,
        description=schema.interfaces.ITextLine['title'].description,
        default=u"",
        required=True,
    )


class FieldTitleAdapter(object):
    implements(IFieldTitle)
    adapts(IField)

    def __init__(self, field):
        self.field = field

    def _read_title(self):
        return self.field.title

    def _write_title(self, value):
        self.field.title = value
    title = property(_read_title, _write_title)


class IFieldProxy(Interface):
    """Marker interface for field being edited by schemaeditor"""


class FieldProxy(object):
    implements(IFieldProxy)

    def __init__(self, context):
        self.__class__ = type(context.__class__.__name__,
                              (self.__class__, context.__class__), {})
        self.__dict__ = context.__dict__

    @property
    def __provides__(self):
        return declarations.Provides(self.__class__)

    __providedBy__ = __provides__


class FieldDataManager(AttributeField):
    implements(IDataManager)
    adapts(IFieldProxy, IField)

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
        if isinstance(old_value, Message) and old_value.default:
            value = Message(unicode(old_value),
                            domain=old_value.domain,
                            default=value,
                            mapping=old_value.mapping)
        elif isinstance(old_value, Message):
            value = Message(value,
                            domain=old_value.domain,
                            mapping=old_value.mapping)
        super(FieldDataManager, self).set(value)


class FieldEditForm(AutoExtensibleForm, form.EditForm):
    implements(IFieldEditForm)
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
        schema_context = self.context.aq_parent
        return [v for k, v in getAdapters((schema_context, self.field),
                                          interfaces.IFieldEditorExtender)]

    def updateFields(self):
        # use a custom 'title' field to make sure it is required
        fields = field.Fields(IFieldTitle)

        # omit the order attribute since it's managed elsewhere
        fields += field.Fields(self._schema).omit(
            'order', 'title', 'default', 'missing_value', 'readonly')
        self.fields = fields

        self.updateFieldsFromSchemata()

    @button.buttonAndHandler(PMF(u'Save'), name='save')
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
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage

        notify(SchemaModifiedEvent(self.context.aq_parent))
        self.redirectToParent()

    @button.buttonAndHandler(PMF(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        self.redirectToParent()

    def redirectToParent(self):
        parent = aq_parent(aq_inner(self.context))
        url = parent.absolute_url()
        if hasattr(parent, 'schemaEditorView') and parent.schemaEditorView:
            url += '/@@' + parent.schemaEditorView

        self.request.response.redirect(url)


# form wrapper to use Plone form template
class EditView(layout.FormWrapper):
    form = FieldEditForm

    def __init__(self, context, request):
        super(EditView, self).__init__(context, request)
        self.field = context.field

    @lazy_property
    def label(self):
        return _(u"Edit Field '${fieldname}'",
                 mapping={'fieldname': self.field.__name__})
