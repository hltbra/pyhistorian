"""
    >>> StoryWithModuleScenarios.run()
    True
    >>> print output.getvalue()
    Story: Story with module scenarios
      As a lazy man
      I want to avoid typing what scenarios I want in my story
      So that they are found in the module
    <BLANKLINE>
      Scenario 1: First scenario
        Then it says "Hi!"   ... OK
    <BLANKLINE>
      Scenario 2: Second scenario
        Then it is the second scenario   ... OK
    <BLANKLINE>
      Ran 2 scenarios with 0 failures, 0 errors and 0 pending steps
    <BLANKLINE>

"""
from pyhistorian import Story, Scenario, Then
from cStringIO import StringIO

output = StringIO()

class StoryWithModuleScenarios(Story):
    """As a lazy man
       I want to avoid typing what scenarios I want in my story
       So that they are found in the module"""
    output = output
    colored = False
       

class FirstScenario(Scenario):
    @Then('it says "Hi!"')
    def say_hi(self):
        return 'Hi!'

class SecondScenario(Scenario):
    @Then('it is the second scenario')
    def foo(self):
        pass
