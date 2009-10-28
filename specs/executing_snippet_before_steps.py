'''
    >>> ExecutingSnippetBeforeScenarios.run()
    True
    >>> print output.getvalue()
    Story: Executing snippet before scenarios
      As a smart dev
      I want to execute some snippet before scenarios
      So that I can start something like a browser driver
    <BLANKLINE>
      Scenario 1: First scenario
        Then I have the core developer name: Hugo   ... OK
      Scenario 2: Second scenario
        Then I have not the core developer name, I have "Another name"   ... OK
    <BLANKLINE>
      Ran 2 scenarios with 0 failures, 0 errors and 0 pending steps
    <BLANKLINE>

    >>> ExecutingSnippetBeforeEachScenario.run()
    True
    >>> print output2.getvalue()
    Story: Executing snippet before each scenario
      As a smart dev
      I want to execute some snippet before each scenario
      So that I can reset my loaded data
    <BLANKLINE>
      Scenario 1: Setting value
        Then I have the core developer name: Hugo   ... OK
    <BLANKLINE>
      Scenario 2: No side effects
        Then if I try changing the name it does NOT have effects   ... OK
    <BLANKLINE>
      Ran 2 scenarios with 0 failures, 0 errors and 0 pending steps
    <BLANKLINE>
'''


from pyhistorian import *
from should_dsl import *
from cStringIO import StringIO

output = StringIO()

class ExecutingSnippetBeforeScenarios(Story):
    '''
      As a smart dev
      I want to execute some snippet before scenarios
      So that I can start something like a browser driver
    '''
    output = output
    colored = False

    scenarios = ['FirstScenario', 'SecondScenario',]

    def before_all(self, context):
        context.name = 'Hugo'


class FirstScenario(Scenario):
    @Then('I have the core developer name: Hugo')
    def check_for_hugo(self):
        self.name |should_be.equal_to| 'Hugo'
        self.name = 'Another name'


class SecondScenario(Scenario):
    @Then('I have not the core developer name, I have "Another name"')
    def check_for_another_name(self):
        self.name |should_be.equal_to| 'Another name'
    

output2 = StringIO()

class ExecutingSnippetBeforeEachScenario(Story):
    '''
      As a smart dev
      I want to execute some snippet before each scenario
      So that I can reset my loaded data
    '''
    output = output2
    colored = False
    scenarios = ['SettingValue', 'NoSideEffects',]

    def before_each(self, context):
        context.name = 'Hugo'

class SettingValue(Scenario):
    @Then('I have the core developer name: Hugo')
    def check_for_hugo(self):
        self.name |should_be.equal_to| 'Hugo'
        self.name = 'Another name'

class NoSideEffects(Scenario):
    @Then('if I try changing the name it does NOT have effects')
    def check_still_for_hugo(self):
        self.name |should_be.equal_to| 'Hugo'

