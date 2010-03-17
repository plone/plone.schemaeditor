from zope.component import getUtilitiesFor
from zope.interface import implements
from zope.i18n import translate
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from plone.schemaeditor.interfaces import IFieldFactory
from plone.schemaeditor import SchemaEditorMessageFactory as _

class FieldFactory(object):
    implements(IFieldFactory)
    
    title = u''
    
    def __init__(self, fieldcls, title):
        self.fieldcls = fieldcls
        self.title = title

    def __call__(self, *args, **kw):
        return self.fieldcls(*args, **kw)

def FieldsVocabularyFactory(context):
    field_factories = getUtilitiesFor(IFieldFactory)
    titled_factories = [(translate(factory.title), factory) for (id, factory) in field_factories]
    items = sorted(titled_factories, key=lambda x: x[0])
    return SimpleVocabulary.fromItems(items)

TextLineFactory = FieldFactory(schema.TextLine, _(u'label_textline_field', default=u'Text line (String)'))
TextFactory = FieldFactory(schema.Text, _(u'label_text_field', default=u'Text'))
IntFactory = FieldFactory(schema.Int, _(u'label_integer_field', default=u'Integer'))
FloatFactory = FieldFactory(schema.Float, _(u'label_float_field', default=u'Floating-point number'))
BoolFactory = FieldFactory(schema.Bool, _(u'label_boolean_field', default=u'Boolean'))
PasswordFactory = FieldFactory(schema.Password, _(u'label_password_field', default=u'Password'))
DatetimeFactory = FieldFactory(schema.Datetime, _(u'label_datetime_field', default=u'Date/Time'))
