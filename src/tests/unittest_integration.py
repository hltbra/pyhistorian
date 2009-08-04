'''
>>> pyhistorian_suite = PyhistorianSuite(story)
>>> suite = unittest.TestSuite()
>>> suite.addTest(pyhistorian_suite)
>>> suite.addTest(unittest.TestLoader().loadTestsFromTestCase(sillyTestCase))
>>> runner = unittest.TextTestRunner(stream=StringIO())
>>> runner.run(suite)
<unittest._TextTestResult run=5 errors=0 failures=1>
'''

from pyhistorian import *
from pyhistorian.suite import *
from should_dsl import should_be
from cStringIO import StringIO
import unittest

class sillyTestCase(unittest.TestCase):
    def test_one_plus_one_should_be_two(self):
        self.assertEquals(2, 1+1)

    def test_should_fail(self):
        self.fail()

class sillyScenarioTestCase(Scenario):
    @Given('I just show you it works')
    def do_nothing(self):
        pass

    @When('I sum 1 and 1')
    def sum_one_and_one(self):
        self.result = 1 + 1

    @Then('I have two as result')
    def two_as_result(self):
        self.result |should_be.equal_to| 2


output = StringIO()

class IntegrationWithUnittest(Story):
    """As a pyhistorian integrator
       I want to integrate suites fo unittest and pyhistorian
       So that it is possible to have a good continuous integration"""

story = IntegrationWithUnittest('integrating a unittest testcase and a story',
                                output=output)
story.add_scenario(sillyScenarioTestCase('Silly TestCase'))
