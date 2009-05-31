'''
>>> (story
...       .add_scenario(StringIOScenario('StringIO feature'))
...       .run()) # see, no output
>>> print string_io.getvalue()
Story: StringIO feature
As a pyhistorian owner
I want to add StringIO support
So that output can be redirected to anywhere
<BLANKLINE>
Scenario 1: StringIO feature
  Given I do not want to output at stdout   ... OK
  When I output any message   ... OK
  Then it should be written in a StringIO object   ... OK
'''

from pyhistorian import *
from cStringIO import *

string_io = StringIO()

class StringIOScenario(Scenario):
    @Given('I do not want to output at stdout')
    def nothing(self):
        pass

    @When('I output any message')
    def nothing2(self):
        pass

    @Then('it should be written in a StringIO object')
    def nothing3(self):
        pass

story = Story('StringIO feature',
              as_a='pyhistorian owner',
              i_want_to='add StringIO support',
              so_that='output can be redirected to anywhere',
              output=string_io)

