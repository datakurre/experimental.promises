# -*- coding:utf-8 -*-
from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
)
from plone.testing import z2
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE


class FuturesTests(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import experimental.futures
        self.loadZCML(package=experimental.futures)

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')


FUTURES_FIXTURE = FuturesTests()

FUTURES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FUTURES_FIXTURE,),
    name='FuturesTests:Integration')

FUTURES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FUTURES_FIXTURE,),
    name='FuturesTests:Functional')

FUTURES_ROBOT_TESTING = FunctionalTesting(
    bases=(FUTURES_FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           z2.ZSERVER),
    name='FuturesTests:Robot')
