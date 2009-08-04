'''
>>> empty_story.run()
>>> print new_scenario_output.getvalue()
Story: Empty story
As a programmer
I want to write this DSL
So that I test this new stuff
<BLANKLINE>
Scenario 1: First Scenario
  Given I test it   ... OK
  When I say OK   ... OK
It's done!
  Then It's done   ... OK
<BLANKLINE>
Ran 1 scenario with 0 failures, 0 errors and 0 steps pending
<BLANKLINE>

>>> new_scenario.first_state
"it's been tested!"

>>> new_scenario.second_state
'I have said OK'


>>> template_story.run()
>>> print template_output.getvalue()
Story: Second story
As a programmer
I want to write a test
So that I can become happy
<BLANKLINE>
Scenario 1: Second Scenario
  Given I have a calculator   ... OK
  When I sum 1 to 1   ... OK
  Then the result is 2   ... OK
<BLANKLINE>
Ran 1 scenario with 0 failures, 0 errors and 0 steps pending
<BLANKLINE>

>>> (two_different_scenarios_story.add_scenario(new_scenario)
...                               .add_scenario(template_scenario)
...                               .run())

>>> print two_different_scenarios_output.getvalue()
Story: Running two different scenarios
As a programmer
I want to put two different scenarios in a story
So that it run all right
<BLANKLINE>
Scenario 1: First Scenario
  Given I test it   ... OK
  When I say ... OK
It's done!
  Then It's done   ... OK
<BLANKLINE>
Scenario 2: Second Scenario
  Given I have a calculator   ... OK
  When I sum 1 to 1   ... OK
  Then the result is 2   ... OK
<BLANKLINE>
Ran 2 scenarios with 0 failures, 0 errors and 0 steps pending
<BLANKLINE>


>>> third_scenario_story.run()
>>> print third_scenario_output.getvalue()
Story: Showing how two whens become when plus and
As a software developer
I want to improve my software
So that everybody loves it
<BLANKLINE>
Scenario 1: It is my third scenario
  Given it is the 3rd scenario   ... OK
  When I do nothing   ... OK
  And I don't know what to do   ... OK
  Then I go refactor this software   ... OK
<BLANKLINE>
Ran 1 scenario with 0 failures, 0 errors and 0 steps pending
<BLANKLINE>


>>> fail_story.run()
>>> print fail_scenario_output.getvalue()
Story: Failures
As a x
I want to y
So that z
<BLANKLINE>
Scenario 1: Failing Scenario
  Given I wanna see FAILS, ERRORS and OKs   ... OK
  When I put a failing spec   ... FAIL
  And I put an error spec   ... ERROR
  And I raise an empty exception   ... ERROR
  Then I see one FAIL and two ERRORs in my output   ... OK
<BLANKLINE>
<BLANKLINE>
Fails:
   ...ZeroDivisionError... is thrown by <function divide_one_by_zero at ...>
<BLANKLINE>
<BLANKLINE>
Errors:
   raising Exception!
   Exception ...Exception... was thrown!
<BLANKLINE>
Ran 1 scenario with 1 failure, 2 errors and 0 steps pending
<BLANKLINE>
'''


from pyhistorian import *
from should_dsl import *
from cStringIO import StringIO


class NewScenario(Scenario):
    @Given('I test it')
    def i_test_it(self):
        self.first_state = "it's been tested!"

    @When('I say OK')
    def i_say_ok(self):
         self.second_state = 'I have said OK'

    @Then("It's done")
    def its_done(self):
        self._output.write("It's done!\n")

new_scenario = NewScenario('First Scenario')
new_scenario_output = StringIO()

class EmptyStory(Story):
    """As a programmer
       I want to write this DSL
       So that I test this new stuff"""

empty_story = EmptyStory(output=new_scenario_output)
empty_story.add_scenario(new_scenario)


class TemplateScenario(Scenario):
    @Given('I have a calculator')
    def i_have_a_calculator(self):
        pass

    @When('I sum 1 to 1')
    def i_sum_number1_to_number2(self):
        self.sum = 1 + 1

    @Then('the result is 2')
    def the_result_is_result(self):
        self.sum |should_be.equal_to| 2

template_scenario = TemplateScenario('Second Scenario')
template_output = StringIO()

class SecondStory(Story):
    """As a programmer
       I want to write a test
       So that I can become happy"""

template_story = SecondStory(output=template_output)
template_story.add_scenario(template_scenario)


two_different_scenarios_output = StringIO()
class RunningTwoDifferentScenarios(Story):
    """As a programmer
       I want to put two different scenarios in a story
       So that it run all right"""

two_different_scenarios_story = RunningTwoDifferentScenarios(
              output=two_different_scenarios_output)

class ThirdScenario(Scenario):
    @Given('it is the 3rd scenario')
    def do_nothing(self):
        pass

    @When('I do nothing')
    def do_nothing_again(self):
        pass
    @When("I don't know what to do")
    def what_should_i_do(self):
        self.what = 'write this software'

    @Then('I go refactor this software')
    def refactor(self):
        pass
third_scenario = ThirdScenario('It is my third scenario')

third_scenario_output = StringIO()
class ShowingHowTwoWhensBecomeWhenPlusAnd(Story):
    """As a software developer
       I want to improve my software
       So that everybody loves it"""
third_scenario_story = ShowingHowTwoWhensBecomeWhenPlusAnd(
              output=third_scenario_output)
third_scenario_story.add_scenario(third_scenario)

class FailScenario(Scenario):
    @Given('I wanna see FAILS, ERRORS and OKs')
    def nothing(self): pass
    
    @When('I put a failing spec')
    def failing_spec(self):
        def divide_one_by_zero(): return 1/0
        ZeroDivisionError |should_not_be.thrown_by| divide_one_by_zero
    @When('I put an error spec')
    def an_error_spec(self):
        raise Exception( 'raising Exception!' )
    @When('I raise an empty exception')
    def raise_empty_exception(self):
        raise Exception

    @Then('I see one FAIL and two ERRORs in my output')
    def where_is_fail(self):
        pass

fail_scenario = FailScenario('Failing Scenario')

fail_scenario_output = StringIO()
class Failures(Story):
    """As a x
       I want to y
       So that z"""

fail_story = Failures(output=fail_scenario_output)
fail_story.add_scenario(fail_scenario)
