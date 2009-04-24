from should_dsl import DSLObject as _

class Step(object):
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
    def __init__(self, title='Empty title'):
        self._givens = []
        self._whens = []
        self._thens = []
        self._title = title
        # reverse the list because in python
        # the methods are created bottom up
        all_attributes = reversed(self.__class__.__dict__.values())
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
