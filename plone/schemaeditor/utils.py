# -*- coding: utf-8 -*-
from plone.schemaeditor.interfaces import IEditableSchema
from plone.schemaeditor.interfaces import ISchemaModifiedEvent
from plone.supermodel.interfaces import FIELDSETS_KEY
from zope.component import adapter
from zope.interface.interfaces import ObjectEvent
from zope.interface import implementer
from zope.interface.interfaces import IInterface
from zope.schema.interfaces import IField

import pkg_resources

_zope_interface_version_major = int(
    pkg_resources.require('zope.interface')[0].version.split('.')[0]
)

def sortedFields(schema):
    """ Like getFieldsInOrder, but does not include fields from bases

        This is verbatim from plone.supermodel's utils.py but I didn't
        want to create a dependency.
    """
    fields = []
    for name in schema.names(all=False):
        field = schema[name]
        if IField.providedBy(field):
            fields.append((name, field,))
    fields.sort(key=lambda item: item[1].order)
    return fields


def non_fieldset_fields(schema):
    fieldset_fields = []
    fieldsets = schema.queryTaggedValue(FIELDSETS_KEY, [])

    for fieldset in fieldsets:
        fieldset_fields.extend(fieldset.fields)

    fields = [info[0] for info in sortedFields(schema)]
    return [f for f in fields if f not in fieldset_fields]


def get_field_fieldset(schema, field_name):
    fieldsets = schema.queryTaggedValue(FIELDSETS_KEY, [])
    for fieldset in fieldsets:
        if field_name in fieldset.fields:
            return fieldset
    return None


def get_fieldset_from_index(schema, index):
    """Return a fieldset from a schema according to it's index.
    """
    index = int(index or 0) - 1
    fieldsets = schema.queryTaggedValue(FIELDSETS_KEY, [])
    return fieldsets[index] if index >= 0 else None


def new_field_position(schema, fieldset_id=None, new_field=False):
    """Get the position for a new field in a schema's fieldset.
    If fieldset_id is ``None`` or ``0``, the default fieldset is used.
    """
    fieldset_id = int(fieldset_id or 0)
    position = 0
    ordered_field_ids = [info[0] for info in sortedFields(schema)]
    if not fieldset_id:
        default_fields = non_fieldset_fields(schema)
        if len(default_fields) > 0:
            position = ordered_field_ids.index(default_fields[-1]) + 1
    else:
        # First we get the first of the fieldsets after the new one
        fieldsets = schema.queryTaggedValue(FIELDSETS_KEY, [])
        for fs in fieldsets[fieldset_id:]:
            if len(fs.fields) > 0:
                position = ordered_field_ids.index(fs.fields[0])
                break
        else:
            position = len(ordered_field_ids) - 1
            if new_field:
                # Special case when adding a new field
                position += 1

    return position


@implementer(IEditableSchema)
@adapter(IInterface)
class EditableSchema(object):

    """ Zope 3 schema adapter to allow addition/removal of schema fields

        XXX this needs to be made threadsafe
    """

    def __init__(self, schema):
        self.schema = schema

    def addField(self, field, name=None):
        """Add a field"""
        if name is None:
            name = field.__name__

        if name in self.schema._InterfaceClass__attrs:
            raise ValueError(
                '{0} schema already has a "{1}" field'.format(
                    self.schema.__identifier__,
                    name,
                )
            )

        self.schema._InterfaceClass__attrs[name] = field
        if _zope_interface_version_major >= 5:
            self.schema._v_attrs = None
        else:
            if hasattr(self.schema, '_v_attrs'):
                self.schema._v_attrs[name] = field

        field.interface = self.schema

    def removeField(self, field_name):
        """ Remove a field
        """
        try:
            self.schema[field_name].interface = None
            del self.schema._InterfaceClass__attrs[field_name]
            if _zope_interface_version_major >= 5:
                self.schema._v_attrs = None
            else:
                if hasattr(self.schema, '_v_attrs'):
                    del self.schema._v_attrs[field_name]
            for fieldset in self.schema.queryTaggedValue(FIELDSETS_KEY, []):
                if field_name in fieldset.fields:
                    fieldset.fields.remove(field_name)
        except KeyError:
            raise ValueError(
                '{0} schema has no "{1}" field'.format(
                    self.schema.__identifier__,
                    field_name,
                )
            )

    def moveField(self, field_name, new_pos):
        """ Move a field to the (new_pos)th position in the schema's sort
        order (indexed beginning at 0).

        Schema fields are assigned an 'order' attribute that increments for
        each new field instance.
        We shuffle these around in case it matters anywhere that they're
        unique.
        """
        moving_field = self.schema[field_name]
        ordered_field_ids = [
            name for (name, field) in sortedFields(self.schema)]

        # make sure this is sane
        if not isinstance(new_pos, int):
            raise IndexError('The new field position must be an integer.')
        if new_pos < 0:
            raise IndexError('The new field position must be greater than 0.')
        if new_pos >= len(ordered_field_ids):
            raise IndexError(
                'The new field position must be less than the number of '
                'fields.'
            )

        # determine which fields we have to update the order attribute on
        cur_pos = ordered_field_ids.index(field_name)
        if new_pos == cur_pos:
            # no change; short circuit
            return
        elif new_pos < cur_pos:
            # walking backwards, we can't use -1 as the endpoint b/c that means
            # the end of the list
            slice_end = new_pos - 1
            if slice_end == -1:
                slice_end = None
            intervening_fields = [
                self.schema[field_id]
                for field_id
                in ordered_field_ids[cur_pos - 1:slice_end:-1]
            ]
        elif new_pos > cur_pos:
            intervening_fields = [
                self.schema[field_id]
                for field_id
                in ordered_field_ids[cur_pos + 1:new_pos + 1]
            ]

        # do a little dance
        prev_order = moving_field.order
        for field in intervening_fields:
            order_buffer = field.order
            field.order = prev_order
            prev_order = order_buffer
        moving_field.order = prev_order

        # if field is in a fieldset, also reorder fieldset tagged value
        fieldset = get_field_fieldset(self.schema, field_name)
        if fieldset is not None:
            ordered_field_ids = [info[0] for info in sortedFields(self.schema)]
            fieldset.fields = sorted(fieldset.fields,
                                     key=lambda x: ordered_field_ids.index(x))

    def changeFieldFieldset(self, field_name, next_fieldset):
        """Move a field from a fieldset to another,
        next_fieldset is a fieldset object, or None for default fieldset
        """
        current_fieldset = get_field_fieldset(self.schema, field_name)
        if current_fieldset != next_fieldset:
            # move field
            if next_fieldset is not None:
                next_fieldset.fields.append(field_name)

            if current_fieldset is not None:
                current_fieldset.fields.remove(field_name)


@implementer(ISchemaModifiedEvent)
class SchemaModifiedEvent(ObjectEvent):
    pass


class FieldModifiedEvent(SchemaModifiedEvent):

    def __init__(self, obj, field):
        super(FieldModifiedEvent, self).__init__(obj)
        self.field = field


class FieldAddedEvent(FieldModifiedEvent):
    pass


class FieldRemovedEvent(FieldModifiedEvent):
    pass
