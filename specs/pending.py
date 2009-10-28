'''
    >>> SpecifyingWithPendingStuff.run()
    True
    >>> colored("""    Given this step is written with no implementation   ... PENDING
    ... """, color='blue') in my_output.getvalue()
    True

    >>> "Ran 1 scenario with 0 failures, 0 errors and 1 pending step" in my_output.getvalue()
    True

    >>> SpecifyingPendingsWithNoDecorators.run()
    True
    >>> print second_output.getvalue()
    Story: Specifying pendings with no decorators
      As a DSL user
      I want to avoid using pending decorator
      So that is is more fluent
    <BLANKLINE>
      Scenario 1: Pending without decorators
        Given I don't write the implementation and this pass is not defined   ... PENDING
        Then it runs as pending (both Given and Then)   ... PENDING
    <BLANKLINE>
      Ran 1 scenario with 0 failures, 0 errors and 2 pending steps
    <BLANKLINE>

'''

from pyhistorian import (Story,
                         Scenario,
                         Given,
                         When,
                         Then,
                         pending)
from cStringIO import StringIO
from pyhistorian.output import colored

my_output = StringIO()
second_output = StringIO()

class SpecifyingWithPendingStuff(Story):
    """As a programmer that writes stories with the stakeholder
       I want to be able to mark steps as pending
       So that the stories and scenarios can be written and later implemented"""
    output = my_output
    colored = True
    scenarios = ('GivenIsPending',)


class GivenIsPending(Scenario):
    @pending
    @Given('this step is written with no implementation')
    def no_implementation(self):
        pass

    @Then('the given step is marked as pending')
    def given_is_pending(self):
        pass

class SpecifyingPendingsWithNoDecorators(Story):
    """As a DSL user
       I want to avoid using pending decorator
       So that is is more fluent"""
    scenarios = ('PendingWithoutDecorators',)
    colored = False
    output = second_output

class PendingWithoutDecorators(Scenario):
    Given("I don't write the implementation and this pass is not defined")
    Then('it runs as pending (both Given and Then)')
