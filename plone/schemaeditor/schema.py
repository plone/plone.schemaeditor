from zope import interface
from zope.schema import interfaces 
from zope import schema

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
    
class IDatetime(interfaces.IDatetime):

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

class IChoice(IChoiceBase, interfaces.IChoice):
    """Fix the IChoice default and missing_value"""

class ITextLinesField(interfaces.IList):
    """A marker for fields which should get the textlines widget"""

class ITextLineChoice(IChoiceBase):
    """A simple choice field with user entered vocabulary values."""

    values = schema.List(
        title=interfaces.IChoice['vocabulary'].title,
        description=interfaces.IChoice['vocabulary'].description,
        required=interfaces.IChoice['vocabulary'].required,
        default=interfaces.IChoice['vocabulary'].default,
        value_type=schema.TextLine())
    interface.alsoProvides(values, ITextLinesField)
