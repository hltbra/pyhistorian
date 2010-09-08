from pyhistorian import *
from pyhistorian.suite import *
from should_dsl import should_be
from cStringIO import StringIO
import unittest
import doctest


class PassingStory(Story):
    """In order to specify the unittest output
    As a smart dev
    I want to have a passing story
    """
    scenarios = ('PassingScenario',)

class PassingScenario(Scenario):
    @Then('it pass')
    def should_pass(self):
        pass

passing_story = PassingStory()


class UnittestSuiteOutput(unittest.TestCase):
    
    def test_output(self):
        output = StringIO()
        checker = doctest.OutputChecker()
        passing_suite = PyhistorianSuite(passing_story)
        runner = unittest.TextTestRunner(stream=output, verbosity=3)
        runner.run(passing_suite)
        expected_output = """\
        Story: Passing Story
          In order to specify the unittest output
          As a smart dev
          I want to have a passing story

          Scenario 1: Passing Scenario
            Then it should pass   ... OK

        ----------------------------------------------------------------------
        Ran 1 test in 0.000s
        """
        self.assertTrue(checker.check_output(expected_output, output.getvalue(), doctest.ELLIPSIS), output.getvalue())

if __name__ == '__main__':
    unittest.main()
