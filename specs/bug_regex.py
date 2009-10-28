'''
>>> FixingRegexBugInSteps.run()
False
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
    Then it should fail here   ... FAIL
<BLANKLINE>
  Failures:
    File ".../bug_regex.py", line ..., in should_fail_here
      self._irregular_regex |should_not_be| None
...
    ShouldNotSatisfied: None is None
<BLANKLINE>
<BLANKLINE>
  Ran 2 scenarios with 1 failure, 0 errors and 0 pending steps
<BLANKLINE>
'''

from pyhistorian import *
from should_dsl import should_not_be
from cStringIO import StringIO
import doctest


output = StringIO()

class FixingRegexBugInSteps(Story):
    """As a issue fixer
       I want to fix regex bugs
       So that people can put ANYTHING into steps texts"""
    output = output
    colored = False
    scenarios = ('RegexBugged', 'RegexFails')

class RegexBugged(Scenario):
    @Given('an ((irregular regex[[')
    def nothing(self):
        self._irregular_regex = None
    @Then('it should not fail here')
    def should_not_fail(self):
        pass


class RegexFails(Scenario):
    Given('an ((irregular regex[[')

    @Then('it should fail here')
    def should_fail_here(self):
        self._irregular_regex |should_not_be| None
