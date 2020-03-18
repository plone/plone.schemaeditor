# -*- coding: utf-8 -*-
from plone.app.z3cform.interfaces import IDateField
from plone.app.z3cform.interfaces import IDatetimeField
from plone.schemaeditor import _
from zope import schema
from zope.interface import alsoProvides
from zope.schema import interfaces


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


class IDatetime(IDatetimeField):

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


class IDate(IDateField):

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


class IChoice(interfaces.IChoice, interfaces.IFromUnicode):
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
    alsoProvides(values, ITextLinesField)

    vocabularyName = schema.Choice(
        title=interfaces.IChoice['vocabularyName'].title,
        description=interfaces.IChoice['vocabularyName'].description,
        default=interfaces.IChoice['vocabularyName'].default,
        required=False,
        vocabulary='plone.schemaeditor.VocabulariesVocabulary',
    )
