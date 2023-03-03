from plone.schemaeditor import _
from plone.schemaeditor import interfaces
from plone.schemaeditor import schema as se_schema
from plone.schemaeditor.interfaces import IFieldFactory
from z3c.form import validator
from zope import component
from zope import interface
from zope import schema
from zope.component import getUtilitiesFor
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.schema import interfaces as schema_ifaces
from zope.schema import vocabulary
from zope.schema.vocabulary import SimpleVocabulary

import copy
import operator


@interface.implementer(interfaces.IFieldEditFormSchema)
@component.adapter(schema_ifaces.IField)
def getFirstFieldSchema(field):
    return [
        s for s in field.__provides__.__iro__ if s.isOrExtends(schema_ifaces.IField)
    ][0]


@implementer(IFieldFactory)
class FieldFactory:
    title = ""

    def __init__(self, fieldcls, title, *args, **kw):
        self.fieldcls = fieldcls
        self.title = title
        self.args = args
        self.kw = kw

    def __call__(self, *args, **kw):
        kwargs = copy.deepcopy(self.kw)
        kwargs.update(**kw)
        return self.fieldcls(*(self.args + args), **kwargs)

    def available(self):
        """field is addable in the current context"""
        return True

    def editable(self, field):
        """test whether a given instance of a field is editable"""
        return True

    def protected(self, field):
        """test whether a given instance of a field is protected"""
        return False


def FieldsVocabularyFactory(context):
    request = getRequest()
    field_factories = getUtilitiesFor(IFieldFactory)
    allowedFields = getattr(context, "allowedFields", None)
    if allowedFields is not None:
        field_factories = [
            (id, factory) for id, factory in field_factories if id in allowedFields
        ]
    terms = []
    for field_id, factory in field_factories:
        terms.append(
            SimpleVocabulary.createTerm(
                factory, factory.title, translate(factory.title, context=request)
            )
        )
    terms = sorted(terms, key=operator.attrgetter("title"))
    return SimpleVocabulary(terms)


# TextLineFactory is the default. We need to set that here to avoid a
# circular import.
TextLineFactory = FieldFactory(
    schema.TextLine, _("label_textline_field", default="Text line (String)")
)
interfaces.INewField["factory"].__dict__["default"] = TextLineFactory

TextFactory = FieldFactory(schema.Text, _("label_text_field", default="Text"))
IntFactory = FieldFactory(schema.Int, _("label_integer_field", default="Integer"))
FloatFactory = FieldFactory(
    schema.Float, _("label_float_field", default="Floating-point number")
)
BoolFactory = FieldFactory(schema.Bool, _("label_boolean_field", default="Yes/No"))
PasswordFactory = FieldFactory(
    schema.Password, _("label_password_field", default="Password")
)
DatetimeFactory = FieldFactory(
    schema.Datetime, _("label_datetime_field", default="Date/Time")
)
DateFactory = FieldFactory(schema.Date, _("label_date_field", default="Date"))


@interface.implementer(interfaces.IFieldEditFormSchema)
@component.adapter(schema_ifaces.IChoice)
def getChoiceFieldSchema(field):
    return se_schema.ITextLineChoice


ChoiceFactory = FieldFactory(
    schema.Choice, _("label_choice_field", default="Choice"), values=[]
)


@interface.implementer(se_schema.ITextLineChoice)
@component.adapter(schema_ifaces.IChoice)
class TextLineChoiceField:
    def __init__(self, field):
        self.__dict__["field"] = field

    def __getattr__(self, name):
        if name == "values":
            values = []
            for term in self.field.vocabulary or []:
                if term.value != term.title:
                    values.append(f"{term.value:s}|{term.title:s}")
                else:
                    values.append(term.value)
            return values

        return getattr(self.field, name)

    def _constructVocabulary(self, value):
        terms = []
        if value:
            for item in value:
                if item and "|" in item:
                    voc_value, voc_title = item.split("|", 1)
                else:
                    voc_value = item
                    voc_title = item

                term = vocabulary.SimpleTerm(
                    token=voc_value.encode("unicode_escape"),
                    value=voc_value,
                    title=voc_title,
                )
                terms.append(term)

        return vocabulary.SimpleVocabulary(terms)

    def __setattr__(self, name, value):
        if name == "values" and value:
            vocab = self._constructVocabulary(value)
            return setattr(self.field, "vocabulary", vocab)
        elif name == "values" and not value:
            return

        if name == "vocabularyName" and value:
            setattr(self.field, "values", None)
            setattr(self.field, "vocabulary", None)
            return setattr(self.field, "vocabularyName", value)
        elif name == "vocabularyName" and not value:
            return setattr(self.field, "vocabularyName", None)

        return setattr(self.field, name, value)

    def __delattr__(self, name):
        if name == "values":
            del self.field.vocabulary

        return delattr(self.field, name)


