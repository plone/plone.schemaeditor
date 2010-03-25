from Acquisition import aq_parent, aq_inner

from zope.interface import implements, Interface
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import adapts
from zope.schema.interfaces import IField, IBool
from zope import schema

from z3c.form import form, field, button
from plone.z3cform import layout

from plone.schemaeditor.interfaces import IFieldEditForm
from plone.schemaeditor import interfaces

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
        fields += field.Fields(self.schema).omit('order', 'title')
        if self.schema.isOrExtends(IBool):
            fields = fields.omit('required', 'missing_value')
        return fields
    
    @button.buttonAndHandler(u'Save', name='save')
    def handleSave(self, action):
        self.handleApply(self, action)
        if self.status != self.formErrorsMessage:
            self.redirectToParent()

    @button.buttonAndHandler(u'Cancel', name='cancel')
    def handleCancel(self, action):
        self.redirectToParent()
    
    def redirectToParent(self):
        self.request.response.redirect(aq_parent(aq_inner(self.context)).absolute_url())

# form wrapper to use Plone form template
class EditView(layout.FormWrapper):
    form = FieldEditForm

    def __init__(self, context, request):
        super(EditView, self).__init__(context, request)
        self.field = context.field

    @lazy_property
    def label(self):
        return u"Edit Field '%s'" % self.field.__name__
