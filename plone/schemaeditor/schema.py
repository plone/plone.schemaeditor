from zope import interface
from zope.schema import interfaces 
from zope import schema

try:
    from plone.app.z3cform.widget import IDatetimeField as IDatetime
    from plone.app.z3cform.widget import IDateField as IDate
    IDatetime, IDate # pyflakes
except ImportError:
    try:
        from collective.z3cform.datetimewidget.interfaces import (
                IDatetimeField as IDatetime)
        from collective.z3cform.datetimewidget.interfaces import (
                IDateField as IDate)
        IDatetime, IDate # pyflakes
    except ImportError:
        IDatetime = interfaces.IDatetime
        IDate = interfaces.IDate

from plone.schemaeditor import SchemaEditorMessageFactory as _


# get rid of unhelpful help text
interfaces.IMinMaxLen['min_length'].description = u''
interfaces.IMinMaxLen['max_length'].description = u''


# now fix up some of the schemas with missing details

class IBool(interfaces.IBool, interfaces.IFromUnicode):
    pass


class IFloat(interfaces.IFloat, interfaces.IFromUnicode):

    min = schema.Float(
        title=interfaces.IFloat['min'].title,
        required=interfaces.IFloat['min'].required,
        default=interfaces.IFloat['min'].default,
        )

    max = schema.Float(
        title=interfaces.IFloat['max'].title,
        required=interfaces.IFloat['max'].required,
        default=interfaces.IFloat['max'].default,
        )
    
class IDatetime(IDatetime):

    min = schema.Datetime(
        title=interfaces.IDatetime['min'].title,
        required=interfaces.IDatetime['min'].required,
        default=interfaces.IDatetime['min'].default,
        )

    max = schema.Datetime(
        title=interfaces.IDatetime['max'].title,
        required=interfaces.IDatetime['max'].required,
        default=interfaces.IDatetime['max'].default,
        )

class IDate(IDate):

    min = schema.Date(
        title=interfaces.IDate['min'].title,
        required=interfaces.IDate['min'].required,
        default=interfaces.IDate['min'].default,
        )

    max = schema.Date(
        title=interfaces.IDate['max'].title,
        required=interfaces.IDate['max'].required,
        default=interfaces.IDate['max'].default,
        )


class IChoice(interfaces.IChoice,
              interfaces.IFromUnicode):
    pass

class ITextLinesField(interfaces.IList):
    """A marker for fields which should get the textlines widget"""

class ITextLineChoice(interfaces.IField):

    values = schema.List(
        title=_(u'Possible values'),
        description=_(u'Enter allowed choices one per line.'),
        required=interfaces.IChoice['vocabulary'].required,
        default=interfaces.IChoice['vocabulary'].default,
        value_type=schema.TextLine())
    interface.alsoProvides(values, ITextLinesField)
