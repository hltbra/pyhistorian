'''
    >>> class newScenarioTestCase(ScenarioTestCase):
    ...     attribute_to_be_ignored = True
    ...
    ...     @Given('foo')
    ...     def one_should_be_equal_to_one(self):
    ...         self._expect(1, 2)
    ...         
    ...     @Then('bar')
    ...     def two_should_be_equal_to_two(self):
    ...         self._expect(2, 2)
    ...
    ...     @Then('foobar')
    ...     def should_raise_an_exception(self):
    ...         raise Exception('just an error!')
    ...
    ...     @When('nothing happens')
    ...     def nothing(self):
    ...         return None
    ...
    ...     # it is a general purpose expect test
    ...     # (with should-dsl or not)
    ...     def _expect(self, v1, v2):
    ...         if should_dsl_imported:
    ...             return self.expect(v1).should_be.equal_to(v2)
    ...         return self.expect(v1 == v2)
    ...
    >>> suite = unittest.TestSuite()
    >>> pyhistorian_suite = PyhistorianSuite(newScenarioTestCase)
    >>> suite.addTest(pyhistorian_suite)
    >>> runner = unittest.TextTestRunner(stream=StringIO())
    >>> runner.run(suite)
    <unittest._TextTestResult run=4 errors=1 failures=1>
'''

import doctest
import unittest
import sys
from cStringIO import StringIO
from pyhistorian import *


class PyhistorianFailure(Exception):
    '''a failure to be accessed by unittest'''

should_dsl_imported = False
try:
    from should_dsl import DSLObject, ShouldNotSatisfied
    failureException = ShouldNotSatisfied
    should_dsl_imported = True
except ImportError:
    failureException = PyhistorianFailure


class Fail(object):
    '''
        >>> try:
        ...     raise Exception('foo')
        ... except Exception, e:
        ...     fail = Fail(e)
        >>> fail.shortDescription()
        'foo'
    '''
    failureException = failureException

    def __init__(self, exception):
        self._exception = exception

    def shortDescription(self):
        return self._exception.args[0]


class ScenarioTestCase(Scenario):
    def __init__(self):
        self._tests = []
        self._set_test_methods()

    def _set_test_methods(self):
        for method in self._givens + self._whens + self._thens:
            self._tests.append(getattr(self, method[0].func_name))

    def expect(self, value):
        if should_dsl_imported:
            return DSLObject(value)
        if value:
            return True
        raise failureException('Condition not satisfied!')

    def runTest(self, result):
        for test in self._tests:
            result.startTest(test)
            try:
                test()
                result.addSuccess(test)
            except failureException, e:
                result.addFailure(Fail(e), sys.exc_info())
            except Exception, e:
                result.addError(Fail(e), sys.exc_info())


class PyhistorianSuite(object):
    def __init__(self, *test_cases):
        self._test_cases = test_cases or []

    def addScenario(self, scenario):
        self._test_cases.append(scenario)

    def __call__(self, result):
        for test_case in self._test_cases:
            test_case().runTest(result)


import doctest
doctest.testmod()
