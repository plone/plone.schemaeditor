from Acquisition import aq_inner, aq_parent
from OFS.SimpleItem import SimpleItem
from zope.interface import implements, Interface
from zope.publisher.interfaces.browser import IBrowserPublisher
from plone.schemaeditor.browser.schema.schema import SchemaContext
from zope import schema

class IDummySchema(Interface):
    
    field1 = schema.TextLine()
    field2 = schema.TextLine()
    field3 = schema.TextLine()
    field4 = schema.TextLine()
    field5 = schema.TextLine()

class DummySchemaContext(SimpleItem):
    implements(IBrowserPublisher)

    id = None

    def publishTraverse(self, request, name):
        schema_context = self.browserDefault(request)[0]
        return schema_context.publishTraverse(request, name)

    def browserDefault(self, request):
        return SchemaContext(IDummySchema, request, name=u'@@schemaeditor').__of__(aq_parent(aq_inner(self))), ('@@edit',)


def log_event(object, event):
    print '[event: %s on %s]' % (event.__class__.__name__, object.__class__.__name__)
