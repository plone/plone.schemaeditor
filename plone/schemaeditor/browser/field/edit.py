from Acquisition import aq_parent, aq_inner
from OFS.SimpleItem import SimpleItem
from ZPublisher.BaseRequest import DefaultPublishTraverse

from zope.interface import implements
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.cachedescriptors import property

from z3c.form import form, field, button
from plone.z3cform import layout

from plone.schemaeditor.interfaces import IFieldContext, IFieldEditForm
from plone.schemaeditor import interfaces

class FieldContext(SimpleItem):
    """ wrapper for published zope 3 schema fields
    """
    implements(IFieldContext, IBrowserPublisher)
    
    def __init__(self, context, request):
        super(FieldContext, self).__init__()
        self.field = context
        self.request = request
        
        # make sure breadcrumbs are correct
        self.id = None
        self.__name__ = self.field.__name__

    def publishTraverse(self, request, name):
        """ It's not valid to traverse to anything below a field context.
        """
        # hack to make inline validation work
        # (plone.app.z3cform doesn't know the form is the default view)
        if name == self.__name__:
            return EditView(self, request).__of__(self)

        return DefaultPublishTraverse(self, request).publishTraverse(request, name)

    def browserDefault(self, request):
        """ Really we want to show the field EditView.
        """
        return self, ('@@edit',)

class FieldEditForm(form.EditForm):
    implements(IFieldEditForm)

    def __init__(self, context, request):
        super(form.EditForm, self).__init__(context, request)
        self.field = context.field
    
    def getContent(self):
        return self.field
    
    @property.Lazy
    def schema(self):
        return interfaces.IFieldEditFormSchema(self.field)
    
    @property.Lazy
    def fields(self):
        # omit the order attribute since it's managed elsewhere
        return field.Fields(self.schema).omit('order')

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

    @property.Lazy
    def label(self):
        return u"Edit Field '%s'" % self.field.__name__
