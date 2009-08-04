from language import (StoryLanguage,
                      TEMPLATE_PATTERN,
                      convert_from_cammel_case_to_spaces,)
from termcolor import colored
import re
import sys

class Scenario(object):
    _language_code = 'en-us'

    def __init__(self):
        self._language = StoryLanguage(self.__class__._language_code)
        self._title = self._get_title_from_class_name_or_docstring()
        self._failures = []
        self._errors = []
        self._pendings = []
        self._story = []
        self._output = sys.stdout
        self._should_be_colored = False

    def _get_title_from_class_name_or_docstring(self):
        return self.__doc__ or\
               convert_from_cammel_case_to_spaces(self.__class__.__name__)

    def _colored(self, message, color):
        if self._should_be_colored:
            return colored(message, color)
        return message

    @classmethod
    def create_scenario(self, story):
        scenario = self()
        scenario._story = story
        scenario._language = story._language
        scenario._output = story._output
        scenario._should_be_colored = story._colored
        return scenario

    @property
    def title(self):
        return self._title

    def run(self):
        self.run_steps(self._givens, 'given')
        self.run_steps(self._whens, 'when')
        self.run_steps(self._thens, 'then')
        self._output_problem(self._failures, 'fail')
        self._output_problem(self._errors, 'error')
        return (self._failures, self._errors, self._pendings)
                
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
        if getattr(method, 'pending', False):
            self._output.write(self._colored('  %s %s   ... %s\n' % (
                                             self._language[step_name],
                                             message,
                                             self._language['pending'].upper()),
                                            color='blue'))
            self._pendings.append(method)
            return
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

class Cenario(Scenario):
    """Portuguese translation"""
    _language_code = 'pt-br'

