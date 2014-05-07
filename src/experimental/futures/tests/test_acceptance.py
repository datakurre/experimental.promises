# -*- coding: utf-8 -*- #
import unittest
import robotsuite

from plone.testing import layered
from experimental.futures.testing import (
    FUTURES_ROBOT_TESTING
)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('acceptance'),
                layer=FUTURES_ROBOT_TESTING),
    ])
    return suite
