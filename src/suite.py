import doctest
import unittest
import sys
from cStringIO import StringIO
from story import *
from scenario import *
from steps import *
from should_dsl import *


__all__= ['PyhistorianSuite', ]


class _Failure(object):
    '''
        >>> fail = _Failure(Exception('foo'))
        >>> fail.shortDescription()
        'foo'
        >>> fail2 = _Failure(Exception())
        >>> fail2.shortDescription()
        ''
    '''
    failureException = AssertionError

    def __init__(self, exception):
        self._exception = exception

    def shortDescription(self):
        if len(self._exception.args):
            return self._exception.args[0]
        return ''


class _StoryCase(object):
    def __init__(self, story):
        self._story = story
        self._steps = []
        self._set_step_methods()

    def _set_step_methods(self):
        for scenario in self._story._scenarios:
            for method, message, args in scenario._givens + scenario._whens + scenario._thens:
                self._steps.append(getattr(scenario, method.func_name))

    def run_steps(self, result):
        for step in self._steps:
            result.startTest(step)
            try:
                step()
                result.addSuccess(step)
            except AssertionError, e:
                result.addFailure(_Failure(e), sys.exc_info())
            except Exception, e:
                result.addError(_Failure(e), sys.exc_info())


class PyhistorianSuite(object):
    def __init__(self, *stories):
        self._story_cases = [_StoryCase(story) for story in stories]

    def __call__(self, result):
        for story in self._story_cases:
            story.run_steps(result)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
