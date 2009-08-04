'''
>>> story.run()
...
>>> print output.getvalue(),
Story: Fixing regex bug in steps
As a issue fixer
I want to fix regex bugs
So that people can put ANYTHING into steps texts
<BLANKLINE>
Scenario 1: Regex bugged
  Given an ((irregular regex[[   ... OK
  Then it should not fail here   ... OK
<BLANKLINE>
Scenario 2: Regex fails here
  Given an ((irregular regex[[   ... OK
  Then it should fail here   ... OK
<BLANKLINE>
Ran 2 scenarios with 0 failures, 0 errors and 0 steps pending
<BLANKLINE>
'''

from pyhistorian import *
from cStringIO import StringIO
import doctest


class RegexBuggedScenario(Scenario):
    @Given('an ((irregular regex[[')
    def nothing(self):
        pass
    @Then('it should not fail here')
    def should_not_fail(self):
        pass


class RegexFailScenario(Scenario):
    Given('an ((irregular regex[[')

    @Then('it should fail here')
    def should_fail_here(self):
        pass

output = StringIO()
regex_bugged_scenario = RegexBuggedScenario('Regex bugged')
regex_fail = RegexFailScenario('Regex fails here')

class FixingRegexBugInSteps(Story):
    """As a issue fixer
       I want to fix regex bugs
       So that people can put ANYTHING into steps texts"""

story = FixingRegexBugInSteps(output=output)

story.add_scenario(regex_bugged_scenario)\
     .add_scenario(regex_fail)
