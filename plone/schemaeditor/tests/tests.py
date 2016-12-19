# -*- coding: utf-8 -*-
from plone.z3cform.interfaces import IFormWrapper
from plone.z3cform.templates import ZopeTwoFormTemplateFactory
from Products.Five import zcml
from Testing import ZopeTestCase as ztc
from zope.interface import classImplements
from zope.interface import implementedBy
from zope.interface import Interface
from ZPublisher.BaseRequest import BaseRequest

import doctest
import os
import plone.schemaeditor
import unittest


optionflags = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_ONLY_FIRST_FAILURE)


def setUp(self):
    try:
        from Zope2.App.schema import configure_vocabulary_registry
    except ImportError:
        try:
            from zope.schema.vocabulary import setVocabularyRegistry
            from Products.Five.schema import Zope2VocabularyRegistry
        except ImportError:
            pass
        else:
            setVocabularyRegistry(Zope2VocabularyRegistry())
    else:
        configure_vocabulary_registry()

    zcml.load_config('browser_testing.zcml', plone.schemaeditor.tests)

    # add a test layer to the request so we can use special form templates
    # that don't pull in main_template
    classImplements(BaseRequest, ITestLayer)


def tearDown(self):
    classImplements(implementedBy(BaseRequest) - ITestLayer)


def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'field_schemata.rst',
            'editing.rst',
            'extending.rst',
            'choice.rst',
            'minmax.rst',
            setUp=setUp,
            tearDown=tearDown,
            optionflags=optionflags
        ),

    ])


class ITestLayer(Interface):
    pass


class RenderWidget(object):

    def __init__(self, widget, request):
        self.widget = widget

    def __call__(self):
        return self.widget.render()


path = lambda p: os.path.join(os.path.dirname(__file__), p)
layout_factory = ZopeTwoFormTemplateFactory(
    path('layout.pt'),
    form=IFormWrapper, request=ITestLayer,
)
