A BDD tool for writing specifications using Given-When-Then template
====================================================================

The goal of *pyhistorian* is to write an internal Given-When-Then template using Python.
The ideas came from JBehave, RBehave, Cucumber and others.

It's possible to write your stories in English and Portuguese, choose your preferred.

A good example of use ``[en-us, by default]`` follows (call this file *calculator.py*)

::
    
    from should_dsl import *
    from pyhistorian import *
    
    class Calculator(object):
        def sum(self, n1, n2):
            return n1+n2
    
    class SumScenario(Scenario):
        @Given('I have a calculator')
        def set_my_calculator(self):
            self.calculator = Calculator()
    
        @When('I enter with 1 + 1')
        def sum_one_to_one(self):
            self.sum = self.calculator.sum(1, 1)
    
        @Then('I have 2 as result')
        def two_as_result(self):
            self.sum |should_be.equal_to| 2
    
    if __name__ == '__main__':
        calculator_story = Story(title='Specifying my new calculator',
                                 as_a='lazy mathematician',
                                 i_want_to='rest my mind',
                                 so_that="I don't waste my time thinking")
        sum_scenario = SumScenario('Sum of 1 and 1')
        (calculator_story.add_scenario(sum_scenario)
                         .run())


Running:

::

    $ python calculator.py 
    Story: Specifying my new calculator
    As a lazy mathematician
    I want to rest my mind
    So that I don't waste my time thinking

    Scenario 1: Sum of 1 and 1
      Given I have a calculator   ... OK
      When I enter with 1 + 1   ... OK
      Then I have 2 as result   ... OK


pyhistorian is at github.com
----------------------------
Due to DVCS I moved pyhistorian from `Google Gode <http://code.google.com/p/pyhistorian>`_ to `github.com <http://github.com/hugobr/pyhistorian>`_. 

You can get it at `here <http://github.com/hugobr/pyhistorian>`_:

http://github.com/hugobr/pyhistorian
