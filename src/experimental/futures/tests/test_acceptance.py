# -*- coding: utf-8 -*- #
import logging
import threading
import unittest

from Products.Five.browser import BrowserView

import robotsuite
from plone.testing import layered
from zope.interface import noLongerProvides
from experimental.futures.interfaces import IContainsPromises
from experimental.futures.testing import FUTURES_ROBOT_TESTING
from experimental import futures


logger = logging.getLogger('experimental.futures')


def echo(value):
    logger.info(u'thread: {0:s}'.format(threading.currentThread()))
    logger.info(u'echo: {0:s}'.format(value))
    return value


class ResultView(BrowserView):
    def content(self):
        try:
            return futures.result('futures.testing')
        except futures.FutureNotSubmittedError:
            futures.submit(
                'futures.testing',
                echo, u'testing-result')
            return u'testing placeholder'


class ResultOrSubmitView(BrowserView):
    def content(self):
        return futures.resultOrSubmit(
            'futures.testing', u'placeholder',
            echo, u'testing-result-or-submit')


class ResultOrSubmitPlaceholderView(BrowserView):
    def content(self):
        try:
            return futures.resultOrSubmit(
                'futures.testing', u'placeholder',
                echo, u'testing-result-or-submit')
        finally:
            noLongerProvides(self.request, IContainsPromises)


class ResultMultiprocessView(BrowserView):
    def content(self):
        try:
            return futures.result('futures.testing')
        except futures.FutureNotSubmittedError:
            futures.submitMultiprocess(
                'futures.testing',
                echo, u'testing-result-multiprocess')
            return u'testing placeholder'


class ResultOrSubmitMultiprocessView(BrowserView):
    def content(self):
        return futures.resultOrSubmitMultiprocess(
            'futures.testing', u'placeholder',
            echo, u'testing-result-or-submit-multiprocess')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('test_acceptance.robot'),
                layer=FUTURES_ROBOT_TESTING),
    ])
    return suite
