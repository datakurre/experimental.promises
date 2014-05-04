# -*- coding:utf-8 -*-
from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
)
from plone.testing import z2
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE


class PromisesTests(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import experimental.promises
        self.loadZCML(package=experimental.promises)

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')


PROMISES_FIXTURE = PromisesTests()

PROMISES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PROMISES_FIXTURE,),
    name='PromisesTests:Integration')

PROMISES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PROMISES_FIXTURE,),
    name='PromisesTests:Functional')

PROMISES_ROBOT_TESTING = FunctionalTesting(
    bases=(PROMISES_FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           z2.ZSERVER),
    name='PromisesTests:Robot')
