'''
>>> story.run() # see, no output
True
>>> print string_io.getvalue()
Story: Different stream feature
As a pyhistorian commiter
I want to add StringIO support
So that output can be redirected to anywhere
<BLANKLINE>
Scenario 1: Using StringIO as output stream
  Given I do not want to output at stdout   ... OK
  When I output any message   ... OK
  Then it should be written in my StringIO object   ... OK
<BLANKLINE>
Ran 1 scenario with 0 failures, 0 errors and 0 pending steps
<BLANKLINE>
'''

from pyhistorian import *
from cStringIO import *

string_io = StringIO()

class StringIOScenario(Scenario):
    """Using StringIO as output stream"""
    @Given('I do not want to output at stdout')
    def nothing(self):
        pass

    @When('I output any message')
    def nothing2(self):
        pass

    @Then('it should be written in my StringIO object')
    def nothing3(self):
        pass

class DifferentStreamFeature(Story):
    """As a pyhistorian commiter
       I want to add StringIO support
       So that output can be redirected to anywhere"""
    output = string_io
    colored = False
    scenarios = [StringIOScenario]

story = DifferentStreamFeature()

