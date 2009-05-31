'''Adding support to termcolor.
Failures and errors are red and sucessful is green.


>>> colored_output = """Story: Support to termcolor
... As a pyhistorian commiter
... I want to have support to colored output
... So that the output becomes more readable
... 
... Scenario 1: Green color
... """+green_output+"""
... Scenario 2: Red color
... """+red_output+"""
... Scenario 3: Green and Red colors
... """+green_and_red_output

>>> output.getvalue() == colored_output
True

'''

from pyhistorian import *
from should_dsl import *
from cStringIO import StringIO
from termcolor import colored

class GreenScenario(Scenario):
    @Given('I want my output colored and it pass')
    def nothing(self):
        pass

    @Then('I have green messages')
    def nothing2(self):
        pass

class RedScenario(Scenario):
    @Given('I want my output colored and it fails')
    def fail1(self):
         'this scenario' |should_be| 'red colored'

    @Then('I have red messages')
    def fail2(self):
        'this fail color' |should_be| 'red'


class GreenAndRedScenario(Scenario):
   @Given('I want my output colored (green and red)')
   def nothing(self):
       pass

   @Then('I have green message')
   def green_message(self):
       pass

   @Then('I have red message')
   def red_message(self):
       'this step' |should_be| 'red'


def red_colored(text):
    return colored(text, color='red')

def green_colored(text):
    return colored(text, color='green')

output = StringIO()
story = Story('Support to termcolor',
              as_a='pyhistorian commiter',
              i_want_to='have support to colored output',
              so_that='the output becomes more readable',
              output=output,
              colored=True)

(story.add_scenario(GreenScenario('Green color'))
      .add_scenario(RedScenario('Red color'))
      .add_scenario(GreenAndRedScenario('Green and Red colors'))
      .run())

green_output = green_colored('\
  Given I want my output colored and it pass   ... OK\n')+ \
  green_colored('\
  Then I have green messages   ... OK\n')

red_output = red_colored('\
  Given I want my output colored and it fails   ... FAIL\n')+ \
  red_colored('\
  Then I have red messages   ... FAIL\n') +\
  red_colored('\n\nFails:\n')+\
  red_colored('\
   this scenario is not red colored\n')+\
  red_colored('\
   this fail color is not red\n')

green_and_red_output = green_colored('\
  Given I want my output colored (green and red)   ... OK\n')+\
  green_colored('\
  Then I have green message   ... OK\n') + \
  red_colored('\
  And I have red message   ... FAIL\n') +\
  red_colored('\n\nFails:\n') + \
  red_colored('\
   this step is not red\n')

