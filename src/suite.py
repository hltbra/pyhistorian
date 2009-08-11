'''
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
from story import *
from scenario import *
from steps import *
from should_dsl import *


__all__= ['PyhistorianSuite', ]


class Failure(object):
    '''
        >>> fail = Failure(Exception('foo'))
        >>> fail.shortDescription()
        'foo'
        >>> fail2 = Failure(Exception())
        >>> fail2.shortDescription()
        ''
    '''
    failureException = AssertionError

    def __init__(self, exception):
        self._exception = exception

    def shortDescription(self):
        if len(self._exception.args):
            return self._exception.args[0]
        return ''


class StoryCase(object):
    def __init__(self, story):
        self._story = story
        self._steps = []
        self._set_step_methods()

    def _set_step_methods(self):
        for scenario in self._story._scenarios:
            for method, message, args in scenario._givens + scenario._whens + scenario._thens:
                self._steps.append(getattr(scenario, method.func_name))

    def run_steps(self, result):
        for step in self._steps:
            result.startTest(step)
            try:
                step()
                result.addSuccess(step)
            except AssertionError, e:
                result.addFailure(Failure(e), sys.exc_info())
            except Exception, e:
                result.addError(Failure(e), sys.exc_info())


class PyhistorianSuite(object):
    def __init__(self, *stories):
        self._story_cases = [StoryCase(story) for story in stories]

    def __call__(self, result):
        for story in self._story_cases:
            story.run_steps(result)


"""
    down here is the needs to run the doctest
"""
class ExampleScenario(Scenario):
    attribute_to_be_ignored = True

    @Given('foo')
    def one_should_be_equal_to_one(self):
        1 |should_be.equal_to| 2
        
    @Given('a simple assert')
    def an_assert(self):
        assert 1==2

    @Then('bar')
    def two_should_be_equal_to_two(self):
        2 |should_be.equal_to| 2

    @Then('foobar')
    def should_raise_an_exception(self):
        raise Exception('just an error!')

    @When('nothing happens')
    def nothing(self):
        return None


class IntegrationWithUnittest(Story):
    """As an unittest tester
       I want to have integration with pyhistorian
       So that I have a nicer continuous integration"""
    scenarios = [ExampleScenario]

story = IntegrationWithUnittest()


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
