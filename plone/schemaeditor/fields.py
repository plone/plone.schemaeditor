import copy
from zope import interface
from zope import component
from zope.component import adapter
from zope.component import getUtilitiesFor
from zope.interface import implements
from zope.i18n import translate
from zope import schema
from zope.schema import interfaces as schema_ifaces
from zope.schema import vocabulary
from zope.schema.vocabulary import SimpleVocabulary
from zope.lifecycleevent.interfaces import IObjectAddedEvent

from z3c.form import validator

from plone.schemaeditor.interfaces import IFieldFactory
from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor import interfaces
from plone.schemaeditor import schema as se_schema


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
        kwargs = copy.deepcopy(self.kw)
        kwargs.update(**kw)
        return self.fieldcls(*(self.args+args), **kwargs)


def FieldsVocabularyFactory(context):
    field_factories = getUtilitiesFor(IFieldFactory)
    terms = []
    for (field_id, factory) in field_factories:
        terms.append(SimpleVocabulary.createTerm(factory, translate(factory.title), factory.title))

    return SimpleVocabulary(terms)


# TextLineFactory is the default. We need to set that here to avoid a circular import.
TextLineFactory = FieldFactory(schema.TextLine, _(u'label_textline_field', default=u'Text line (String)'))
interfaces.INewField['factory'].__dict__['default'] = TextLineFactory

TextFactory = FieldFactory(schema.Text, _(u'label_text_field', default=u'Text'))
IntFactory = FieldFactory(schema.Int, _(u'label_integer_field', default=u'Integer'))
FloatFactory = FieldFactory(schema.Float, _(u'label_float_field', default=u'Floating-point number'))
BoolFactory = FieldFactory(schema.Bool, _(u'label_boolean_field', default=u'Yes/No'))
PasswordFactory = FieldFactory(schema.Password, _(u'label_password_field', default=u'Password'))
DatetimeFactory = FieldFactory(schema.Datetime, _(u'label_datetime_field', default=u'Date/Time'))
DateFactory = FieldFactory(schema.Date, _(u'label_date_field', default=u'Date'))


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
            return [term.value for term in (self.field.vocabulary or [])]

        return getattr(self.field, name)

    def _constructVocabulary(self, value):
        terms = []
        if value:
            for value in value:
                term = vocabulary.SimpleTerm(
                    token=value.encode('unicode_escape'),
                    value=value, title=value)
                terms.append(term)

        return vocabulary.SimpleVocabulary(terms)

    def __setattr__(self, name, value):
        if name == 'values' and value:
            vocab = self._constructVocabulary(value)
            return setattr(self.field, 'vocabulary', vocab)
        elif name == 'values' and not value:
            return

        if name == 'vocabularyName' and value:
            setattr(self.field, 'values', None)
            setattr(self.field, 'vocabulary', None)
            return setattr(self.field, 'vocabularyName', value)
        elif  name == 'vocabularyName' and not value:
            return setattr(self.field, 'vocabularyName', None)

        return setattr(self.field, name, value)

    def __delattr__(self, name):
        if name == 'values':
            del self.field.vocabulary

        return delattr(self.field, name)


class VocabularyValuesValidator(validator.SimpleFieldValidator):
    """Ensure duplicate vocabulary terms are not submitted
    """
    component.adapts(interface.Interface, interface.Interface,
                     interfaces.IFieldEditForm,
                     se_schema.ITextLinesField, interface.Interface)

    def validate(self, values):
        if values is None:
            return super(VocabularyValuesValidator, self).validate(
                values)

        by_value = {}
        by_token = {}
        for value in values:
            term = vocabulary.SimpleTerm(token=value.encode('unicode_escape'),
                                         value=value, title=value)
            if term.value in by_value:
                raise interface.Invalid(
                    _('field_edit_error_conflicting_values',
                      default=u"The '${value1}' vocabulary value conflicts with '${value2}'.",
                      mapping={'value1': value,
                               'value2': by_value[term.value].value}))

            if term.token in by_token:
                raise interface.Invalid(
                    _('field_edit_error_conflicting_values',
                      default=u"The '${value1}' vocabulary value conflicts with '${value2}'.",
                      mapping={'value1': value,
                               'value2': by_value[term.token].value}))

            by_value[term.value] = term
            by_token[term.token] = term

        return super(VocabularyValuesValidator, self).validate(values)


class VocabularyNameValidator(validator.SimpleFieldValidator):
    """Ensure user has not submitted a vocabulary values AND a factory
    """

    def validate(self, values):
        if values is None:
            return super(VocabularyNameValidator, self).validate(
                values)

        if values and self.request.form.get('form.widgets.values', None):
            raise interface.Invalid(
                _('field_edit_error_values_and_name',
                  default=u"You can't set a vocabulary name AND vocabulary values. "
                          u"Please clear values field or set no value here."))

        return super(VocabularyNameValidator, self).validate(values)

validator.WidgetValidatorDiscriminators(
                            VocabularyNameValidator,
                            field=se_schema.ITextLineChoice['vocabularyName'])


@interface.implementer(interfaces.IFieldEditFormSchema)
@component.adapter(schema_ifaces.ISet)
def getMultiChoiceFieldSchema(field):
    return se_schema.ITextLineChoice


MultiChoiceFactory = FieldFactory(
    schema.Set,
    _(u'label_multi_choice_field', default=u'Multiple Choice'),
    value_type=schema.Choice(values=[]))


class TextLineMultiChoiceField(TextLineChoiceField):
    interface.implementsOnly(se_schema.ITextLineChoice)
    component.adapts(schema_ifaces.ISet)

    def __init__(self, field):
        self.__dict__['field'] = field

    def __getattr__(self, name):
        if name == 'values':
            return [term.value
                    for term in (self.field.value_type.vocabulary or [])]

        return getattr(self.field, name)

    def __setattr__(self, name, value):
        if name == 'values' and value:
            vocab = self._constructVocabulary(value)
            return setattr(self.field.value_type, 'vocabulary', vocab)
        elif name == 'values' and not value:
            return

        if name == 'vocabularyName' and value:
            setattr(self.field.value_type, 'values', None)
            setattr(self.field.value_type, 'vocabulary', None)
            setattr(self.field.value_type, 'vocabularyName', value)
            return setattr(self.field, 'vocabularyName', value)
        elif name == 'vocabularyName' and not value:
            setattr(self.field.value_type, 'vocabularyName', None)
            return setattr(self.field, 'vocabularyName', None)

        return setattr(self.field, name, value)


# make Bool fields use the radio widget by default
@adapter(schema_ifaces.IBool, IObjectAddedEvent)
def setBoolWidget(field, event):
    schema = field.interface
    widgets = schema.queryTaggedValue('plone.autoform.widgets', {})
    widgets[field.__name__] = 'z3c.form.browser.radio.RadioFieldWidget'
    schema.setTaggedValue('plone.autoform.widgets', widgets)

