from plone.schemaeditor import _
from plone.schemaeditor.utils import SchemaModifiedEvent
from plone.supermodel.interfaces import FIELDSETS_KEY
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.container.contained import notifyContainerModified
from zope.event import notify


class DeleteFieldset(BrowserView):

    def __call__(self):
        fieldset_name = self.request.form.get('name')
        schema = self.context.schema
        fieldsets = schema.queryTaggedValue(FIELDSETS_KEY, [])

        new_fieldsets = []
        for fieldset in fieldsets:
            if fieldset.__name__ == fieldset_name:
                if fieldset.fields:
                    IStatusMessage(self.request).addStatusMessage(
                        _(u'Only empty fieldsets can be deleted'),
                        type='error')
                    return self.request.RESPONSE.redirect(self.nextURL)
                continue
            else:
                new_fieldsets.append(fieldset)
        if len(fieldsets) == len(new_fieldsets):
            IStatusMessage(self.request).addStatusMessage(
                _(u'Fieldset not found'), type='error')
            return self.request.RESPONSE.redirect(self.nextURL)

        schema.setTaggedValue(FIELDSETS_KEY, new_fieldsets)

        notifyContainerModified(schema)
        notify(SchemaModifiedEvent(self.context))
        IStatusMessage(self.request).addStatusMessage(
            _(u'Fieldset deleted successfully.'), type='info')
        return self.request.RESPONSE.redirect(self.nextURL)

    @property
    def nextURL(self):
        return self.request.get('HTTP_REFERER')
