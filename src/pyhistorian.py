# coding: utf-8
#from should_dsl import DSLObject as _
from language import StoryLanguage
import sys
import re


TEMPLATE_PATTERN = r'\$[a-zA-Z]\w*'

class Step(object):
    '''Step is a baseclass for step directives'''

    name = 'step'

    def __init__(self, message, *args):
        self._message = message
        self._args = args

    def _set_step_attrs(self, local_attrs):
        for private_step in ['_givens', '_whens', '_thens']:
            if not private_step in local_attrs:
                local_attrs[private_step] = []

    def __call__(self, method=None):
        frame = sys._getframe(1)
        step = self.__class__.name
        self._set_step_attrs(frame.f_locals)
        steps = frame.f_locals['_%ss' % step]
        steps.append((method, self._message, self._args))
        return method

class Given(Step):
    name = 'given'

class When(Step):
    name = 'when'

class Then(Step):
    name = 'then'

class DadoQue(Given):
    '''given in portuguese'''

class Quando(When):
    '''when in portuguese'''

class Entao(Then):
    '''then in portuguese'''


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

    def _set_defined_steps(self, scenario):
        for step in ['_givens', '_whens', '_thens']:
            scenario_steps = getattr(scenario, step)
            for i in range(len(scenario_steps)):
                method, msg, args = scenario_steps[i]
                if method is None:
                    for scenario2 in self._scenarios:
                        ok = False
                        for meth2, msg2, args2 in getattr(scenario2, step):
                            msg_pattern = re.sub(TEMPLATE_PATTERN, r'(.*)', msg2)
                            regex = re.match(msg_pattern, msg)
                            if regex:
                                scenario_steps[i] = meth2, msg, regex.groups()
                                ok = True
                                break
                        if ok:
                            break
                        
                    else:
                        def undefined_step(self):
                            raise Exception('%s -- %s' % (self._language['undefined_step'], msg))
                        scenario_steps[i] = undefined_step, msg, args

    def add_scenario(self, scenario):
        scenario.set_story(self)
        self._set_defined_steps(scenario)
        self._scenarios.append(scenario)
        return self

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
        self._title = title or self._language['empty_scenario_title']
        self._errors = []
        self._story = []

    @property
    def title(self):
        return self._title

    def set_story(self, story):
        self._story = story
        self._language = story._language

    def run(self):
        #self._replace_templates()
        self.run_steps(self._givens, 'given')
        self.run_steps(self._whens, 'when')
        self.run_steps(self._thens, 'then')
        if self._errors:
            print '\n\n%ss:' % self._language['fail']
            for error in self._errors:
                if not error.args:
                    error = self._language['exception_thrown'] % str(error.__class__)
                print ' ', error

    def _replace_template(self, message, args):
        for arg in args:
            message = re.sub(TEMPLATE_PATTERN, str(arg), message, 1)
        return message

    def _run_step(self, step, step_name):
        method, message, args = step
        message = self._replace_template(message, args)
        try:
            method(self, *args)
            print '  %s %s   ... OK' % (self._language[step_name], message)
        except Exception, e:
            self._errors.append(e)
            print '  %s %s   ... %s' % (self._language[step_name],
                                    message,
                                    self._language['fail'].upper())
            self._errors.append(e)

    def run_steps(self, steps, step_name):
        if steps == []:
            return False

        self._run_step(steps[0], step_name)
        for step in steps[1:]:
            self._run_step(step, 'and_word')
