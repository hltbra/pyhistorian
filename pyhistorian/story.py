# coding: utf-8
from language import (StoryLanguage,
                      TEMPLATE_PATTERN,
                      convert_from_cammel_case_to_spaces,
                      pluralize,)
from scenario import Scenario, Cenario
from output import OutputWriter, colored
import sys
import re


__all__ = [ 'Story', 'Historia', ]


class InvalidStoryHeader(Exception):
    '''Invalid Story Header!'''


class ScenarioNotFound(Exception):
    '''Scenario not found!'''


class Namespace(object):
    pass


class Story(object):
    output = sys.stdout
    colored = True
    language = 'en-us'
    scenarios = []
    template_color = 'term'
    failure_color = 'red'
    error_color = 'red'
    pending_color = 'blue'
    title = ''
    namespace = None

    def __init__(self):
        self._language = StoryLanguage(self.__class__.language)
        self._title = self._get_title()
        self._validate_header()
        self._scenarios = []
        self._output = self._get_output()
        self._output_writer = OutputWriter(self._output,
                                           self._language,
                                           self.colored)
        self._add_scenarios()

    def _get_title(self):
        return self.title or convert_from_cammel_case_to_spaces(self.__class__.__name__)

    def _validate_header(self):
        meaningful_lines = [line.strip() for line in self.__doc__.split('\n')
                                if line.strip()]
        for line in meaningful_lines:
            if not (line.startswith(self._language['as_a']) or\
                    line.startswith(self._language['i_want_to']) or\
                    line.startswith(self._language['so_that']) or\
                    line.startswith(self._language['in_order_to'])):
                raise InvalidStoryHeader('Invalid Story Header!')

    def _get_output(self):
        """return output stream depending on the ``output`` class attribute.
        if ``output`` is a kind of string, it returns an open file stream.
        if not, returns the output itself"""
        if type(self.__class__.output) in [str, unicode]:
            return open(self.__class__.output, 'w')
        return self.__class__.output

    def _get_this_class_module(self):
        """return the class' module object"""
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
        """return all Scenario's subclasses from the story module"""
        module = self._get_this_class_module()
        scenarios = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and \
               (Scenario in attr.__bases__ or \
                Cenario in attr.__bases__) and \
               attr is not Cenario:
                scenarios.append(attr)
        return scenarios

    def _add_scenario(self, scenario):
        """add a scenario based on its value.
        if it is a string, look for it in the story's module,
        if not, instantiate it"""
        if scenario.__class__ in [unicode, str]:
            this_scenario_class = self._look_for_scenario_in_story_module(scenario)
            this_scenario = this_scenario_class(self)
        else:
            this_scenario = scenario(self)
        self._set_defined_steps(this_scenario)
        self._scenarios.append(this_scenario)
        return self

    def _add_scenarios(self):
        """add all scenarios specified in the Story class.
        if not specified any, get all from story's module"""
        scenarios = self.__class__.scenarios
        if len(self.__class__.scenarios) == 0:
            scenarios = self._get_scenarios_from_story_module()
        for scenario in scenarios:
                self._add_scenario(scenario)

    def _find_step_matching_to(self, step, msg_set, args_default):
        """find step matching to ``msg_set`` in all scenarios,
           passing ``args_default``"""
        for scenario in self._scenarios:
            for meth, msg, args in getattr(scenario, step):
                msg_pattern = re.sub(TEMPLATE_PATTERN, r'(.+)', msg)
                msg_pattern = re.escape(msg_pattern)
                msg_pattern = msg_pattern.replace(re.escape(r'(.+)'), r'(.+)')
                regex = re.match(msg_pattern, msg_set)
                if regex:
                    return meth, msg_set, regex.groups()
        return Scenario.undefined_step, msg_set, args_default

    def _set_defined_steps(self, scenario):
        for step in ['_givens', '_whens', '_thens']:
            scenario_steps = getattr(scenario, step)
            for i in range(len(scenario_steps)):
                method, msg, args = scenario_steps[i]
                if method is None:
                    scenario_steps[i] = self._find_step_matching_to(step,
                                                                    msg,
                                                                    args)

    def _close_output_file_stream(self):
        """close output files that are not
           sys.stdout, sys.stderr, sys.stdin"""
        if type(self._output) == file and\
           self._output.fileno() > 3:
            self._output.close()

    def _colored(self, msg, color):
        if self.colored == False:
            return msg
        return colored(msg, color)

    def _show_header(self):
        """shows story's title and feature request, role and motivation"""
        self._output.write(self._colored(
                                '%s: %s\n' % (self._language['story'],
                                              self._title),
                                                  self.template_color))
        for line in [line.strip() for line in self.__doc__.split('\n') if line.strip()]:
            self._output.write(self._colored(
                                '  ' + line + '\n', self.template_color))

    @classmethod
    def run(instance_or_class):
        """``run`` can be called with a Story instance or a Story subclass.
           If passed a class, instantiates it"""
        if isinstance(instance_or_class, type):
            self = instance_or_class()
        else:
            self = instance_or_class
        self._show_header()

        number_of_scenarios = len(self._scenarios)
        number_of_failures = number_of_errors = number_of_pendings = 0

        self.namespace = Namespace()
        self.before_all(self.namespace)
         
        status_code = True
        try:
          for scenario, number in zip(self._scenarios, range(1, len(self._scenarios)+1)):
              self._output.write(self._colored('\n  %s %d: %s\n' % (
                                                  self._language['scenario'],
                                                  number,
                                                  scenario.title),
                                                      self.template_color))
              self.before_each(scenario)
              failures, errors, pendings = scenario.run()
              self.after_each(scenario)
              number_of_failures += len(failures)
              number_of_errors += len(errors)
              number_of_pendings += len(pendings)
              status_code = status_code and len(errors) == 0 and len(failures) == 0

          self._output_writer.output_statistics(number_of_scenarios,
                                 number_of_failures,
                                 number_of_errors,
                                 number_of_pendings,
                                 self.template_color)
          self._close_output_file_stream()
          return status_code
        finally:
          self.after_all(self.namespace)


    def before_all(self, scenario):
        pass

    def before_each(self, scenario):
        pass

    def after_all(self, scenario):
        pass

    def after_each(self, scenario):
        pass


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

    @classmethod
    def rodar(cls):
        return super(Historia, cls).run()
