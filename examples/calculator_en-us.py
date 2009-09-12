from should_dsl import *
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


class SpecifyingMyNewCalculator(Story):
    """As a lazy mathematician
       I want to use a calculator
       So that I don't waste my time thinking"""
    colored = True
    template_color = 'yellow'
    scenarios = ['SumScenario', 'SumAndReduceScenario', 'DivisionScenario', 'MultiplyScenario']


class SumScenario(Scenario):
    @Given('I have a calculator')
    def set_my_calculator(self):
        self.calculator = Calculator()

    @When('I enter with 1 + 1')
    def sum_one_to_one(self):
        self.result = self.calculator.sum(1, 1)

    @Then('I have $value as result', '2')
    def get_result(self, value):
        self.result |should_be| int(value)


class SumAndReduceScenario(Scenario):
    Given('I have a calculator')

    When('I enter with 1 + 1')

    @When('I reduce 3 of the actual result')
    def reduce_three_of_result(self):
        self.result = self.calculator.reduce(self.result, 3)

    Then('I have -1 as result')


class DivisionScenario(Scenario):
    Given('I have a calculator')

    @When('I enter with 5 / 2')
    def five_by_two(self):
        self.result = self.calculator.divide(5, 2)

    Then('I have 2 as result')


class MultiplyScenario(Scenario):
    Given('I have a calculator')

    @When('I enter with 2 * 3')
    def multiply_two_by_three(self):
        self.result = self.calculator.multiply(2, 3)

    Then('I have 6 as result')



if __name__ == '__main__':
    SpecifyingMyNewCalculator.run()
