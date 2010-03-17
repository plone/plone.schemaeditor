from zope import interface
from zope.interface import implements
from zope import schema
from zope.schema import interfaces as schema_ifaces
from zope.schema.vocabulary import SimpleVocabulary
from interfaces import IFieldFactory
from plone.schemaeditor import SchemaEditorMessageFactory as _

from plone.schemaeditor import interfaces
from plone.schemaeditor import schema as se_schema
from zope import component

@interface.implementer(interfaces.IFieldEditFormSchema)
@component.adapter(schema_ifaces.IField)
def getFirstFieldSchema(field):
    return [s for s in field.__provides__.__iro__ if
            s.isOrExtends(schema_ifaces.IField)][0]

class FieldFactory(object):
    implements(IFieldFactory)
    
    title = u''
    
    def __init__(self, fieldcls, title, *args, **kw):
        self.fieldcls = fieldcls
        self.title = title
        self.args = args
        self.kw = kw

    def __call__(self, *args, **kw):
        kwargs = self.kw.copy()
        kwargs.update(**kw)
        return self.fieldcls(*(self.args+args), **kwargs)

TextLineFactory = FieldFactory(schema.TextLine, _(u'label_textline_field', default=u'Text line (String)'))
TextFactory = FieldFactory(schema.Text, _(u'label_text_field', default=u'Text'))
IntFactory = FieldFactory(schema.Int, _(u'label_integer_field', default=u'Integer'))
FloatFactory = FieldFactory(schema.Float, _(u'label_float_field', default=u'Floating-point number'))
BoolFactory = FieldFactory(schema.Bool, _(u'label_boolean_field', default=u'Boolean'))
PasswordFactory = FieldFactory(schema.Password, _(u'label_password_field', default=u'Password'))
DatetimeFactory = FieldFactory(schema.Datetime, _(u'label_datetime_field', default=u'Date/Time'))

@interface.implementer(interfaces.IFieldEditFormSchema)
@component.adapter(schema_ifaces.IChoice)
def getChoiceFieldSchema(field):
    return se_schema.ITextLineChoice

ChoiceFactory = FieldFactory(
    schema.Choice, _(u'label_choice_field', default=u'Choice'),
    values=[])

class TextLineChoiceField(object):
    interface.implements(se_schema.ITextLineChoice)
    component.adapts(schema_ifaces.IChoice)

    def __init__(self, field):
        self.__dict__['field'] = field

    def __getattr__(self, name):
        if name == 'values':
            return [term.value for term in self.field.vocabulary]
        return getattr(self.field, name)

    def __setattr__(self, name, value):
        if name == 'values':
            self.field.vocabulary = SimpleVocabulary.fromValues(
                value)
        return setattr(self.field, name, value)

    def __delattr__(self, name):
        if name == 'values':
            del self.field.vocabulary
        return delattr(self.field, name)
