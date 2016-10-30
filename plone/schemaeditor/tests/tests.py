# -*- coding: utf-8 -*-
from plone.schemaeditor.testing import optionflags
from plone.schemaeditor.testing import ITestLayer
from plone.schemaeditor.testing import PLONE_SCHEMAEDITOR_FUNCTIONAL_TESTING
from plone.testing import layered
from plone.z3cform.interfaces import IFormWrapper
from plone.z3cform.templates import ZopeTwoFormTemplateFactory
from zope.interface import classImplements
from zope.interface import implementedBy
from ZPublisher.BaseRequest import BaseRequest

import doctest
import os
import re
import six
import unittest


doctests_files = [
    'choice.rst',
    'editing.rst',
    'extending.rst',
    'field_schemata.rst',
    'minmax.rst',
]


def setUp(self):
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
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'tests/{0}'.format(test_file),
                package='plone.schemaeditor',
                optionflags=optionflags,
                setUp=setUp,
                tearDown=tearDown,
                checker=Py23DocChecker(),
            ),
            layer=PLONE_SCHEMAEDITOR_FUNCTIONAL_TESTING)
        for test_file in doctests_files]
    )
    return suite


class RenderWidget(object):

    def __init__(self, widget, request):
        self.widget = widget

    def __call__(self):
        return self.widget.render()


path = lambda p: os.path.join(os.path.dirname(__file__), p)
layout_factory = ZopeTwoFormTemplateFactory(
    path('layout.pt'),
    form=IFormWrapper,
    request=ITestLayer,
)
