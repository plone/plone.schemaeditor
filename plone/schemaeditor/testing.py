# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.testing import z2
from zope.interface import Interface

import doctest


class ITestLayer(Interface):
    pass


class PloneSchemaeditorRobotLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import plone.schemaeditor
        self.loadZCML(package=plone.schemaeditor)


class PloneSchemaeditorBrowserLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import plone.schemaeditor
        self.loadZCML(package=plone.schemaeditor)
        self.loadZCML(
            package=plone.schemaeditor.tests,
            name='browser_testing.zcml',
        )
        from Zope2.App.schema import configure_vocabulary_registry
        configure_vocabulary_registry()


PLONE_SCHEMAEDITOR_FIXTURE = PloneSchemaeditorBrowserLayer()
PLONE_SCHEMAEDITOR_ROBOT_FIXTURE = PloneSchemaeditorRobotLayer()

PLONE_SCHEMAEDITOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_SCHEMAEDITOR_FIXTURE, ),
    name='PloneSchemaeditorLayer:IntegrationTesting',
)
PLONE_SCHEMAEDITOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_SCHEMAEDITOR_FIXTURE, ),
    name='PloneSchemaeditorLayer:FunctionalTesting',
)

PLONE_SCHEMAEDITOR_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PloneSchemaeditorRobotLayer,
        AUTOLOGIN_LIBRARY_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='PloneSchemaeditorLayer:AcceptanceTesting',
)


optionflags = (
    doctest.ELLIPSIS |
    doctest.NORMALIZE_WHITESPACE |
    doctest.REPORT_ONLY_FIRST_FAILURE
)
