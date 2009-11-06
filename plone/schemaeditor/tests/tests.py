import unittest
import doctest
from Testing import ZopeTestCase as ztc
import Products.Five
from Products.Five import zcml
import plone.schemaeditor
from zope.interface import classImplements, implementedBy
from ZPublisher.BaseRequest import BaseRequest

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUp(self):
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('configure.zcml', plone.schemaeditor)
    zcml.load_config('tests.zcml', plone.schemaeditor.tests)

    # make sure we use the correct vocabulary registry
    import zope.app.schema.vocabulary
    
    # add a test layer to the request so we can use special form templates that don't
    # pull in main_template
    classImplements(BaseRequest, ITestLayer)
    
def tearDown(self):
    classImplements(implementedBy(BaseRequest) - ITestLayer)

def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'editing.txt',
            setUp=setUp,
            tearDown=tearDown,
            optionflags=optionflags
            ),

        ])

from zope.interface import Interface
class ITestLayer(Interface):
    pass
from plone.z3cform.templates import ZopeTwoFormTemplateFactory
from plone.z3cform.interfaces import IFormWrapper
from plone.schemaeditor.interfaces import IJavascriptFormWrapper
import os
path = lambda p: os.path.join(os.path.dirname(__file__), p)
layout_factory = ZopeTwoFormTemplateFactory(path('layout.pt'), form=IFormWrapper, request=ITestLayer)
js_layout_factory = ZopeTwoFormTemplateFactory(path('layout.pt'), form=IJavascriptFormWrapper, request=ITestLayer)
