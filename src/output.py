from language import pluralize
import termcolor


def colored(msg, color):
    if color == 'term':
        return msg
    return termcolor.colored(msg, color)


class OutputWriter(object):
    def __init__(self, stream, language, should_be_colored=True):
        self._stream = stream
        self._language = language
        self._should_be_colored = should_be_colored

    def _colored(self, msg, color):
        if self._should_be_colored:
            return colored(msg, color)
        return msg

    def _output_problems_info(self, problems, problem_type, color='red'):
        if not problems:
            return

        self._stream.write(self._colored('\n  %ss:\n' %
                                    self._language[problem_type],
                                        color))
        for problem in problems:
            self._stream.write(self._colored('%s\n' % problem,
                                                color))
 
    def _output_step_line(self, step_name, message, status, color):
        self._stream.write(self._colored('    %s %s   ... %s\n' % (
                                      self._language[step_name].capitalize(),
                                      message,
                                      self._language[status].upper()),
                                        color))

    def output_ok_step_line(self, step_name, message, color='green'):
        self._output_step_line(step_name, message, 'ok', color)

    def output_pending_step_line(self, step_name, message, color='blue'):
        self._output_step_line(step_name, message, 'pending', color)
        
    def output_fail_step_line(self, step_name, message, color='red'):
        self._output_step_line(step_name, message, 'fail', color)

    def output_error_step_line(self, step_name, message, color='red'):
        self._output_step_line(step_name, message, 'error', color)

    def output_failures_info(self, problems, color='red'):
        self._output_problems_info(problems, 'failure', color)

    def output_errors_info(self, problems, color='red'):
        self._output_problems_info(problems, 'error', color)

    def output_statistics(self, number_of_scenarios,
                                number_of_failures,
                                number_of_errors,
                                number_of_pendings,
                                color='white'):
        scenario_word = pluralize(self._language['scenario'],
                                  number_of_scenarios).lower()
        failure_word = pluralize(self._language['failure'],
                                 number_of_failures).lower()
        error_word = pluralize(self._language['error'],
                               number_of_errors).lower()
        step_word = pluralize(self._language['step'],
                               number_of_pendings).lower()
        pending_word = self._language['pending'].lower()
        steps_pending = pending_word + ' ' + step_word
        if self._language['pending'].lower() == 'pendente':
            pending_word = pluralize('pendente',
                                        number_of_pendings).lower()
            steps_pending = step_word + ' ' + pending_word

        ran = self._language['ran'].capitalize()
        with_word = self._language['with'].lower()
        and_word = self._language['and'].lower()
        self._stream.write(self._colored('\n  %s\n' % ' '.join(map(str,
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
                                                      steps_pending,])),
                                                          color))
