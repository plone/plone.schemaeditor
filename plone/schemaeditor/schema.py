from zope import interface
from zope.schema import interfaces 
from zope import schema

try:
    from collective.z3cform.datetimewidget.interfaces import (
        IDatetimeField as IDatetime)
    IDatetime # pyflakes
except ImportError:
    IDatetime = interfaces.IDatetime

from plone.schemaeditor import SchemaEditorMessageFactory as _

class IText(interfaces.IText):

    default = schema.Text(
        title=interfaces.IText['default'].title,
        description=interfaces.IText['default'].description,
        required=False)

    missing_value = schema.Text(
        title=interfaces.IText['missing_value'].title,
        description=interfaces.IText['missing_value'].description,
        required=False)

class ITextLine(interfaces.ITextLine):

    default = schema.TextLine(
        title=interfaces.ITextLine['default'].title,
        description=interfaces.ITextLine['default'].description,
        required=False)

    missing_value = schema.TextLine(
        title=interfaces.ITextLine['missing_value'].title,
        description=interfaces.ITextLine['missing_value'].description,
        required=False)

class IBool(interfaces.IBool, interfaces.IFromUnicode):

    default = schema.Bool(
        title=interfaces.IBool['default'].title,
        description=interfaces.IBool['default'].description,
        required=False)

    missing_value = schema.Bool(
        title=interfaces.IBool['missing_value'].title,
        description=interfaces.IBool['missing_value'].description,
        required=False)

class IInt(interfaces.IInt):

    default = schema.Int(
        title=interfaces.IInt['default'].title,
        description=interfaces.IInt['default'].description,
        required=False)

    missing_value = schema.Int(
        title=interfaces.IInt['missing_value'].title,
        description=interfaces.IInt['missing_value'].description,
        required=False)

class IPassword(interfaces.IPassword):

    default = schema.Password(
        title=interfaces.IPassword['default'].title,
        description=interfaces.IPassword['default'].description,
        required=False)

    missing_value = schema.Password(
        title=interfaces.IPassword['missing_value'].title,
        description=interfaces.IPassword['missing_value'].description,
        required=False)

class IFloat(interfaces.IFloat, interfaces.IFromUnicode):

    default = schema.Float(
        title=interfaces.IFloat['default'].title,
        description=interfaces.IFloat['default'].description,
        required=False)

    missing_value = schema.Float(
        title=interfaces.IFloat['missing_value'].title,
        description=interfaces.IFloat['missing_value'].description,
        required=False)

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

    default = schema.Datetime(
        title=interfaces.IDatetime['default'].title,
        description=interfaces.IDatetime['default'].description,
        required=False)

    missing_value = schema.Datetime(
        title=interfaces.IDatetime['missing_value'].title,
        description=interfaces.IDatetime['missing_value'].description,
        required=False)

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

class IChoiceBase(interfaces.IField):

    default = schema.Choice(
        title=interfaces.IChoice['default'].title,
        description=interfaces.IChoice['default'].description,
        required=False,
        values=[])

    missing_value = schema.Choice(
        title=interfaces.IChoice['missing_value'].title,
        description=interfaces.IChoice['missing_value'].description,
        required=False,
        values=[])

class IChoice(IChoiceBase, interfaces.IChoice,
              interfaces.IFromUnicode):
    """Fix the IChoice default and missing_value"""

class ITextLinesField(interfaces.IList):
    """A marker for fields which should get the textlines widget"""

class ITextLineChoiceBase(interfaces.IField):

    values = schema.List(
        title=interfaces.IChoice['vocabulary'].title,
        description=_(u'Enter vocabulary values one per line.'),
        required=interfaces.IChoice['vocabulary'].required,
        default=interfaces.IChoice['vocabulary'].default,
        value_type=schema.TextLine())
    interface.alsoProvides(values, ITextLinesField)

class ITextLineChoice(IChoiceBase, ITextLineChoiceBase):
    """A simple choice field with user entered vocabulary values."""

    default = schema.TextLine(
        title=interfaces.IChoice['default'].title,
        description=interfaces.IChoice['default'].description,
        required=False)

    missing_value = schema.TextLine(
        title=interfaces.IChoice['missing_value'].title,
        description=interfaces.IChoice['missing_value'].description,
        required=False)

class IListBase(interfaces.IField):

    default = schema.List(
        title=interfaces.IList['default'].title,
        description=interfaces.IList['default'].description,
        required=False)

    missing_value = schema.List(
        title=interfaces.IList['missing_value'].title,
        description=interfaces.IList['missing_value'].description,
        required=False)

class IList(IListBase, interfaces.IList):
    """Fix the IList default and missing_value"""

class ITextLineMultiChoice(IListBase, ITextLineChoiceBase):
    """
    A multuple choice field with user entered vocabulary values.
    """

    default = schema.List(
        title=interfaces.IList['default'].title,
        description=interfaces.IList['default'].description,
        required=False,
        value_type=schema.TextLine())
    interface.alsoProvides(default, ITextLinesField)

    missing_value = schema.List(
        title=interfaces.IList['missing_value'].title,
        description=interfaces.IList['missing_value'].description,
        required=False,
        value_type=schema.TextLine())
    interface.alsoProvides(missing_value, ITextLinesField)
