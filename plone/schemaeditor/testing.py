# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class PloneSchemaeditorRobotLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import plone.app.dexterity
        self.loadZCML(package=plone.schemaeditor.tests,
                      name='robot_testing.zcml')
        self.loadZCML(package=plone.app.dexterity,
                      name='configure.zcml')
        self.loadZCML(package=plone.app.dexterity,
                      name='overrides.zcml')


FIXTURE = PloneSchemaeditorRobotLayer(
    name="ROBOT"
)


ACCEPTANCE = FunctionalTesting(
    bases=(
        FIXTURE,
        AUTOLOGIN_LIBRARY_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name="ACCEPTANCE"
)
