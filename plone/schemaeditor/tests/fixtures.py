from zope.interface import Interface
from zope import schema
from plone.schemaeditor.browser.schema.traversal import SchemaContext

class IDummySchema(Interface):
    
    field1 = schema.TextLine()
    field2 = schema.TextLine()
    field3 = schema.TextLine()
    field4 = schema.TextLine()
    field5 = schema.TextLine()

class DummySchemaContext(SchemaContext):
    def __init__(self, context, request):
        super(DummySchemaContext, self).__init__(IDummySchema, request, name='@@schemaeditor')

def log_event(object, event):
    print '[event: %s on %s]' % (event.__class__.__name__, object.__class__.__name__)

from z3c.form import form, field
from plone.z3cform import layout

class EditForm(form.EditForm):

    ignoreContext = True
    ignoreRequest = True

    def update(self):
        self.fields = field.Fields(IDummySchema)
        super(EditForm, self).update()

EditView = layout.wrap_form(EditForm)
