'''
>>> print output.getvalue(),
Story: Fixing Regex Bug in Steps
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

story = Story('Fixing Regex Bug in Steps',
              as_a='issue fixer',
              i_want_to='fix regex bugs',
              so_that='people can put ANYTHING into steps texts',
              output=output)
(story.add_scenario(regex_bugged_scenario)
      .add_scenario(regex_fail)
      .run())
