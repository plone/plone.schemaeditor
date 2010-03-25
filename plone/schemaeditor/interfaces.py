from zope.interface.interfaces import Interface, IInterface
from zope.publisher.interfaces.browser import IBrowserPage
from zope.schema import Object, TextLine, Text, Choice, ASCIILine
from zope.schema.interfaces import IField
from z3c.form.interfaces import IEditForm
from OFS.interfaces import IItem

class ISchemaView(IBrowserPage):
    """ A publishable view of a zope 3 schema
    """

class ISchemaContext(IItem):
    """ A publishable wrapper of a zope 3 schema
    """

    schema = Object(
        schema = IInterface
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

class INewField(Interface):

    title = TextLine(
        title = u'Title',
        required=True
        )
    
    __name__ = ASCIILine(
        title = u'Short Name',
        description = u'Used for programmatic access to the field.',
        required=True,
        )

    description = Text(
        title = u'Help Text',
        description=u'Shows up in the form as help text for the field.',
        required=False
        )

    factory = Choice(
        title=u"Field type",
        vocabulary="Fields",
        required=True
        )
