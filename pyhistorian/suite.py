import doctest
import unittest
import sys
from cStringIO import StringIO
from story import *
from scenario import *
from steps import *
from should_dsl import *
try:
    # FIXME: it should not be here
    # it is here because we need pyhistorian tests passing
    # and pyhistorian_plone needs to work too :)
    from Products.PloneTestCase.PloneTestCase import PloneTestCase as TestCase
except ImportError:
    from unittest import TestCase

__all__= ['PyhistorianSuite', ]


class WrapTestCase(TestCase):
    """
    Specialization of TestCase to handle Stories + Steps
    """
    def __init__(self, func, func_name, msg, step_name):
        self._func = func
        self._func_name = func_name
        self._msg = msg
        self._step_name = step_name
        TestCase.__init__(self, '_func')

    def shortDescription(self):
        doc = self._msg
        return doc and doc.split("\n")[0].strip() or None

    def id(self):
        return "%s.%s" % (unittest._strclass(self.__class__), self._func_name)

    def setUp(self):
        """
        setUp should do NOTHING
        because if it does anything, every step - given/when/then - sharing vars would break
        """

    def tearDown(self):
        """
        tearDown should do NOTHING
        because if it does anything, every step - given/when/then - sharing vars would break
        """

    def shortDescription(self):
        return str(self)

    def __str__(self):
        step_msg = "\n    %s %s" % (self._step_name.title(), self._msg)
        return step_msg
#        class_name = self._func.im_class.__module__
#        return "    %s # %s" % (step_msg.ljust(30), class_name)

    def __repr__(self):
        return "<%s testMethod=%s>" % \
               (unittest._strclass(self.__class__), self._func_name)



class FakeTestCase(TestCase):
    def __init__(self, msg):
        self._msg = msg
        TestCase.__init__(self, 'fake_test')

    def fake_test(self):
        pass

    def run(self, result):
        """
        patch the test runner to not include the fake in the output
        """
        result.showAll = False
        result.testsRun -= 1
        result.startTest(self)
        if hasattr(result, 'stream'):
            result.stream.write(self._msg)
        result.stopTest(self)
        result.showAll = True
        
    __call__ = run

    def __str__(self):
        return self._msg

    def countTestCases(self):
        return 0


class _ScenarioTestSuite(unittest.TestSuite):
    def __init__(self, scenario):
        self._scenario = scenario
        self._tests = [FakeTestCase('  Scenario 1: %s' % scenario._title)]
        self._set_step_methods()

    def __iter__(self):
        return iter(self._tests)

    def _set_step_methods(self):
        for step_name in ['given', 'when', 'then']:
            self._set_step_method(step_name)

    def _set_step_method(self, step_name):
        step = getattr(self._scenario, '_%ss' % step_name)
        for method, message, args in step:
            func = getattr(self._scenario, method.func_name)
            wrapped_testcase = WrapTestCase(func, method.func_name, message, step_name)
            self._tests.append(wrapped_testcase)


class _StoryTestSuite(unittest.TestSuite):
    def __init__(self, story):
        header_lines = [line.strip() for line in story.__doc__.split('\n')]
        self._tests = [FakeTestCase('Story: %s\n  %s\n' % (story._title, '\n  '.join(header_lines)))]
        self._tests += [_ScenarioTestSuite(scenario) for scenario in story._scenarios]

    def __iter__(self):
        return iter(self._tests)
    

class PyhistorianSuite(unittest.TestSuite):
    def __init__(self, *stories):
        self._stories = [_StoryTestSuite(story) for story in stories]
        self._tests = self._stories

    def __iter__(self):
        return iter(self._stories)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
