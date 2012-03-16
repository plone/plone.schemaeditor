.. -*-doctest-*-

==============
Field Schemata
==============

There are several places in the schemaeditor where we need to complete
and or improve on the schema provided by field instances in order to
fully support the field edit forms.

The schema used on an edit form for a field is retrieved by
introspecting the interfaces provided by the field looking for the
first which is or extends zope.schema.interfaces.IField.

    >>> from zope import schema
    >>> from plone.schemaeditor.browser.field import traversal, edit
    >>> field = schema.Field()
    >>> context = traversal.FieldContext(field, None)
    >>> form = edit.FieldEditForm(context, None)
    >>> form._schema
    <InterfaceClass zope.schema.interfaces.IField>

The default values for fields should generally be the same type as the
field itself.  The plone.schemaeditor declares that the zope.schema
field classes implement schemata with correct default types.

Some field types are declared generically as Object fields in zope.schema,
but we want to use the correct field types for our edit form. For example,
plone.schemaeditor declares that the min and max fields for Datetime
fields are also Datetimes.

    >>> field = schema.Datetime()
    >>> context = traversal.FieldContext(field, None)
    >>> form = edit.FieldEditForm(context, None)
    >>> form._schema['min']
    <zope.schema._field.Datetime object at ...>
    >>> form._schema['max']
    <zope.schema._field.Datetime object at ...>
