"""
PyhistorianloneSuite is an PloneTestCase compatible test suite


Every class here is the specialization of the similar in suite.py, but
specially written for Plone - the names are almost the same, except for
the leading _Plone in the name.

This module contains kinds of "mixins" for PloneTestCase integration,
all based upon suite.py classes.

You should check pyhistorian.suite out first :)
"""

from Products.PloneTestCase.PloneTestCase import PloneTestCase
from pyhistorian.suite import (PyhistorianSuite,
                               _StoryTestSuite,
                               _ScenarioTestSuite,
                               _StepTestCase,
                               _FakeTestCase,
                               _FakeScenarioTestCase,
                               _FakeStoryTestCase,)

__all__ = ('PyhistorianPloneSuite',)


class _PloneFakeTestCase(_FakeTestCase, PloneTestCase):
    def __init__(self, obj):
        self._obj = obj
        PloneTestCase.__init__(self, 'fake_test')


class _PloneFakeScenarioTestCase(_PloneFakeTestCase, _FakeScenarioTestCase):
    pass


class _PloneFakeStoryTestCase(_PloneFakeTestCase, _FakeStoryTestCase):
    pass


class _PloneStepTestCase(_StepTestCase, PloneTestCase):
    def __repr__(self):
        """
        shows function name - help for debugging
        """
        return '<Pyhistorian plone step method "%s">' % self._func.func_name


class _PloneScenarioTestSuite(_ScenarioTestSuite):
    testcase = PloneTestCase
    fake_scenario_testcase = _PloneFakeScenarioTestCase
    step_testcase = _PloneStepTestCase


class _PloneStoryTestSuite(_StoryTestSuite):
    fake_story_testcase = _PloneFakeStoryTestCase
    scenario_test_suite = _PloneScenarioTestSuite


class PyhistorianPloneSuite(PyhistorianSuite):
    story_test_suite = _PloneStoryTestSuite
