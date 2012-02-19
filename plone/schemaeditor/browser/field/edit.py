from Acquisition import aq_parent, aq_inner

from zope.interface import implements, Interface
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import adapts
from zope.event import notify
from zope.schema.interfaces import IField
from zope import schema
from zope.i18nmessageid import MessageFactory

from z3c.form import form, field, button
from plone.z3cform import layout

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

class FieldEditForm(form.EditForm):
    implements(IFieldEditForm)

    def __init__(self, context, request):
        super(form.EditForm, self).__init__(context, request)
        self.field = context.field

    def getContent(self):
        return self.field

    @lazy_property
    def schema(self):
        return interfaces.IFieldEditFormSchema(self.field)

    @lazy_property
    def fields(self):
        # use a custom 'title' field to make sure it is required
        fields = field.Fields(IFieldTitle)

        # omit the order attribute since it's managed elsewhere
        fields += field.Fields(self.schema).omit(
            'order', 'title', 'default', 'missing_value', 'readonly')
        return fields

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
        return _(u"Edit Field '${fieldname}'", mapping={'fieldname': self.field.__name__})
