import os
from zope.interface import implements
from plone.z3cform.layout import FormWrapper
from plone.z3cform.templates import ZopeTwoFormTemplateFactory
from plone.schemaeditor.interfaces import IJavascriptFormWrapper

class JavascriptFormWrapper(FormWrapper):
    implements(IJavascriptFormWrapper)
    
    def javascript(self):
        return self.form_instance.javascript()

path = lambda p: os.path.join(os.path.dirname(__file__), p)
layout_factory = ZopeTwoFormTemplateFactory(
    path('jsform.pt'), form=IJavascriptFormWrapper)
