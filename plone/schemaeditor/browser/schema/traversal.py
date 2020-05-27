# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from plone.schemaeditor.browser.field.traversal import FieldContext
from plone.schemaeditor.interfaces import ISchemaContext
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserPublisher
from ZPublisher.BaseRequest import DefaultPublishTraverse


@implementer(ISchemaContext, IBrowserPublisher)
class SchemaContext(SimpleItem):

    """ This is a transient item that allows us to traverse through (a wrapper
        of) a zope 3 schema to (a wrapper of) a zope 3 schema field.
    """

    schemaEditorView = None
    additionalSchemata = ()
    allowedFields = None  # all fields
    fieldsWhichCannotBeDeleted = ()
    enableFieldsets = True

    def __init__(self, context, request, name=u'schema', title=None):
        self.schema = context
        self.request = request

        # make sure absolute_url and breadcrumbs are correct
        self.id = None
        self.__name__ = name
        if title is None:
            title = name
        self.Title = lambda: title

    def publishTraverse(self, request, name):
        """ Look up the field whose name matches the next URL path element,
        and wrap it.
        """
        try:
            return FieldContext(self.schema[name], self.request).__of__(self)
        except KeyError:
            return DefaultPublishTraverse(self, request).publishTraverse(
                request,
                name
            )

    def browserDefault(self, request):
        """ If not traversing through the schema to a field,
        show the SchemaListingPage.
        """
        return self, ('@@edit',)
