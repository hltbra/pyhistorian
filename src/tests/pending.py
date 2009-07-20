'''
    >>> my_output = StringIO()
    >>> scenario_with_pending_given = ScenarioWithPendingGiven(
    ... 'Given is pending')

    >>> story = Story('Specifying with pending stuff',
    ...               as_a='programmer that writes stories with the stakeholder',
    ...               i_want_to='be able to mark steps as pending',
    ...               so_that='the stories and scenarios can be written and '+\
                              'later implemented',
    ...               output=my_output,
    ...               colored=True)
    >>> story.add_scenario(scenario_with_pending_given)
    <...Story object at ...>

    >>> story.run()
    >>> colored("""  Given this step is written with no implementation   ... PENDING
    ... """, color='blue') in my_output.getvalue()
    True

'''

from pyhistorian import (Story,
                         Scenario,
                         Given,
                         When,
                         Then,
                         pending)
from cStringIO import StringIO
from termcolor import colored

class ScenarioWithPendingGiven(Scenario):
    @pending
    @Given('this step is written with no implementation')
    def no_implementation(self):
        pass

    @Then('the given step is marked as pending')
    def given_is_pending(self):
        pass

