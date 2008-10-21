import Acquisition
from Acquisition import aq_inner, aq_parent
from OFS.SimpleItem import Item
from zope.interface import implements, Interface
from zope.component import provideAdapter
from zope.publisher.interfaces.browser import IBrowserPublisher, IBrowserRequest
from plone.schemaeditor.browser.schema.schema import SchemaContext
from zope.schema.interfaces import IField

class DummySchemaContext(Item, Acquisition.Implicit):
    implements(IBrowserPublisher)

    id = None

    def publishTraverse(self, request, name):
        schema_context = self.browserDefault(request)[0]
        return schema_context.publishTraverse(request, name)

    def browserDefault(self, request):
        return SchemaContext(IField, request, name=u'@@schemaeditor').__of__(aq_parent(aq_inner(self))), ('@@edit',)
