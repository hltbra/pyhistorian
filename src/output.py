from termcolor import colored

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

        self._stream.write(self._colored('\n%ss:\n' %
                                    self._language[problem_type],
                                        color))
        for problem in problems:
            self._stream.write(self._colored('%s\n' % problem,
                                                color))
 
    def _output_step_line(self, step_name, message, status, color):
        self._stream.write(self._colored('  %s %s   ... %s\n' % (
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
