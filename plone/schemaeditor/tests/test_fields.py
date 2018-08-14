# -*- coding: utf-8 -*-
from plone.app.testing import PLONE_FIXTURE
from plone.schemaeditor.fields import TextLineChoiceField
from plone.schemaeditor.fields import TextLineMultiChoiceField
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class DummyField(object):
    """ Dummy field """

    def __init__(self):
        self.value_type = self

    vocabulary = None


class VocabularyTestCase(unittest.TestCase):

    layer = PLONE_FIXTURE

    def assertVocabulary(self, voc, values):
        self.assertTrue(IVocabularyTokenized.providedBy(voc))
        self.assertEqual(
            [(term.value, term.token, term.title) for term in voc],
            values
        )

    def test_singlechoice_voc(self):
        field = TextLineChoiceField(DummyField())
        field.values = [u'New York', u'city2|München']
        self.assertEqual(
            field.values,
            [u'New York', u'city2|München']
        )
        self.assertVocabulary(
            field.vocabulary,
            [(u'New York', u'New York', u'New York'),
             (u'city2', u'city2', u'München')]
          )

    def test_multichoice_voc(self):
        field = TextLineMultiChoiceField(DummyField())
        field.values = [u'New York', u'city1|Zürich']
        self.assertEqual(
            field.values,
            [u'New York', u'city1|Zürich']
        )
        self.assertVocabulary(
            field.vocabulary,
            [(u'New York', u'New York', u'New York'),
             (u'city1', u'city1', u'Zürich')]
            )
