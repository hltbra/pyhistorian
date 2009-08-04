# coding: utf-8
from language import StoryLanguage
from termcolor import colored
import sys
import re


TEMPLATE_PATTERN = r'\$[a-zA-Z]\w*'

__all__ = [ 'Story', 'Historia', ]

class InvalidStoryHeader(Exception):
    '''Invalid Story Header!'''

def pluralize(word, size):
    if size >= 2 or size == 0:
        return word+'s'
    return word


class Story(object):
    _as_a = ''
    _i_want_to = ''
    _so_that = ''
    output = sys.stdout
    colored = False
    language = 'en-us'
    scenarios = []

    def __init__(self):
        self._language = StoryLanguage(self.__class__.language)
        self._title = self._create_title_based_on_class_name()
        self._create_header()
        self._scenarios = []
        self._output = self.__class__.output
        self._colored = self.__class__.colored
        self._add_scenarios()

    def _add_scenarios(self):
        for scenario in self.__class__.scenarios:
            self.add_scenario(scenario)

    def _create_title_based_on_class_name(self):
        class_name = self.__class__.__name__
        expanded_cammel_case = class_name[0]
        for char in class_name[1:]:
            if char == char.capitalize():
                expanded_cammel_case += ' ' + char.lower()
            else:
                expanded_cammel_case += char
        return expanded_cammel_case

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

        ran = self._language['ran'].capitalize()
        with_word = self._language['with_word'].lower()
        and_word = self._language['and_word'].lower()
        pending_word = self._language['pending'].lower()
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

    def add_scenario(self, scenario):
        this_scenario = scenario
        if isinstance(scenario, type):
            this_scenario = scenario()
        this_scenario.set_story(self)
        self._set_defined_steps(this_scenario)
        self._scenarios.append(this_scenario)
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

        number_of_scenarios = len(self._scenarios)
        number_of_failures = number_of_errors = number_of_pendings = 0

        for scenario, number in zip(self._scenarios, range(1, len(self._scenarios)+1)):
            self._output.write('\n%s %d: %s\n' % (self._language['scenario'],
                                                number,
                                                scenario.title))
            failures, errors, pendings = scenario.run()
            number_of_failures += len(failures)
            number_of_errors += len(errors)
            number_of_pendings += len(pendings)

        self.output_statistics(number_of_scenarios,
                               number_of_failures,
                               number_of_errors,
                               number_of_pendings)
        

class Historia(Story):
    saida = sys.stdout
    colorido = False
    language = 'pt-br'

    def __init__(self):
        super(Historia, self).__init__()
        self._output = self.__class__.saida
        self._colored = self.__class__.colorido

    adicionar_cenario = Story.add_scenario
    rodar = Story.run
