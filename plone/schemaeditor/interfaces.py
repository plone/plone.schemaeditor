# -*- coding: utf-8 -*-
from OFS.interfaces import IItem
from plone.schemaeditor import _
from z3c.form.interfaces import IEditForm
from zope.interface.interfaces import IObjectEvent
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface.interfaces import Attribute
from zope.interface.interfaces import IInterface
from zope.interface.interfaces import Interface
from zope.publisher.interfaces.browser import IBrowserPage
from zope.schema import ASCIILine
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import Int
from zope.schema import Object
from zope.schema import Text
from zope.schema import TextLine
from zope.schema.interfaces import IField

import re


class ISchemaView(IBrowserPage):
    """ A publishable view of a zope 3 schema
    """


class ISchemaContext(IItem):
    """ A publishable wrapper of a zope 3 schema
    """

    schema = Object(
        schema=IInterface
    )

    schemaEditorView = Attribute(
        """Name of the schema editor view. Optional.""")

    additionalSchemata = Attribute(
        """Additional schemas that may modify this one.""")

    allowedFields = Attribute(
        """List of field factory ids that may be added to this schema.
        Or None to allow all fields.
        """)

    fieldsWhichCannotBeDeleted = Attribute(
        """List of field names that may not be deleted from this schema."""
    )

    enableFieldsets = Attribute(
        """Enable extra fieldsets."""
    )


class ISchemaModifiedEvent(IObjectEvent):

    object = Object(
        schema=ISchemaContext
    )


class IFieldContext(IItem):
    """ A publishable wrapper of a zope 3 schema field
    """

    field = Object(
        schema=IField
    )


class IFieldEditorExtender(IInterface):
    """ An additional schema for use when editing a field."""


class IFieldFactory(IField):
    """ A component that instantiates a field when called."""
    title = TextLine(title=u'Title')

    def available(self):
        """ field is addable in the current context """

    def editable(self, field):
        """ test whether a given instance of a field is editable """

    def protected(self, field):
        """ test whether a given instance of a field is protected """


class IEditableSchema(Interface):
    """ Interface for adding/removing fields to/from a schema.
    """

    def addField(field, name=None):
        """ Add a field to a schema

        If not provided, the field's name will be taken from its __name__
        attribute.
        """

    def removeField(field_name):
        """ Remove a field from a schema
        """

    def moveField(field_name, new_pos):
        """ Move a field to the (new_pos)th position in the schema's sort ç
        order (indexed beginning at 0).

        Schema fields are assigned an 'order' attribute that increments for
        each new field instance.
        We shuffle these around in case it matters anywhere that they're
        unique.
        """

    def changeFieldFieldset(field_name, next_fieldset):
        """Move a field from a fieldset to another,
        next_fieldset is a fieldset object, or None for default fieldset
        """


class IFieldEditForm(IEditForm):
    """ Marker interface for field edit forms
    """


class IFieldEditFormSchema(Interface):
    """ The schema describing the form fields for a field.
    """


RESERVED_NAMES = (
    'subject',
    'format',
    'language',
    'creators',
    'contributors',
    'rights',
    'effective_date',
    'expiration_date',
)

# a letter followed by letters, numbers, or underscore
ID_RE = re.compile(r'^[a-z][\w\d\.]*$')


def isValidFieldName(value):
    if not ID_RE.match(value):
        raise Invalid(
            _(u'Please start with a lowercase letter and after this use only letters, '
              u'numbers and the following characters: _.')
        )
    if value in RESERVED_NAMES:
        raise Invalid(
            _(u"'${name}' is a reserved field name.", mapping={'name': value}))
    return True


class INewField(Interface):

    fieldset_id = Int(
        title=_(u'Fieldset ID'),
        description=_(u'Used to decide where to put this field.'),
        required=True,
    )

    title = TextLine(
        title=_(u'Title'),
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
        title=_(u'Field type'),
        vocabulary='Fields',
        required=True,
        # This can't be done yet or we'll create circular import problem.
        # So it will be injected from fields.py
        # default=TextLineFactory,
    )

    required = Bool(
        title=_(u'Required field'),
        description=_(
            u'Check this box if you want this field to be required.'
        ),
        default=False,
        required=False,
    )

    @invariant
    def checkTitleAndDescriptionTypes(data):
        if data.__name__ is not None and data.factory is not None:
            if data.__name__ == 'title' and \
                    data.factory.fieldcls is not TextLine:
                raise Invalid(
                    _(u"The 'title' field must be a Text line (string) field.")
                )
            if data.__name__ == 'description' and \
                    data.factory.fieldcls is not Text:
                raise Invalid(
                    _(u"The 'description' field must be a Text field.")
                )


class INewFieldset(Interface):

    label = TextLine(
        title=_(u'Title'),
        required=True
    )

    __name__ = ASCIILine(
        title=_(u'Short Name'),
        description=_(u'Used for programmatic access to the fieldset.'),
        required=True,
        constraint=isValidFieldName,
    )

    description = Text(
        title=_(u'Description'),
        required=False
    )
