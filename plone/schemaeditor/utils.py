from zope.interface import implements
from zope.interface.interfaces import IInterface
from zope.component import adapts
from zope.component.interfaces import ObjectEvent
from zope.schema.interfaces import IField
from plone.schemaeditor.interfaces import IEditableSchema
from plone.schemaeditor.interfaces import ISchemaModifiedEvent
from plone.supermodel.interfaces import FIELDSETS_KEY


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
    fieldsets = schema.getTaggedValue(FIELDSETS_KEY)
    for fieldset in fieldsets:
        fieldset_fields.extend(fieldset.fields)

    fields = [name for (name, field) in sortedFields(schema)]
    return [f for f in fields if f not in fieldset_fields]


class EditableSchema(object):
    """ Zope 3 schema adapter to allow addition/removal of schema fields

        XXX this needs to be made threadsafe
    """
    implements(IEditableSchema)
    adapts(IInterface)

    def __init__(self, schema):
        self.schema = schema

    def addField(self, field, name=None):
        """ Add a field
        """
        if name is None:
            name = field.__name__

        if self.schema._InterfaceClass__attrs.has_key(name):
            raise ValueError, "%s schema already has a '%s' field" % (self.schema.__identifier__, name)

        self.schema._InterfaceClass__attrs[name] = field
        if hasattr(self.schema, '_v_attrs'):
            self.schema._v_attrs[name] = field

        field.interface = self.schema

    def removeField(self, name):
        """ Remove a field
        """
        try:
            self.schema[name].interface = None
            del self.schema._InterfaceClass__attrs[name]
            if hasattr(self.schema, '_v_attrs'):
                del self.schema._v_attrs[name]
        except KeyError:
            raise ValueError, "%s schema has no '%s' field" % (self.schema.__identifier__, name)

    def moveField(self, field_id, new_pos):
        """ Move a field to the (new_pos)th position in the schema's sort order (indexed beginning
            at 0).

            Schema fields are assigned an 'order' attribute that increments for each new field
            instance.  We shuffle these around in case it matters anywhere that they're unique.
        """
        moving_field = self.schema[field_id]
        ordered_field_ids = [name for (name, field) in sortedFields(self.schema)]

        # make sure this is sane
        if not isinstance(new_pos, int):
            raise IndexError, 'The new field position must be an integer.'
        if new_pos < 0:
            raise IndexError, 'The new field position must be greater than 0.'
        if new_pos >= len(ordered_field_ids):
            raise IndexError, 'The new field position must be less than the number of fields.'

        # determine which fields we have to update the order attribute on
        cur_pos = ordered_field_ids.index(field_id)
        if new_pos == cur_pos:
            # no change; short circuit
            return
        elif new_pos < cur_pos:
            # walking backwards, we can't use -1 as the endpoint b/c that means
            # the end of the list
            slice_end = new_pos - 1
            if slice_end == -1:
                slice_end = None
            intervening_fields = [self.schema[field_id] for field_id in ordered_field_ids[cur_pos - 1:slice_end:-1]]
        elif new_pos > cur_pos:
            intervening_fields = [self.schema[field_id] for field_id in ordered_field_ids[cur_pos + 1:new_pos + 1]]

        # do a little dance
        prev_order = moving_field.order
        for field in intervening_fields:
            order_buffer = field.order
            field.order = prev_order
            prev_order = order_buffer
        moving_field.order = prev_order


class SchemaModifiedEvent(ObjectEvent):
    implements(ISchemaModifiedEvent)


class FieldModifiedEvent(SchemaModifiedEvent):

    def __init__(self, object, field):
        super(FieldModifiedEvent, self).__init__(object)
        self.field = field


class FieldAddedEvent(FieldModifiedEvent):
    pass


class FieldRemovedEvent(FieldModifiedEvent):
    pass
