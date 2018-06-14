# -*- coding: utf-8 -*-
from plone.z3cform.interfaces import IFormWrapper
from plone.z3cform.templates import ZopeTwoFormTemplateFactory
from Testing import ZopeTestCase as ztc
from zope.interface import classImplements
from zope.interface import implementedBy
from zope.interface import Interface
from Zope2.App import zcml
from ZPublisher.BaseRequest import BaseRequest

import doctest
import os
import plone.schemaeditor
import re
import six
import unittest


optionflags = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_ONLY_FIRST_FAILURE)


def setUp(self):
    from Zope2.App.schema import configure_vocabulary_registry
    configure_vocabulary_registry()

    zcml.load_config('browser_testing.zcml', plone.schemaeditor.tests)

    # add a test layer to the request so we can use special form templates
    # that don't pull in main_template
    classImplements(BaseRequest, ITestLayer)


def tearDown(self):
    classImplements(implementedBy(BaseRequest) - ITestLayer)


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            want = re.sub('zExceptions.unauthorized.Unauthorized', 'Unauthorized', want)
            got = re.sub("u'(.*?)'", "'\\1'", got)
            want = re.sub("b'(.*?)'", "'\\1'", want)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


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
            optionflags=optionflags,
            checker=Py23DocChecker(),
        ),

    ])


class ITestLayer(Interface):
    pass


class RenderWidget(object):

    def __init__(self, widget, request):
        self.widget = widget

    def __call__(self):
        return self.widget.render()


layout_factory = ZopeTwoFormTemplateFactory(
    os.path.join(os.path.dirname(__file__), 'layout.pt'),
    form=IFormWrapper, request=ITestLayer,
)
