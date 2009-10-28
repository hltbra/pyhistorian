from language import (StoryLanguage,
                      TEMPLATE_PATTERN,
                      convert_from_cammel_case_to_spaces,
                      format_traceback)
from output import OutputWriter, colored
from steps import pending
import re
import sys
import traceback

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
        self._output_writer = OutputWriter(self._output,
                                           self._language,
                                           self._should_be_colored)

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

    def _run_step(self, step, step_name):
        method, message_template, args = step
        message = self._get_message_with_values_based_on_template(message_template, args)
        if hasattr(method, 'pending'):
            self._pendings.append(method)
            self._output_writer.output_pending_step_line(step_name,
                                                         message,
                                                         self._pending_color)
            return
        try:
            method(self, *args)
            self._output_writer.output_ok_step_line(step_name,
                                                    message,
                                                    'green')
        except AssertionError, e:
            self._failures.append(self._get_traceback_info())
            self._output_writer.output_fail_step_line(step_name,
                                                     message,
                                                     self._failure_color)
        except Exception, e:
            self._errors.append(self._get_traceback_info())
            self._output_writer.output_error_step_line(step_name,
                                                       message,
                                                       self._error_color)

    def __getattr__(self, attr):
        """ first look at the scenario instance,
            and if it does not find the attr, it looks to story's namespace.
            it is useful to ``before_all`` and ``before_each`` story's methods
        """
        if attr not in self.__dict__:
           try:
                return getattr(self.__getattribute__('_story').namespace, attr)
           except AttributeError:
                pass
        return self.__getattribute__(attr)

    def __setattr__(self, attr, value):
        """ first look at the scenario instance,
            and if it does not find the attr, it looks to story's namespace.
            it is useful to ``before_all`` and ``before_each`` story's methods
        """
        if attr not in self.__dict__:
            if getattr(self, '_story', None) and getattr(self._story, 'namespace', None):
                setattr(self._story.namespace, attr, value)
                return
        object.__setattr__(self, attr, value)

    @property
    def title(self):
        return self._title

    def run_steps(self, steps, step_name):
        if len(steps) == 0:
            return
        self._run_step(steps[0], step_name)
        for step in steps[1:]:
            self._run_step(step, 'and')

    def run(self):
        self.run_steps(self._givens, 'given')
        self.run_steps(self._whens, 'when')
        self.run_steps(self._thens, 'then')
        self._output_writer.output_failures_info(self._failures,
                                                 self._failure_color)
        self._output_writer.output_errors_info(self._errors,
                                                 self._error_color)
        return (self._failures, self._errors, self._pendings)
                

class Cenario(Scenario):
    """Portuguese translation"""

