# -*- coding: utf-8 -*- #
import unittest
import robotsuite

from plone.testing import layered
from experimental.promises.testing import (
    PROMISES_ROBOT_TESTING
)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('acceptance'),
                layer=PROMISES_ROBOT_TESTING),
    ])
    return suite
