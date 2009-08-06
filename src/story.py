# coding: utf-8
from language import (StoryLanguage,
                      TEMPLATE_PATTERN,
                      convert_from_cammel_case_to_spaces,)
from termcolor import colored
from scenario import Scenario
from steps import pending
import sys
import re

__all__ = [ 'Story', 'Historia', ]

class InvalidStoryHeader(Exception):
    '''Invalid Story Header!'''

class ScenarioNotFound(Exception):
    '''Scenario not found!'''

def pluralize(word, size):
    if size >= 2 or size == 0:
        return word+'s'
    return word


class Story(object):
    _as_a = ''
    _i_want_to = ''
    _so_that = ''
    output = sys.stdout
    colored = True
    language = 'en-us'
    scenarios = []

    def __init__(self):
        self._language = StoryLanguage(self.__class__.language)
        self._title = convert_from_cammel_case_to_spaces(self.__class__.__name__)
        self._create_header()
        self._scenarios = []
        self._output = self._get_output()
        self._colored = self.__class__.colored
        self._add_scenarios()

    def _get_output(self):
        if type(self.__class__.output) in [str, unicode]:
            return open(self.__class__.output, 'w')
        return self.__class__.output

    def _get_this_class_module(self):
        module_root = __import__(self.__class__.__module__)
        for module in self.__class__.__module__.split('.')[1:]:
            module_root = getattr(module_root, module)
        return module_root

    def _look_for_scenario_in_story_module(self, scenario):
        module = self._get_this_class_module()
        if scenario not in dir(module):
            raise ScenarioNotFound()
        return getattr(module, scenario)

    def _get_scenarios_from_story_module(self):
        module = self._get_this_class_module()
        scenarios = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and Scenario in attr.__bases__:
                scenarios.append(attr)
        return scenarios

    def _add_scenario(self, scenario):
        if scenario.__class__ in [unicode, str]:
            this_scenario_class = self._look_for_scenario_in_story_module(scenario)
            this_scenario = this_scenario_class(self)
        else:
            this_scenario = scenario(self)
        self._set_defined_steps(this_scenario)
        self._scenarios.append(this_scenario)
        return self

    def _add_scenarios(self):
        scenarios = self.__class__.scenarios
        if len(self.__class__.scenarios) == 0:
            scenarios = self._get_scenarios_from_story_module()
        for scenario in scenarios:
                self._add_scenario(scenario)

    def _create_header(self):
        header = filter(None, self.__doc__.split('\n'))

        if len(header) < 3:
            raise InvalidStoryHeader()

        if self._language['as_a'] == 'As a':
            as_a_match = re.match(r'^\s*As an? (.+)', header[0])
        else:
            as_a_match = re.match(r'^\s*%s (.+)' % self._language['as_a'], header[0])
        i_want_to_match = re.match(r'^\s*%s (.+)' % self._language['i_want_to'], header[1])
        so_that_match = re.match(r'^\s*%s (.+)' % self._language['so_that'], header[2])

        if as_a_match and i_want_to_match and so_that_match:
            self._as_a = as_a_match.group(1)
            self._i_want_to = i_want_to_match.group(1)
            self._so_that = so_that_match.group(1)
        else:
            raise InvalidStoryHeader()

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
        @pending
        def undefined_step(self, *args, **kw):
            """it doesn't do anything, is just marked as pending"""
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

    def _close_output_stream(self):
        if type(self._output) == file:
            self._output.close()

    def output_statistics(self, number_of_scenarios,
                                number_of_failures,
                                number_of_errors,
                                number_of_pendings):
        scenario_word = pluralize(self._language['scenario'],
                                  number_of_scenarios).lower()
        failure_word = pluralize(self._language['failure'],
                                 number_of_failures).lower()
        error_word = pluralize(self._language['error'],
                               number_of_errors).lower()
        step_word = pluralize(self._language['step'],
                               number_of_pendings).lower()
        pending_word = self._language['pending'].lower()
        if self._language['pending'].lower() == 'pendente':
            pending_word = pluralize('pendente',
                                        number_of_pendings).lower()

        ran = self._language['ran'].capitalize()
        with_word = self._language['with_word'].lower()
        and_word = self._language['and_word'].lower()
        self._output.write('\n%s\n' % ' '.join(map(str,
                                                      [ran,
                                                      number_of_scenarios,
                                                      scenario_word,
                                                      with_word,
                                                      number_of_failures,
                                                      failure_word+',',
                                                      number_of_errors,
                                                      error_word,
                                                      and_word,
                                                      number_of_pendings,
                                                      step_word,
                                                      pending_word])))

    def show_story_title(self):
        self._output.write('%s: %s\n' % (self._language['story'], self._title))

    def show_header(self):
        if not (self._as_a == self._i_want_to and self._so_that == ''):
            self._output.write('%s %s\n' % (self._language['as_a'], self._as_a))
            self._output.write('%s %s\n' % (self._language['i_want_to'],
                                          self._i_want_to))
            self._output.write('%s %s\n' % (self._language['so_that'], self._so_that))

    @classmethod
    def run(instance_or_class):
        """``run`` can be called with a Story instance or a Story subclass.
           If passed a class, instantiates it"""
        if isinstance(instance_or_class, type):
            instance = instance_or_class()
        else:
            instance = instance_or_class
        instance.show_story_title()
        instance.show_header()

        number_of_scenarios = len(instance._scenarios)
        number_of_failures = number_of_errors = number_of_pendings = 0

        for scenario, number in zip(instance._scenarios, range(1, len(instance._scenarios)+1)):
            instance._output.write('\n%s %d: %s\n' % (instance._language['scenario'],
                                                number,
                                                scenario.title))
            failures, errors, pendings = scenario.run()
            number_of_failures += len(failures)
            number_of_errors += len(errors)
            number_of_pendings += len(pendings)

        instance.output_statistics(number_of_scenarios,
                               number_of_failures,
                               number_of_errors,
                               number_of_pendings)
        instance._close_output_stream()

class Historia(Story):
    saida = sys.stdout
    colorido = True
    language = 'pt-br'
    cenarios = []

    def __init__(self):
        self.__class__.scenarios = self.__class__.cenarios
        self.__class__.colored = self.__class__.colorido
        self.__class__.output = self.__class__.saida
        super(Historia, self).__init__()

    rodar = Story.run
