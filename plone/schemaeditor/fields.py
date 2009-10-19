from zope.interface import implements
from zope import schema
from interfaces import IFieldFactory
from plone.schemaeditor import SchemaEditorMessageFactory as _

class FieldFactory(object):
    implements(IFieldFactory)
    
    title = u''
    
    def __init__(self, fieldcls, title):
        self.fieldcls = fieldcls
        self.title = title

    def __call__(self, *args, **kw):
        return self.fieldcls(*args, **kw)

TextLineFactory = FieldFactory(schema.TextLine, _(u'label_textline_field', default=u'Text line'))
TextFactory = FieldFactory(schema.Text, _(u'label_text_field', default=u'Text'))
IntFactory = FieldFactory(schema.Int, _(u'label_integer_field', default=u'Integer'))
FloatFactory = FieldFactory(schema.Float, _(u'label_float_field', default=u'Floating-point number'))
BoolFactory = FieldFactory(schema.Bool, _(u'label_boolean_field', default=u'Boolean'))
PasswordFactory = FieldFactory(schema.Password, _(u'label_password_field', default=u'Password'))
DatetimeFactory = FieldFactory(schema.Datetime, _(u'label_datetime_field', default=u'Date/Time'))
