# coding: utf-8
from should_dsl import DSLObject as _
from language import StoryLanguage

class Step(object):
    name = 'step'

    def __init__(self, message):
        self._message = message

    def __call__(self, method):
        method._step = self.__class__.name
        method.__doc__ = self.repr() + ' ' + self._message
        return method

    def repr(self):
        return self.__class__.__name__

class Given(Step):
    name = 'given'

class When(Step):
    name = 'when'

class Then(Step):
    name = 'then'

class DadoQue(Step):
    name = 'given'
    def repr(self):
        return 'Dado que'

class Quando(Step):
    name = 'when'

class Entao(Step):
    name = 'then'
    def repr(self):
        return 'Então'

class Story(object):
    def __init__(self, title='',
                       as_a='',
                       i_want_to='',
                       so_that='',
                       language='en-us'):
        self._language = StoryLanguage(language)
        self._title = title or self._language['empty_story_title']
        self._as_a = as_a
        self._i_want_to = i_want_to
        self._so_that = so_that
        self._scenarios = []

    def add_scenario(self, scenario):
        self._scenarios.append(scenario)

    def show_story_title(self):
        print '%s: %s' % (self._language['story'], self._title)

    def show_header(self):
        if not (self._as_a == self._i_want_to and self._so_that == ''):
            print self._language['as_a'], self._as_a
            print self._language['i_want_to'], self._i_want_to
            print self._language['so_that'], self._so_that

    def run(self):
        self.show_story_title()
        self.show_header()
        for scenario, number in zip(self._scenarios, range(1, len(self._scenarios)+1)):
            print '\n%s %d: %s' % (self._language['scenario'], number, scenario.title)
            scenario.run()


class Scenario(object):
    def __init__(self, title='', language='en-us'):
        self._language = StoryLanguage(language)
        self._givens = []
        self._whens = []
        self._thens = []
        self._title = title or self._language['empty_title']
        self._errors = []
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
        if self._errors:
            print '\n\n%ss:' % self._language['fail']
            for error in self._errors:
                if not error.args:
                    error = 'Exception %s was thrown!' % str(error.__class__)
                print ' ', error

    def run_steps(self, steps):
        #if steps == []:
            #return False
        try:
            steps[0]()
            print ' ',  steps[0].__doc__ + '   ... OK'
        except Exception, e:
            self._errors.append(e)
            print ' ',  steps[0].__doc__ + '   ... %s' % self._language['fail'].upper()

        for step in steps[1:]:
            try:
                step()
                print '  %s ' % self._language['and_word'] + ' '.join(step.__doc__.split()[1:]) + '   ... OK'
            except Exception, e:
                print '  %s ' % self._language['and_word'] + ' '.join(step.__doc__.split()[1:]) + '   ... %s' % self._language['fail'].upper()
                self._errors.append(e)
