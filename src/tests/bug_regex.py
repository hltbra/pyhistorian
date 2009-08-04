'''
>>> FixingRegexBugInSteps().run()
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
Scenario 2: Regex fails
  Given an ((irregular regex[[   ... OK
  Then it should fail here   ... OK
<BLANKLINE>
Ran 2 scenarios with 0 failures, 0 errors and 0 steps pending
<BLANKLINE>
'''

from pyhistorian import *
from cStringIO import StringIO
import doctest


class RegexBugged(Scenario):
    @Given('an ((irregular regex[[')
    def nothing(self):
        pass
    @Then('it should not fail here')
    def should_not_fail(self):
        pass


class RegexFails(Scenario):
    Given('an ((irregular regex[[')

    @Then('it should fail here')
    def should_fail_here(self):
        pass

output = StringIO()

class FixingRegexBugInSteps(Story):
    """As a issue fixer
       I want to fix regex bugs
       So that people can put ANYTHING into steps texts"""
    output = output
    scenarios = (RegexBugged, RegexFails)
