"""
The fake objects exist because the unittest result
cares about output and number of tests
"""

import unittest
try:
    # FIXME: it should not be here
    # it is here because we need pyhistorian tests passing
    # and pyhistorian_plone needs to work too :)
    from Products.PloneTestCase.PloneTestCase import PloneTestCase as TestCase
except ImportError:
    from unittest import TestCase

__all__= ['PyhistorianSuite', ]


class PyhistorianSuite(unittest.TestSuite):
    def __init__(self, *stories):
        self._tests = [_StoryTestSuite(story) for story in stories]


class _StoryTestSuite(unittest.TestSuite):
    def __init__(self, story):
        self._tests = [_FakeStoryTestCase(story)]
        self._tests += [_ScenarioTestSuite(scenario) for scenario in story._scenarios]


class _ScenarioTestSuite(unittest.TestSuite):
    def __init__(self, scenario):
        self._scenario = scenario
        self._tests = [_FakeScenarioTestCase(scenario)]
        self._add_step_methods()

    def _add_step_methods(self):
        self._add_step_method('given', self._scenario._givens)
        self._add_step_method('when', self._scenario._whens)
        self._add_step_method('then', self._scenario._thens)

    def _add_step_method(self, step_name, steps):
        for method, message, args in steps:
            step_func = getattr(self._scenario, method.func_name)
            step_testcase = _StepTestCase(step_func, message, step_name)
            self._tests.append(step_testcase)


class _FakeTestCase(TestCase):
    """
    Fake TestCases do not count as a test and has a custom message
    """

    def __init__(self, obj):
        self._obj = obj
        TestCase.__init__(self, 'fake_test')

    def fake_test(self):
        pass

    def run(self, result):
        """
        patch the test runner to not include the fake in the output
        """
        if hasattr(result, 'stream'):
            result.stream.write(str(self))
        
    def countTestCases(self):
        return 0

    def setUp(self):
        """
        do nothing
        """

    def tearDown(self):
        """
        do nothing
        """


class _FakeScenarioTestCase(_FakeTestCase):
    def __str__(self):
        return '  Scenario 1: %s' % self._obj._title


class _FakeStoryTestCase(_FakeTestCase):
    def __str__(self):
        story = self._obj
        header_lines = [line.strip() for line in story.__doc__.split('\n')]
        story_header = 'Story: %s\n  %s\n' % (story._title, '\n  '.join(header_lines))
        return story_header


class _StepTestCase(TestCase):
    """
    Specialization of TestCase to handle Steps
    """
    def __init__(self, func, msg, step_name):
        self._func = func
        self._msg = msg
        self._step_name = step_name
        super(self.__class__, self).__init__('_func')

    def setUp(self):
        """
        setUp should do NOTHING
        because if it does anything, every step - given/when/then - break the sharing state
        """

    def tearDown(self):
        """
        tearDown should do NOTHING
        because if it does anything, every step - given/when/then - break the sharing state
        """

    def shortDescription(self):
        return str(self)

    def __str__(self):
        step_msg = "\n    %s %s" % (self._step_name.title(), self._msg)
        return step_msg

    def __repr__(self):
        """
        __repr__ shows function name - help for debuggingthe for debug
        """
        return '<Pyhistorian step method "%s">' % self._func.func_name
