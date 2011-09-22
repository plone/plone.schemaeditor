from Acquisition import aq_parent, aq_inner

from zope.interface import implements, Interface, Invalid
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import adapts
from zope.event import notify
from zope.schema.interfaces import IField, IBool
from zope import schema

from z3c.form import form, field, button
from z3c.form.interfaces import WidgetActionExecutionError
from plone.z3cform import layout

from plone.schemaeditor.interfaces import IFieldEditForm
from plone.schemaeditor import interfaces
from plone.schemaeditor.utils import SchemaModifiedEvent
from plone.schemaeditor import SchemaEditorMessageFactory as _

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
        fields += field.Fields(self.schema).omit('order', 'title', 'missing_value')
        if self.schema.isOrExtends(IBool):
            fields = fields.omit('required')
        return fields
    
    @button.buttonAndHandler(u'Save', name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        
        # For choice fields, make sure default is in the valid values
        if 'values' in data:
            values = data['values'] or []
            if 'default' in data and data['default']:
                default = data['default']
                if type(default) is not list:
                    default = [default]
                for value in default:
                    if value not in values:
                        raise WidgetActionExecutionError('default',
                            Invalid(_(u'Please enter a valid vocabulary value.')))
        
        if errors:
            self.status = self.formErrorsMessage
            return
        
        # clear current min/max to avoid range errors
        if 'min' in data:
            self.field.min = None
        if 'max' in data:
            self.field.max = None

        default = data.pop('default', _marker)
        changes = self.applyChanges(data)
        
        # make sure we can report invalid defaults
        if default is not _marker:
            try:
                changes2 = self.applyChanges({'default': default})
            except schema.ValidationError, e:
                raise WidgetActionExecutionError('default', e)
            else:
                changes = changes or changes2
        
        if changes:
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage

        notify(SchemaModifiedEvent(self.context.aq_parent))
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
