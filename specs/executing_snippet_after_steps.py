'''
    >>> ExecutingSnippetAfterAllScenarios.run()
    True
    >>> print output.getvalue()
    Story: Executing snippet after all scenarios
      As a smart dev
      I want to execute some snippet after scenarios
      So that I can clean the env created by before_steps
    <BLANKLINE>
      Scenario 1: Scenario change name
        Given My name is Gabriel   ... OK
        When I change my name to Joao   ... OK
        Then My name is Joao   ... OK
    <BLANKLINE>
      Ran 1 scenario with 0 failures, 0 errors and 0 pending steps
    <BLANKLINE>
    >>> ExecutingSnippetAfterEachScenario.run()
    True
    >>> print output2.getvalue()
    Story: Executing snippet after each scenario
      As a smart dev
      I want to execute some snippet after each scenario
      So that I can clean the env created by before_steps
    <BLANKLINE>
      Scenario 1: Scenario only to change name
        When I change my name to Joao   ... OK
    <BLANKLINE>
      Ran 1 scenario with 0 failures, 0 errors and 0 pending steps
    <BLANKLINE>
'''


from pyhistorian import *
from should_dsl import *
from cStringIO import StringIO

output = StringIO()
output2 = StringIO()

class ScenarioChangeName(Scenario):
    @Given('My name is Gabriel')
    def name_equal_gabriel(self):
        self.name |should_be.equal_to| "Gabriel"
    
    @When('I change my name to Joao')
    def change_name_to_joao(self):
        self.name = 'Joao'

    @Then('My name is Joao')
    def check_for_hugo(self):
        self.name |should_be.equal_to| 'Joao'

class ExecutingSnippetAfterAllScenarios(Story):
    '''
      As a smart dev
      I want to execute some snippet after scenarios
      So that I can clean the env created by before_steps
    '''
    output = output
    colored = False

    scenarios = [ScenarioChangeName,]

    def before_all(self, context):
        context.name = 'Gabriel'

    def after_all(self, context):
        context.name |should_be.equal_to| 'Joao'

class ScenarioOnlyToChangeName(Scenario):
    
    @When('I change my name to Joao')
    def change_name_to_joao(self):
        self.name |should_be.equal_to| 'Gabriel'
        self.name = 'Joao'

class ExecutingSnippetAfterEachScenario(Story):
    '''
      As a smart dev
      I want to execute some snippet after each scenario
      So that I can clean the env created by before_steps
    '''
    output = output2
    colored = False

    scenarios = [ScenarioOnlyToChangeName,]

    def before_each(self, context):
        context.name = 'Gabriel'

    def after_each(self, context):
        context.name |should_be.equal_to| 'Joao'
