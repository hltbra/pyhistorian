'''
    >>> class newScenario(Scenario):
    ...     attribute_to_be_ignored = True
    ...
    ...     @Given('foo')
    ...     def one_should_be_equal_to_one(self):
    ...         1 |should_be.equal_to| 2
    ...         
    ...     @Given('a simple assert')
    ...     def an_assert(self):
    ...         assert 1==2
    ...
    ...     @Then('bar')
    ...     def two_should_be_equal_to_two(self):
    ...         2 |should_be.equal_to| 2
    ...
    ...     @Then('foobar')
    ...     def should_raise_an_exception(self):
    ...         raise Exception('just an error!')
    ...
    ...     @When('nothing happens')
    ...     def nothing(self):
    ...         return None
    ...

    >>> story = Story('Integrating pyhistorian to unittest',
    ...               as_a='unittest tester',
    ...               i_want_to='have integration with pyhistorian',
    ...               so_that='I have a nicer continuous integration')
    >>> story.add_scenario(newScenario('scenario 1'))
    <pyhistorian.Story object at ...>

    >>> suite = unittest.TestSuite()
    >>> story_suite = PyhistorianSuite(story)
    >>> suite.addTest(story_suite)
    >>> runner = unittest.TextTestRunner(stream=StringIO())
    >>> runner.run(suite)
    <unittest._TextTestResult run=5 errors=1 failures=2>
'''

import doctest
import unittest
import sys
from cStringIO import StringIO
from pyhistorian import *
from should_dsl import *


class Failure(object):
    '''
        >>> try:
        ...     raise Exception('foo')
        ... except Exception, e:
        ...     fail = Failure(e)
        >>> fail.shortDescription()
        'foo'
    '''
    failureException = AssertionError

    def __init__(self, exception):
        self._exception = exception

    def shortDescription(self):
        if len(self._exception.args):
            return self._exception.args[0]
        return ''


class StoryTestCase(object):
    def __init__(self, story):
        self._story = story
        self._tests = []
        self._set_test_methods()

    def _set_test_methods(self):
        for scenario in self._story._scenarios:
            for method in scenario._givens + scenario._whens + scenario._thens:
                self._tests.append(getattr(scenario, method[0].func_name))

    def runTest(self, result):
        for test in self._tests:
            result.startTest(test)
            try:
                test()
                result.addSuccess(test)
            except AssertionError, e:
                result.addFailure(Failure(e), sys.exc_info())
            except Exception, e:
                result.addError(Failure(e), sys.exc_info())


class PyhistorianSuite(object):
    def __init__(self, *stories):
        self._test_cases = [StoryTestCase(story) for story in stories]

    def addStory(self, story):
        self._test_cases.append(StoryTestCase(story))

    def __call__(self, result):
        for story in self._test_cases:
            story.runTest(result)


import doctest
doctest.testmod(optionflags=doctest.ELLIPSIS)
