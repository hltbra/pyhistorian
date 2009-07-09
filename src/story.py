# coding: utf-8
from language import StoryLanguage
from termcolor import colored
import sys
import re


TEMPLATE_PATTERN = r'\$[a-zA-Z]\w*'

__all__ = [ 'Story' ]

def pluralize(word, size):
    if size >= 2 or size == 0:
        return word+'s'
    return word


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

    def output_statistics(self, number_of_scenarios,
                                number_of_failures,
                                number_of_errors):
        scenario_word = pluralize(self._language['scenario'],
                                  number_of_scenarios).lower()
        failure_word = pluralize(self._language['failure'],
                                 number_of_failures).lower()
        error_word = pluralize(self._language['error'],
                               number_of_errors).lower()

        ran = self._language['ran'].capitalize()
        with_word = self._language['with_word'].lower()
        and_word = self._language['and_word'].lower()
        self._output.write('\n%s\n' % ' '.join(map(str,
                                                      [ran,
                                                      number_of_scenarios,
                                                      scenario_word,
                                                      with_word,
                                                      number_of_failures,
                                                      failure_word,
                                                      and_word,
                                                      number_of_errors,
                                                      error_word,])))

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

        number_of_scenarios = len(self._scenarios)
        number_of_failures = number_of_errors = 0
        for scenario, number in zip(self._scenarios, range(1, len(self._scenarios)+1)):
            self._output.write('\n%s %d: %s\n' % (self._language['scenario'],
                                                number,
                                                scenario.title))
            failures, errors = scenario.run()
            number_of_failures += len(failures)
            number_of_errors += len(errors)

        self.output_statistics(number_of_scenarios,
                               number_of_failures,
                               number_of_errors)
        

