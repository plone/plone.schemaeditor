import unittest
import doctest
from Testing import ZopeTestCase as ztc
from zope.app.testing import placelesssetup
from zope.security.management import endInteraction
import Products.Five
from Products.Five import zcml
import plone.schemaeditor

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUp(self):
    placelesssetup.setUp()
    endInteraction()

    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('configure.zcml', plone.schemaeditor)
    
def tearDown(self):
    placelesssetup.tearDown()

def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            '../README.txt',
            setUp=setUp,
            tearDown=tearDown,
            optionflags=optionflags
            ),

        ])

from plone.z3cform.templates import ZopeTwoFormTemplateFactory
from plone.z3cform.interfaces import IFormWrapper
import os
path = lambda p: os.path.join(os.path.dirname(__file__), p)
layout_factory = ZopeTwoFormTemplateFactory(path('layout.pt'), form=IFormWrapper)
