from language import (StoryLanguage,
                      TEMPLATE_PATTERN,
                      convert_from_cammel_case_to_spaces,
                      format_traceback)
from termcolor import colored
import re
import sys
import traceback
from steps import pending

__all__ = ['Scenario', 'Cenario',]

class Scenario(object):
    _givens = []
    _whens = []
    _thens = []
    
    @staticmethod
    @pending
    def undefined_step(*args, **kw):
        """it doesn't do anything, is just marked as pending"""

    def __init__(self, story):
        self._title = self._get_title_from_class_name_or_docstring()
        self._story = story
        self._language = story._language
        self._output = story._output
        self._should_be_colored = story.colored
        self._failures = []
        self._errors = []
        self._pendings = []
        self._failure_color = story.failure_color
        self._error_color = story.error_color
        self._pending_color = story.pending_color

    def _get_title_from_class_name_or_docstring(self):
        """returns the docstring if defined or
           the class name converted from cammel case to spaces"""
        return self.__doc__ or\
               convert_from_cammel_case_to_spaces(self.__class__.__name__)

    def _colored(self, message, color):
        """returns message colored with color
           if the scenario is allowed to use colors"""
        if self._should_be_colored:
            return colored(message, color)
        return message

    def _output_problems_info(self, problems, problem_type, color):
        """outputs problems information, like failures and its traceback"""
        self._output.write(self._colored('\n%ss:\n' % 
                                self._language[problem_type],
                                color=color))
        for problem in problems:
            self._output.write(self._colored('%s\n' % problem,
                                                      color=color))

    def _output_failures_info(self):
        """outputs failures and its traceback"""
        if self._failures:
            self._output_problems_info(self._failures,
                                       'failure',
                                       self._failure_color)

    def _output_errors_info(self):
        """outputs errors and its traceback"""
        if self._errors:
            self._output_problems_info(self._errors,
                                       'error',
                                       self._error_color)
    
    def _get_message_with_values_based_on_template(self, message, args):
        """returns a message based on a template and values:
           message_template -> Hello (.+)!
           values -> [World]
           message returned -> Hello World!"""
        for arg in args:
            message = re.sub(TEMPLATE_PATTERN, str(arg), message, 1)
        return message

    def _get_traceback_info(self):
        """this method is like traceback.format_exc,
        but it internationalizates the phrase and
        it doesn't need parameters"""
        exc, value, tb = sys.exc_info()
        return format_traceback(exc, value, tb, self._language)

    def _output_step_line_by_type(self, step_name, message, type_name, color):
        """this method is responsible for the template of step line output,
           it shows the step line and info about it, like ``... OK``"""
        self._output.write(self._colored('  %s %s   ... %s\n' % (self._language[step_name],
                                         message,
                                         self._language[type_name].upper()),
                                         color=color))

    def _output_pending_step_line(self, step_name, message):
        self._output_step_line_by_type(step_name,
                                       message,
                                       'pending',
                                       self._pending_color)

    def _output_ok_step_line(self, step_name, message):
        self._output_step_line_by_type(step_name, message, 'ok', 'green')

    def _output_fail_step_line(self, step_name, message):
        self._output_step_line_by_type(step_name,
                                       message,
                                       'fail',
                                       self._failure_color)
 
    def _output_error_step_line(self, step_name, message):
        self._output_step_line_by_type(step_name,
                                       message,
                                       'error',
                                       self._error_color)

    def _run_step(self, step, step_name):
        method, message_template, args = step
        message = self._get_message_with_values_based_on_template(message_template, args)
        if hasattr(method, 'pending'):
            self._pendings.append(method)
            self._output_pending_step_line(step_name, message)
            return
        try:
            method(self, *args)
            self._output_ok_step_line(step_name, message)
        except AssertionError, e:
            self._failures.append(self._get_traceback_info())
            self._output_fail_step_line(step_name, message)
        except Exception, e:
            self._errors.append(self._get_traceback_info())
            self._output_error_step_line(step_name, message)

    @property
    def title(self):
        return self._title

    def run(self):
        self.run_steps(self._givens, 'given')
        self.run_steps(self._whens, 'when')
        self.run_steps(self._thens, 'then')
        self._output_failures_info()
        self._output_errors_info()
        return (self._failures, self._errors, self._pendings)
                
    def run_steps(self, steps, step_name):
        if len(steps) == 0:
            return
        self._run_step(steps[0], step_name)
        for step in steps[1:]:
            self._run_step(step, 'and')

class Cenario(Scenario):
    """Portuguese translation"""

