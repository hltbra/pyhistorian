'''
>>> EmptyStory.run()
True
>>> print new_scenario_output.getvalue()
Story: Empty story
As a programmer
I want to write this DSL
So that I test this new stuff
<BLANKLINE>
Scenario 1: First scenario
  Given I test it   ... OK
  When I say OK   ... OK
It's done!
  Then It's done   ... OK
<BLANKLINE>
Ran 1 scenario with 0 failures, 0 errors and 0 pending steps
<BLANKLINE>


>>> SecondStory.run()
True
>>> print template_output.getvalue()
Story: Second story
As a programmer
I want to write a test
So that I can become happy
<BLANKLINE>
Scenario 1: Template scenario
  Given I have a calculator   ... OK
  When I sum 1 to 1   ... OK
  Then the result is 2   ... OK
<BLANKLINE>
Ran 1 scenario with 0 failures, 0 errors and 0 pending steps
<BLANKLINE>

>>> two_different_scenarios_story.run()
True
>>> print two_different_scenarios_output.getvalue()
Story: Running two different scenarios
As a programmer
I want to put two different scenarios in a story
So that it run all right
<BLANKLINE>
Scenario 1: First scenario
  Given I test it   ... OK
  When I say ... OK
It's done!
  Then It's done   ... OK
<BLANKLINE>
Scenario 2: Template scenario
  Given I have a calculator   ... OK
  When I sum 1 to 1   ... OK
  Then the result is 2   ... OK
<BLANKLINE>
Ran 2 scenarios with 0 failures, 0 errors and 0 pending steps
<BLANKLINE>


>>> third_scenario_story.run()
True
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
Ran 1 scenario with 0 failures, 0 errors and 0 pending steps
<BLANKLINE>


>>> fail_story.run()
False
>>> print fail_scenario_output.getvalue()
Story: Failures
As a x
I want to y
So that z
<BLANKLINE>
Scenario 1: Failing scenario
  Given I wanna see FAILS, ERRORS and OKs   ... OK
  When I put a failing spec   ... FAIL
  And I put an error spec   ... ERROR
  And I raise an empty exception   ... ERROR
  Then I see one FAIL and two ERRORs in my output   ... OK
<BLANKLINE>
Failures:
  File ".../specs/scenario.py", line ..., in failing_spec
    ZeroDivisionError |should_not_be.thrown_by| divide_one_by_zero
  File ".../should_dsl.py", line 25, in __or__
    return self._check_expectation()
  File ".../should_dsl.py", line ..., in _check_expectation
  ...
  ShouldNotSatisfied: ...ZeroDivisionError... is thrown by <function divide_one_by_zero at ...>
<BLANKLINE>
<BLANKLINE>
Errors:
  File ".../specs/scenario.py", line ..., in an_error_spec
    raise Exception( 'raising Exception!' )
  Exception: raising Exception!
<BLANKLINE>
  File ".../specs/scenario.py", line ..., in raise_empty_exception
    raise Exception
  Exception
<BLANKLINE>
<BLANKLINE>
Ran 1 scenario with 1 failure, 2 errors and 0 pending steps
<BLANKLINE>
'''


from pyhistorian import *
from should_dsl import *
from cStringIO import StringIO


class FirstScenario(Scenario):
    @Given('I test it')
    def i_test_it(self):
        self.first_state = "it's been tested!"

    @When('I say OK')
    def i_say_ok(self):
         self.second_state = 'I have said OK'

    @Then("It's done")
    def its_done(self):
        self._output.write("It's done!\n")
        self.first_state |should_be.equal_to| "it's been tested!"
        self.second_state |should_be.equal_to| 'I have said OK'

new_scenario_output = StringIO()

class EmptyStory(Story):
    """As a programmer
       I want to write this DSL
       So that I test this new stuff"""
    output = new_scenario_output
    colored = False
    scenarios = [FirstScenario]


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

template_output = StringIO()

class SecondStory(Story):
    """As a programmer
       I want to write a test
       So that I can become happy"""
    output = template_output
    colored = False
    scenarios = [TemplateScenario]


two_different_scenarios_output = StringIO()
class RunningTwoDifferentScenarios(Story):
    """As a programmer
       I want to put two different scenarios in a story
       So that it run all right"""
    output = two_different_scenarios_output
    colored = False
    scenarios = (FirstScenario, TemplateScenario)

two_different_scenarios_story = RunningTwoDifferentScenarios()

class ItIsMyThirdScenario(Scenario):
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

third_scenario_output = StringIO()
class ShowingHowTwoWhensBecomeWhenPlusAnd(Story):
    """As a software developer
       I want to improve my software
       So that everybody loves it"""
    output = third_scenario_output
    colored = False
    scenarios = [ItIsMyThirdScenario]

third_scenario_story = ShowingHowTwoWhensBecomeWhenPlusAnd()

class FailingScenario(Scenario):
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


fail_scenario_output = StringIO()
class Failures(Story):
    """As a x
       I want to y
       So that z"""
    output = fail_scenario_output
    colored = False
    scenarios = [FailingScenario]

fail_story = Failures()
