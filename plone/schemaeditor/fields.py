from zope.component import getGlobalSiteManager
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

def register_field_factory(fieldcls, title):
    factory = FieldFactory(fieldcls, title)
    factory_name = "%s.%s" % (fieldcls.__module__, fieldcls.__name__)

    gsm = getGlobalSiteManager()
    gsm.registerUtility(factory, provided=IFieldFactory, name=factory_name)

register_field_factory(schema.TextLine, _(u'label_textline_field', default=u'Text line'))
register_field_factory(schema.Text, _(u'label_text_field', default=u'Text'))
register_field_factory(schema.Int, _(u'label_integer_field', default=u'Integer'))
register_field_factory(schema.Float, _(u'label_float_field', default=u'Floating-point number'))
register_field_factory(schema.Bool, _(u'label_boolean_field', default=u'Boolean'))
register_field_factory(schema.Password, _(u'label_password_field', default=u'Password'))
#register_field_factory(schema.Bytes, _(u'label_file_field', default=u'File'))
register_field_factory(schema.Datetime, _(u'label_datetime_field', default=u'Date/Time'))
