'''
>>> suite = unittest.TestSuite()
>>> story_suite = PyhistorianSuite(only_pyhistorian_stuff_story)
>>> suite.addTest(story_suite)
>>> runner = unittest.TextTestRunner(stream=StringIO())
>>> runner.run(suite)
<unittest._TextTestResult run=5 errors=1 failures=2>

>>> pyhistorian_suite = PyhistorianSuite(story)
>>> suite = unittest.TestSuite()
>>> suite.addTest(pyhistorian_suite)
>>> suite.addTest(unittest.TestLoader().loadTestsFromTestCase(sillyTestCase))
>>> runner = unittest.TextTestRunner(stream=StringIO())
>>> runner.run(suite)
<unittest._TextTestResult run=6 errors=0 failures=1>
'''

from pyhistorian import *
from pyhistorian.suite import *
from should_dsl import should_be
from cStringIO import StringIO
import unittest


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

only_pyhistorian_stuff_story = IntegrationWithUnittest()


class sillyTestCase(unittest.TestCase):
    def test_one_plus_one_should_be_two(self):
        self.assertEquals(2, 1+1)

    def test_should_fail(self):
        self.fail()

class SillyTestcase(Scenario):
    @Given('I just show you it works')
    def do_nothing(self):
        pass

    @When('I sum 1 and 1')
    def sum_one_and_one(self):
        self.result = 1 + 1

    @Then('I have two as result')
    def two_as_result(self):
        self.result |should_be.equal_to| 2

    Then('the pending stuff is ran as sucessful')


output = StringIO()

class IntegrationWithUnittest(Story):
    """As a pyhistorian integrator
       I want to integrate suites fo unittest and pyhistorian
       So that it is possible to have a good continuous integration"""
    output = output
    scenarios = (SillyTestcase, )

story = IntegrationWithUnittest()
