from zope.interface import implements
from zope.interface.interfaces import IInterface
from zope.component import adapts
from zope.schema.interfaces import IField
from plone.schemaeditor.interfaces import IEditableSchema

def sorted_fields(schema):
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

class EditableSchema(object):
    """ Zope 3 schema adapter to allow addition/removal of schema fields
    """
    implements(IEditableSchema)
    adapts(IInterface)
    
    def __init__(self, schema):
        self.schema = schema
        
    def add_field(self, field, name=None):
        """ Add a field
        """
        if name is None:
            name = field.__name__
        
        if self.schema._InterfaceClass__attrs.has_key(name):
            raise ValueError, "%s schema already has a '%s' field" % (self.schema.__identifier__, name)
        
        self.schema._InterfaceClass__attrs[name] = field
        if hasattr(self.schema, '_v_attrs'):
            self.schema._v_attrs[name] = field
        
    def remove_field(self, name):
        """ Remove a field
        """
        try:
            del self.schema._InterfaceClass__attrs[name]
            if hasattr(self.schema, '_v_attrs'):
                del self.schema._v_attrs[name]
        except KeyError:
            raise ValueError, "%s schema has no '%s' field" % (self.schema.__identifier__, name)
