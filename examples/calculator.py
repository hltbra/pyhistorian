from should_dsl import DSLObject as _
from pyhistorian import *

class Calculator(object):
    def sum(self, n1, n2):
        return n1+n2

    def reduce(self, n1, n2):
        return n1-n2

    def divide(self, n1, n2):
        return n1/n2

    def multiply(self, n1, n2):
        return n1*n2

class SumScenario(Scenario):
    @Given('I have a calculator')
    def set_my_calculator(self):
        self.calculator = Calculator()

    @When('I enter with 1 + 1')
    def sum_one_to_one(self):
        self.sum = self.calculator.sum(1, 1)

    @Then('I have 2 as result')
    def two_as_result(self):
        _(self.sum).should_be.equal_to(2)


class SumAndReduceScenario(Scenario):
    @Given('I have a calculator')
    def set_my_calculator(self):
        self.calculator = Calculator()

    @When('I enter with 1 + 1')
    def one_plus_one(self):
        self.result = self.calculator.sum(1, 1)

    @When('I reduce 3 of the actual result')
    def reduce_three_of_result(self):
        self.result = self.calculator.reduce(self.result, 3)

    @Then('I have -1 as result')
    def get_my_result(self):
        _(self.result).should_be.equal_to(-1)


class DivisionScenario(Scenario):
    @Given('I have a calculator')
    def set_my_calculator(self):
        self.calculator = Calculator()

    @When('I enter with 5 / 2')
    def five_by_two(self):
        self.result = self.calculator.divide(5, 2)

    @Then('I have 2 as result')
    def get_result(self):
        _(self.result).should_be.equal_to(2)


class MultiplyScenario(Scenario):
    @Given('I have a calculator')
    def set_my_calculator(self):
        self.calculator = Calculator()

    @When('I enter with 2 * 3')
    def multiply_two_by_three(self):
        self.result = self.calculator.multiply(2, 3)

    @Then('I have 6 as result')
    def get_result(self):
        _(self.result).should_be.equal_to(6)



if __name__ == '__main__':
    calculator_story = Story(title='Specifying my new calculator',
                             as_a='lazy mathematician',
                             i_want_to='rest my mind',
                             so_that="I don't waste my time thinking")
    sum_scenario = SumScenario('Sum of 1 and 1')
    sum_and_reduce_scenario = SumAndReduceScenario('Sum and Reduce')
    division_scenario = DivisionScenario('Division Scenario')
    multiplication_scenario = MultiplyScenario('Multiplication Scenario')
    calculator_story.add_scenario(sum_scenario)
    calculator_story.add_scenario(sum_and_reduce_scenario)
    calculator_story.add_scenario(division_scenario)
    calculator_story.add_scenario(multiplication_scenario)
    calculator_story.run()
