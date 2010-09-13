"""
PyhistorianSuite is an unittest compatible test suite


The fake objects exist because the unittest result
cares about output and number of tests


It is recommended to run pyhistorian_plone tests too. Check it out:
    
    http://github.com/hugobr/pyhistorian_plone3_buildout

"""

import unittest

__all__ = ('PyhistorianSuite',)


class _FakeTestCase(unittest.TestCase):
    """
    Fake TestCases do not count as a test and has a custom message
    """

    def __init__(self, obj):
        self._obj = obj
        unittest.TestCase.__init__(self, 'fake_test')

    def fake_test(self):
        pass

    def run(self, result):
        """
        only show the string representation (story or scenario line)
        """
        if hasattr(result, 'stream'):
            result.stream.write(str(self))
        
    def countTestCases(self):
        """
        Plone use this method to increment the number of tests ran
        """
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


class _StepTestCase(unittest.TestCase):
    """
    Specialization of TestCase to handle Steps
    """

    testcase = unittest.TestCase

    def __init__(self, func, msg, step_name):
        self._func = func
        self._msg = msg
        self._step_name = step_name
        self.testcase.__init__(self, '_func')

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
        """
        Plone use this method to retrieve verbose message
        """
        return str(self)

    def __str__(self):
        return "\n    %s %s" % (self._step_name.title(), self._msg)

    def __repr__(self):
        """
        shows function name - help for debugging
        """
        return '<Pyhistorian step method "%s">' % self._func.func_name


class _ScenarioTestSuite(unittest.TestSuite):
    fake_scenario_testcase = _FakeScenarioTestCase
    step_testcase = _StepTestCase

    def __init__(self, scenario):
        self._scenario = scenario
        self._tests = [self.fake_scenario_testcase(scenario)]
        self._add_step_methods()

    def _add_step_methods(self):
        self._add_step_method('given', self._scenario._givens)
        self._add_step_method('when', self._scenario._whens)
        self._add_step_method('then', self._scenario._thens)

    def _add_step_method(self, step_name, steps):
        for method, message, args in steps:
            step_func = getattr(self._scenario, method.func_name)
            step_testcase = self.step_testcase(step_func, message, step_name)
            self._tests.append(step_testcase)


class _StoryTestSuite(unittest.TestSuite):
    fake_story_testcase = _FakeStoryTestCase
    scenario_test_suite = _ScenarioTestSuite

    def __init__(self, story):
        self._tests = [self.fake_story_testcase(story)]
        self._tests += [self.scenario_test_suite(scenario) for scenario in story._scenarios]


class PyhistorianSuite(unittest.TestSuite):
    story_test_suite = _StoryTestSuite

    def __init__(self, *stories):
        self._tests = [self.story_test_suite(story) for story in stories]



