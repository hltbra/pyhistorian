'''
    >>> story.run()
    >>> colored("""  Given this step is written with no implementation   ... PENDING
    ... """, color='blue') in my_output.getvalue()
    True

    >>> "Ran 1 scenario with 0 failures, 0 errors and 1 step pending" in \
                                                        my_output.getvalue()
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

class SpecifyingWithPendingStuff(Story):
    """As a programmer that writes stories with the stakeholder
       I want to be able to mark steps as pending
       So that the stories and scenarios can be written and later implemented"""

my_output = StringIO()
story = SpecifyingWithPendingStuff(output=my_output,
                                   colored=True)

scenario_with_pending_given = ScenarioWithPendingGiven('Given is pending')
story.add_scenario(scenario_with_pending_given)
