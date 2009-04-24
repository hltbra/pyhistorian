from should_dsl import DSLObject as _

class Step(object):
    '''

        >>> def hello_world():
        ...    return 'hello world!'
        >>> hello_world = Step('test')(hello_world)
        >>> hello_world.__doc__
        'Step test'
        >>> hello_world._step
        'step'
    '''
    def __init__(self, message):
        self._message = message

    def __call__(self, method):
        method._step = self.__class__.__name__.lower()
        method.__doc__ = method._step.capitalize() + ' ' + self._message
        return method


class Given(Step):
    pass

class When(Step):
    pass

class Then(Step):
    pass


class Story(object):
    '''
        >>> class FakeScenario(object):
        ...     title = 'Fake Title'
        ...
        ...     def run(self):
        ...         print 'Given I run it'
        ...         print 'When I type X'
        ...         print 'Then it shows me X'
        >>> fake_scenario = FakeScenario()

        >>> story = Story(title='Hacker Story',
        ...               as_a='hacker',
        ...               i_want_to='hack it',
        ...               so_that='it is hacked!')
        >>> story.add_scenario(fake_scenario)
        >>> story.run()
        Story: Hacker Story
        As a hacker
        I want to hack it
        So that it is hacked!
        <BLANKLINE>
        Scenario 1: Fake Title
          Given I run it
          When I type X
          Then it shows me X
    '''
    def __init__(self, title='Empty Story',
                       as_a='',
                       i_want_to='',
                       so_that=''):
        self._title = title
        self._as_a = as_a
        self._i_want_to = i_want_to
        self._so_that = so_that
        self._scenarios = []

    def add_scenario(self, scenario):
        self._scenarios.append(scenario)

    def run(self):
        print 'Story: %s' % self._title
        if not (self._as_a == self._i_want_to and self._so_that == ''):
            print 'As a %s\nI want to %s\nSo that %s' % (self._as_a,
                                                         self._i_want_to,
                                                         self._so_that)
        for scenario, number in zip(self._scenarios, range(1, len(self._scenarios)+1)):
            print '\nScenario %d: %s' % (number, scenario.title)
            scenario.run()


class Scenario(object):
    '''
        >>> class NewScenario(Scenario):
        ...     @Given('I test it')
        ...     def i_test_it(self):
        ...         self.first_state = "it's been tested!"
        ...
        ...     @When('I say OK')
        ...     def i_say_ok(self):
        ...          self.second_state = 'I have said OK'
        ...
        ...     @Then("It's done")
        ...     def its_done(self):
        ...         print "It's done!"

        >>> new_scenario = NewScenario('First Scenario')

        >>> story = Story(as_a='programmer',
        ...               i_want_to='write this DSL',
        ...               so_that='I test this new stuff')
        >>> story.add_scenario(new_scenario)

        >>> story.run()
        Story: Empty Story
        As a programmer
        I want to write this DSL
        So that I test this new stuff
        <BLANKLINE>
        Scenario 1: First Scenario
          Given I test it
          When I say OK
          Then It's done
        It's done!

        >>> new_scenario.first_state
        "it's been tested!"

        >>> new_scenario.second_state
        'I have said OK'


        >>> class TemplateScenario(Scenario):
        ...     @Given('I have a calculator')
        ...     def i_have_a_calculator(self):
        ...         pass
        ...
        ...     @When('I sum 1 to 1')
        ...     def i_sum_number1_to_number2(self):
        ...         self.sum = 1 + 1
        ...
        ...     @Then('the result is 2')
        ...     def the_result_is_result(self):
        ...         _(self.sum).should_be.equal_to(2)

        >>> template_scenario = TemplateScenario('Second Scenario')

        >>> template_story = Story(title='Second Test',
        ...                        as_a='programmer',
        ...                        i_want_to='write a test',
        ...                        so_that='I can become happy')
        >>> template_story.add_scenario(template_scenario)
        >>> template_story.run()
        Story: Second Test
        As a programmer
        I want to write a test
        So that I can become happy
        <BLANKLINE>
        Scenario 1: Second Scenario
          Given I have a calculator
          When I sum 1 to 1
          Then the result is 2


        >>> story = Story(title='Running two different scenarios',
        ...               as_a='programmer',
        ...               i_want_to='put two different scenarios in a story',
        ...               so_that='it run all right')
        >>> story.add_scenario(new_scenario)
        >>> story.add_scenario(template_scenario)
        >>> story.run()
        Story: Running two different scenarios
        As a programmer
        I want to put two different scenarios in a story
        So that it run all right
        <BLANKLINE>
        Scenario 1: First Scenario
          Given I test it
          When I say OK
          Then It's done
        It's done!
        <BLANKLINE>
        Scenario 2: Second Scenario
          Given I have a calculator
          When I sum 1 to 1
          Then the result is 2

        >>> class ThirdScenario(Scenario):
        ...     @Given('it is the 3rd scenario')
        ...     def do_nothing(self):
        ...         pass
        ...
        ...     @When('I do nothing')
        ...     def do_nothing_again(self):
        ...         pass
        ...     @When("I don't know what to do")
        ...     def what_should_i_do(self):
        ...         self.what = 'write this software'
        ...
        ...     @Then('I go refactor this software')
        ...     def refactor(self):
        ...         pass
        >>> third_scenario = ThirdScenario('It is my third scenario')

        >>> story = Story(title='Showing how two whens become one when+and',
        ...               as_a='software developer',
        ...               i_want_to='improve my software',
        ...               so_that='everybody loves it')
        >>> story.add_scenario(third_scenario)
        >>> story.run()
        Story: Showing how two whens become one when+and
        As a software developer
        I want to improve my software
        So that everybody loves it
        <BLANKLINE>
        Scenario 1: It is my third scenario
          Given it is the 3rd scenario
          When I do nothing
          And I don't know what to do
          Then I go refactor this software
    '''

    def __init__(self, title='Empty title'):
        self._givens = []
        self._whens = []
        self._thens = []
        self._title = title
        # revert the list because in python
        # the methods are created bottom up
        all_attributes = self.__class__.__dict__.values()[::-1]
        steps = [step for step in all_attributes
                            if getattr(step, '_step', None)]
        for method in steps:
            self.add_step(getattr(self, method.func_name))

    @property
    def title(self):
        return self._title

    def add_step(self, method):
        if method._step == 'given':
            self._add_given(method)
        elif method._step == 'when':
            self._add_when(method)
        elif method._step == 'then':
            self._add_then(method)

    def _add_given(self, given):
        self._givens.append(given)

    def _add_when(self, when):
        self._whens.append(when)

    def _add_then(self, then):
        self._thens.append(then)

    def run(self):
        self.run_steps(self._givens)
        self.run_steps(self._whens)
        self.run_steps(self._thens)

    def run_steps(self, steps):
        print ' ',  steps[0].__doc__
        steps[0]()
        for step in steps[1:]:
            print '  And ' + ' '.join(step.__doc__.split()[1:])
            step()


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
