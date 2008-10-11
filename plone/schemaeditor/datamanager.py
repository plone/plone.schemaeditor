from AccessControl import getSecurityManager

from zope.component import adapts
from zope.schema.interfaces import IField
from z3c import form

from plone.schemaeditor.interfaces import IFieldEditingContext

class SchemaFieldFormDataManager(form.datamanager.DataManager):
    """Form data adapter that modifies Field definitions on the schema."""
    adapts(IFieldEditingContext, IField)

    def __init__(self, wrapper, field):
        self.context = wrapper
        self.schema = wrapper.schema
        self.field = wrapper.field
        
        self.metafield = field

    def get(self):
        # """See z3c.form.interfaces.IDataManager"""
        return getattr(self.field, self.metafield.__name__)

    def query(self, default=form.interfaces.NOVALUE):
        # """See z3c.form.interfaces.IDataManager"""
        try:
            return self.get()
        except AttributeError:
            return default
        return None

    def set(self, value):
        # """See z3c.form.interfaces.IDataManager"""
        if self.metafield.readonly:
            raise TypeError("Can't set values on read-only fields "
                            "(name=%s, class=%s.%s)"
                            % (self.metafield.__name__,
                               self.field.__class__.__module__,
                               self.field.__class__.__name__))
        setattr(self.field, self.metafield.__name__, value)
        return

    def canAccess(self):
        """See z3c.form.interfaces.IDataManager"""
        return getSecurityManager().checkPermission('Manage schemata', self.context)
    
    def canWrite(self):
        """See z3c.form.interfaces.IDataManager"""
        return getSecurityManager().checkPermission('Manage schemata', self.context)
