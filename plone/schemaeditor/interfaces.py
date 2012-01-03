import re
from zope.component.interfaces import IObjectEvent
from zope.interface import Invalid, invariant
from zope.interface.interfaces import Interface, IInterface, Attribute
from zope.publisher.interfaces.browser import IBrowserPage
from zope.schema import Object, TextLine, Text, Choice, ASCIILine
from zope.schema.interfaces import IField
from z3c.form.interfaces import IEditForm
from OFS.interfaces import IItem
from plone.schemaeditor import SchemaEditorMessageFactory as _


class ISchemaView(IBrowserPage):
    """ A publishable view of a zope 3 schema
    """

class ISchemaContext(IItem):
    """ A publishable wrapper of a zope 3 schema
    """

    schema = Object(
        schema = IInterface
        )
    
    schemaEditorView = Attribute("""Name of the schema editor view. Optional.""")
    
    additionalSchemata = Attribute("""Additional schemas that may modify this one.""")

class ISchemaModifiedEvent(IObjectEvent):

    object = Object(
        schema = ISchemaContext
        )

class IFieldContext(IItem):
    """ A publishable wrapper of a zope 3 schema field
    """

    field = Object(
        schema = IField
        )

class IFieldFactory(IField):
    """ A component that instantiates a field when called.
    """
    title = TextLine(title=u'Title')

class IEditableSchema(Interface):
    """ Interface for adding/removing fields to/from a schema.
    """

    def addField(field, name=None):
        """ Add a field to a schema

            If not provided, the field's name will be taken from its __name__ attribute.
        """

    def removeField(name):
        """ Remove a field from a schema
        """

class IFieldEditForm(IEditForm):
    """ Marker interface for field edit forms
    """

class IFieldEditFormSchema(Interface):
    """ The schema describing the form fields for a field.
    """

RESERVED_NAMES = (
    "subject", "format", "language", "creators", "contributors", "rights",
    "effective_date", "expiration_date"
    )

# a letter followed by letters, numbers, or underscore
ID_RE = re.compile(r'^[a-z][\w\d\.]*$')

def isValidFieldName(value):
    if not ID_RE.match(value):
        raise Invalid(_(u'Please use only letters, numbers and the following characters: _.'))
    if value in RESERVED_NAMES:
        raise Invalid(_(u'"${name}" is a reserved field name.', mapping={'name': value}))
    return True


class INewField(Interface):

    title = TextLine(
        title = _(u'Title'),
        required=True
        )

    __name__ = ASCIILine(
        title=_(u'Short Name'),
        description=_(u'Used for programmatic access to the field.'),
        required=True,
        constraint=isValidFieldName,
        )

    description = Text(
        title=_(u'Help Text'),
        description=_(u'Shows up in the form as help text for the field.'),
        required=False
        )

    factory = Choice(
        title=_(u"Field type"),
        vocabulary="Fields",
        required=True,
        # This can't be done yet or we'll create circular import problem.
        # So it will be injected from fields.py
        # default=TextLineFactory,
        )
    
    @invariant
    def checkTitleAndDescriptionTypes(data):
        if data.__name__ is not None and data.factory is not None:
            if data.__name__ == 'title' and data.factory.fieldcls is not TextLine:
                raise Invalid(_(u'The "title" field must be a Text line (string) field.'))
            if data.__name__ == 'description' and data.factory.fieldcls is not Text:
                raise Invalid(_(u'The "description" field must be a Text field.'))
