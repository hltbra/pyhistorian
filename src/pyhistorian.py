# coding: utf-8
from language import StoryLanguage
from termcolor import colored
import sys
import re


TEMPLATE_PATTERN = r'\$[a-zA-Z]\w*'

class Step(object):
    '''Step is a baseclass for step directives'''

    name = 'step'

    def __init__(self, message, *args):
        self._message = message
        self._args = args
        self._context = sys._getframe(1)
        self._set_step_attrs(self._context.f_locals)
        step = self.__class__.name
        self._steps = self._context.f_locals['_%ss' % step]
        self._steps.append((None, self._message, self._args))

    def _set_step_attrs(self, local_attrs):
        for private_step in ['_givens', '_whens', '_thens']:
            if not private_step in local_attrs:
                local_attrs[private_step] = []

    def __call__(self, method=None):
        del self._steps[-1]
        self._steps.append((method, self._message, self._args))
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
                       language='en-us',
                       output=sys.stdout,
                       colored=False):
        self._language = StoryLanguage(language)
        self._title = title or self._language['empty_story_title']
        self._as_a = as_a
        self._i_want_to = i_want_to
        self._so_that = so_that
        self._scenarios = []
        self._output = output
        self._colored = colored

    def _convert_to_int(self, args):
        '''returns a new container where each string
           containing just integer (delimited by spaces)
           will be converted to real integers - casting with int().
           what is not an integer, will not be affected'''
        new_args = []
        for arg in args:
            if type(arg) == str:
                if re.search(r'^\s*-?\d+\s*$', arg):
                    arg = int(arg)
            new_args.append(arg)
        return new_args

    def _find_step_matching_to(self, step, msg_set, args_default):
        def undefined_step(self):
            raise Exception('%s -- %s' % (self._language['undefined_step'],
                                          msg))
        for scenario in self._scenarios:
            for meth, msg, args in getattr(scenario, step):
                msg_pattern = re.sub(TEMPLATE_PATTERN, r'(.+?)', msg)
                msg_pattern = re.escape(msg_pattern)
                msg_pattern = msg_pattern.replace(re.escape(r'(.+?)'), r'(.+?)')
                regex = re.match(msg_pattern, msg_set)
                if regex:
                    new_args = self._convert_to_int(regex.groups())
                    return meth, msg_set, new_args
        return undefined_step, msg_set, args_default

    def _set_defined_steps(self, scenario):
        for step in ['_givens', '_whens', '_thens']:
            scenario_steps = getattr(scenario, step)
            for i in range(len(scenario_steps)):
                method, msg, args = scenario_steps[i]
                if method is None:
                    scenario_steps[i] = self._find_step_matching_to(step,
                                                                    msg,
                                                                    args)

    def add_scenario(self, scenario):
        scenario.set_story(self)
        self._set_defined_steps(scenario)
        self._scenarios.append(scenario)
        return self

    def show_story_title(self):
        self._output.write('%s: %s\n' % (self._language['story'], self._title))

    def show_header(self):
        if not (self._as_a == self._i_want_to and self._so_that == ''):
            self._output.write('%s %s\n' % (self._language['as_a'], self._as_a))
            self._output.write('%s %s\n' % (self._language['i_want_to'],
                                          self._i_want_to))
            self._output.write('%s %s\n' % (self._language['so_that'], self._so_that))

    def run(self):
        self.show_story_title()
        self.show_header()
        for scenario, number in zip(self._scenarios, range(1, len(self._scenarios)+1)):
            self._output.write('\n%s %d: %s\n' % (self._language['scenario'],
                                                number,
                                                scenario.title))
            scenario.run()


class Scenario(object):
    def __init__(self, title='', language='en-us', output=sys.stdout):
        self._language = StoryLanguage(language)
        self._title = title or self._language['empty_scenario_title']
        self._errors = []
        self._failures = []
        self._story = []
        self._output = output
        self._should_be_colored = False

    def _colored(self, message, color):
        if self._should_be_colored:
            return colored(message, color)
        return message

    @property
    def title(self):
        return self._title

    def set_story(self, story):
        self._story = story
        self._language = story._language
        self._output = story._output
        self._should_be_colored = story._colored

    def run(self):
        self.run_steps(self._givens, 'given')
        self.run_steps(self._whens, 'when')
        self.run_steps(self._thens, 'then')
        self._output_problem(self._failures, 'fail')
        self._output_problem(self._errors, 'error')
                
    def _output_problem(self, problems, problem_type):
        if problems:
            self._output.write(self._colored('\n\n%ss:\n' %
                                        self._language[problem_type], color='red'))
            for problem in problems:
                if not problem.args:
                    problem = self._language['exception_thrown'] % str(problem.__class__)
                self._output.write(self._colored('   %s\n' % problem,
                                                    color='red'))

    def _replace_template(self, message, args):
        for arg in args:
            message = re.sub(TEMPLATE_PATTERN, str(arg), message, 1)
        return message

    def _run_step(self, step, step_name):
        method, message, args = step
        message = self._replace_template(message, args)
        try:
            method(self, *args)
            self._output.write(self._colored('  %s %s   ... OK\n' % (self._language[step_name],
                                                     message), color='green'))
        except AssertionError, e:
            self._failures.append(e)
            self._output.write(self._colored('  %s %s   ... %s\n' % (self._language[step_name],
                                             message,
                                             self._language['fail'].upper()),
                                             color='red'))
        except Exception, e:
            self._errors.append(e)
            self._output.write(self._colored('  %s %s   ... %s\n' % (self._language[step_name],
                                             message,
                                             self._language['error'].upper()),
                                             color='red'))

    def run_steps(self, steps, step_name):
        if steps == []:
            return False

        self._run_step(steps[0], step_name)
        for step in steps[1:]:
            self._run_step(step, 'and_word')
