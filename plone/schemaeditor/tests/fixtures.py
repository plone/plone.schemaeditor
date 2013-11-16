from zope.interface import Interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from plone.schemaeditor.browser.schema.traversal import SchemaContext
from plone.supermodel import model


class IDummySchema(Interface):

    model.fieldset('alpha', fields=['fieldA'])

    field1 = schema.TextLine()
    field2 = schema.TextLine()
    field3 = schema.TextLine()
    field4 = schema.TextLine()
    field5 = schema.TextLine()
    fieldA = schema.TextLine()


class DummySchemaContext(SchemaContext):
    def __init__(self, context, request):
        super(DummySchemaContext, self).__init__(
            IDummySchema, request, name='@@schemaeditor')


def log_event(object, event):
    print '[event: %s on %s]' % (
        event.__class__.__name__, object.__class__.__name__)


from z3c.form import field
from z3c.form.form import EditForm
from plone.z3cform import layout


class EditForm(EditForm):

    ignoreContext = True
    ignoreRequest = True

    def update(self):
        self.fields = field.Fields(IDummySchema)
        super(EditForm, self).update()

EditView = layout.wrap_form(EditForm)


class BaseVocabulary(object):

    def __call__(self, context):
        terms = [SimpleVocabulary.createTerm(
                     value,
                     value,
                     label)
                 for value, label in self.values_list]
        return SimpleVocabulary(terms)


class CountriesVocabulary(BaseVocabulary):

    values_list = [('fr', u'France'),
                   ('uk', u'United Kingdom'),
                   ('es', u'Spain')]


class CategoriesVocabulary(BaseVocabulary):

    values_list = [('php', u'PHP'),
                   ('c', u'C'),
                   ('ruby', u'Ruby')]