@component.adapter(
    interface.Interface,
    interface.Interface,
    interfaces.IFieldEditForm,
    se_schema.ITextLinesField,
    interface.Interface,
)
class VocabularyValuesValidator(validator.SimpleFieldValidator):

    """Ensure duplicate vocabulary terms are not submitted"""

    def validate(self, values):
        if values is None:
            return super().validate(values)

        by_value = {}
        by_token = {}
        for value in values:
            term = vocabulary.SimpleTerm(
                token=value.encode("unicode_escape"), value=value, title=value
            )
            if term.value in by_value:
                raise interface.Invalid(
                    _(
                        "field_edit_error_conflicting_values",
                        default="The '${value1}' vocabulary value conflicts "
                        "with '${value2}'.",
                        mapping={"value1": value, "value2": by_value[term.value].value},
                    )
                )

            if term.token in by_token:
                raise interface.Invalid(
                    _(
                        "field_edit_error_conflicting_values",
                        default="The '${value1}' vocabulary value conflicts "
                        "with '${value2}'.",
                        mapping={"value1": value, "value2": by_value[term.token].value},
                    )
                )

            by_value[term.value] = term
            by_token[term.token] = term

        return super().validate(values)


class VocabularyNameValidator(validator.SimpleFieldValidator):

    """Ensure user has not submitted a vocabulary values AND a factory"""

    def validate(self, values):
        if values is None:
            return super().validate(values)

        if values and self.request.form.get("form.widgets.values", None):
            raise interface.Invalid(
                _(
                    "field_edit_error_values_and_name",
                    default="You can not set a vocabulary name AND vocabulary "
                    "values. Please clear values field or set no value "
                    "here.",
                )
            )

        return super().validate(values)


validator.WidgetValidatorDiscriminators(
    VocabularyNameValidator, field=se_schema.ITextLineChoice["vocabularyName"]
)


@interface.implementer(interfaces.IFieldEditFormSchema)
@component.adapter(schema_ifaces.ISet)
def getMultiChoiceFieldSchema(field):
    return se_schema.ITextLineChoice


MultiChoiceFactory = FieldFactory(
    schema.Set,
    _("label_multi_choice_field", default="Multiple Choice"),
    value_type=schema.Choice(values=[]),
)


@interface.implementer_only(se_schema.ITextLineChoice)
@component.adapter(schema_ifaces.ISet)
class TextLineMultiChoiceField(TextLineChoiceField):
    def __init__(self, field):
        self.__dict__["field"] = field

    def __getattr__(self, name):
        field = self.field
        if name == "values":
            values = []
            for term in self.field.value_type.vocabulary or []:
                if term.value != term.title:
                    values.append(f"{term.value:s}|{term.title:s}")
                else:
                    values.append(term.value)
            return values
        elif name == "vocabularyName":
            return getattr(field.value_type, name, None) or getattr(field, name)
        else:
            return getattr(field, name)

    def __setattr__(self, name, value):
        if name == "values" and value:
            vocab = self._constructVocabulary(value)
            return setattr(self.field.value_type, "vocabulary", vocab)
        elif name == "values" and not value:
            return

        if name == "vocabularyName" and value:
            setattr(self.field.value_type, "values", None)
            setattr(self.field.value_type, "vocabulary", None)
            setattr(self.field.value_type, "vocabularyName", value)
            return setattr(self.field, "vocabularyName", value)
        elif name == "vocabularyName" and not value:
            setattr(self.field.value_type, "vocabularyName", None)
            return setattr(self.field, "vocabularyName", None)

        return setattr(self.field, name, value)


# make Bool fields use the radio widget by default
@component.adapter(schema_ifaces.IBool, IObjectAddedEvent)
def setBoolWidget(field, event):
    schema = field.interface
    widgets = schema.queryTaggedValue("plone.autoform.widgets", {})
    widgets[field.__name__] = "z3c.form.browser.radio.RadioFieldWidget"
    schema.setTaggedValue("plone.autoform.widgets", widgets)
