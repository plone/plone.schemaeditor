# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from plone.schemaeditor.browser.field.edit import EditView
from plone.schemaeditor.interfaces import IFieldContext
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserPublisher
from ZPublisher.BaseRequest import DefaultPublishTraverse


@implementer(IFieldContext, IBrowserPublisher)
class FieldContext(SimpleItem):

    """ wrapper for published zope 3 schema fields
    """

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

        return DefaultPublishTraverse(self, request).publishTraverse(
            request,
            name,
        )

    def browserDefault(self, request):
        """ Really we want to show the field EditView.
        """
        return self, ('@@edit',)
