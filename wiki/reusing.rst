You don't need to repeat yourself!
==================================
It is possible to reuse steps, you just need to repeat the sentence.

Backing to our calculator example.
----------------------------------
If we are writing a calculator story, we will need a calculator ready in every scenario and nobody likes rewriting sentences and methods definitions.

So a fix was written to it, using the ideas of "directives", from `Martian <http://pypi.python.org/pypi/martian>`_.


Before, we had to writing something like it:
::

    class Calculator(object):
        def sum(self, n1, n2):
            return n1+n2

        def reduce(self, n1, n2):
            return n1-n2

    class SumScenario(Scenario):
        @Given('I have a calculator')
        def set_my_calculator(self):
            self.calculator = Calculator()

        @When('I enter with 1 + 1')
        def sum_one_to_one(self):
            self.result = self.calculator.sum(1, 1)

        @Then('I have 2 as result')
        def get_result(self):
            self.result |should_be.equal_to| 2


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
        def get_result(self):
            self.result |should_be.equal_to| -1


    calculator_story = Story(title='Reusing steps',
                             as_a='smart story writer',
                             i_want_to='write less',
                             so_that="I don't waste repeating myself")

    sum_scenario = SumScenario('Sum of 1 and 1')
    sum_and_reduce_scenario = SumAndReduceScenario('Sum and Reduce')
    (calculator_story
                    .add_scenario(sum_scenario)
                    .add_scenario(sum_and_reduce_scenario)
                    .run())

But now - with the idea of directives implemented - we don't need that rewriting, we can do something like this:
::

    class Calculator(object):
        def sum(self, n1, n2):
            return n1+n2

        def reduce(self, n1, n2):
            return n1-n2

    class SumScenario(Scenario):
        @Given('I have a calculator')
        def set_my_calculator(self):
            self.calculator = Calculator()

        @When('I enter with 1 + 1')
        def sum_one_to_one(self):
            self.result = self.calculator.sum(1, 1)

        @Then('I have $result as result', 2)
        def get_result(self, result):
            self.result |should_be.equal_to| result


    class SumAndReduceScenario(Scenario):
        Given('I have a calculator')

        When('I enter with 1 + 1')

        @When('I reduce 3 of the actual result')
        def reduce_three_of_result(self):
            self.result = self.calculator.reduce(self.result, 3)

        Then('I have -1 as result')


    calculator_story = Story(title='Reusing steps',
                             as_a='smart story writer',
                             i_want_to='write less',
                             so_that="I don't waste repeating myself")

    sum_scenario = SumScenario('Sum of 1 and 1')
    sum_and_reduce_scenario = SumAndReduceScenario('Sum and Reduce')
    (calculator_story
                    .add_scenario(sum_scenario)
                    .add_scenario(sum_and_reduce_scenario)
                    .run())

Much better, ah?!
-----------------

You just need to pay attention that every directive looks up in the story for methods, so you could not add ``SumAndReduceScenario`` scenario before ``SumScenario`` in the latter case, because ``SumAndReduceScenario`` looks up in ``SumScenario`` behind the scenes.
