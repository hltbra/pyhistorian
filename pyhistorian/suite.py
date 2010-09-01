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


class Wrap(unittest.TestCase):
    def __init__(self, step, msg):
        self._step = step
        self._msg = msg

    def __str__(self):
        return self._msg


class _StoryCase(unittest.TestCase):
    def __init__(self, story):
        self._story = story
        self._steps = []
        self._set_step_methods()

    def _set_step_methods(self):
        for scenario in self._story._scenarios:
            for method, message, args in scenario._givens + scenario._whens + scenario._thens:
                func = getattr(scenario, method.func_name)
                self._steps.append((func, message))

    def run(self, result):
        for step, message in self._steps:
            result.startTest(Wrap(step, message))
            try:
                step()
                result.addSuccess(self)
            except AssertionError, e:
                result.addFailure(_Failure(e), sys.exc_info())
            except Exception, e:
                result.addError(_Failure(e), sys.exc_info())
            result.stopTest(self)

    def __str__(self):
        return self._story._title
#        return "%s (%s)" % ('run', unittest._strclass(self.__class__))

##    def __repr__(self):
##        return "<%s testMethod=%s>" % \
##               (_strclass(self.__class__), 'run')
##

#    failureException = AssertionError
#
#    def __init__(self, methodName='runTest'):
#        """Create an instance of the class that will use the named test
#           method when executed. Raises a ValueError if the instance does
#           not have a method with the specified name.
#        """
#        try:
#            self.__testMethodName = methodName
#            testMethod = getattr(self, methodName)
#            self.__testMethodDoc = testMethod.__doc__
#        except AttributeError:
#            raise ValueError, "no such test method in %s: %s" % \
#                  (self.__class__, methodName)
#
#    def setUp(self):
#        "Hook method for setting up the test fixture before exercising it."
#        pass
#
#    def tearDown(self):
#        "Hook method for deconstructing the test fixture after testing it."
#        pass
#
#    def countTestCases(self):
#        return 1
#
#    def defaultTestResult(self):
#        return TestResult()
#
#    def shortDescription(self):
#        """Returns a one-line description of the test, or None if no
#        description has been provided.
#
#        The default implementation of this method returns the first line of
#        the specified test method's docstring.
#        """
#        doc = self.__testMethodDoc
#        return doc and doc.split("\n")[0].strip() or None
#
#    def id(self):
#        return "%s.%s" % (_strclass(self.__class__), self.__testMethodName)
#
#    def __str__(self):
#        return "%s (%s)" % (self.__testMethodName, _strclass(self.__class__))
#
#    def __repr__(self):
#        return "<%s testMethod=%s>" % \
#               (_strclass(self.__class__), self.__testMethodName)
#
#    def run(self, result=None):
#        if result is None: result = self.defaultTestResult()
#        result.startTest(self)
#        testMethod = getattr(self, self.__testMethodName)
#        try:
#            try:
#                self.setUp()
#            except KeyboardInterrupt:
#                raise
#            except:
#                result.addError(self, self.__exc_info())
#                return
#
#            ok = False
#            try:
#                testMethod()
#                ok = True
#            except self.failureException:
#                result.addFailure(self, self.__exc_info())
#            except KeyboardInterrupt:
#                raise
#            except:
#                result.addError(self, self.__exc_info())
#
#            try:
#                self.tearDown()
#            except KeyboardInterrupt:
#                raise
#            except:
#                result.addError(self, self.__exc_info())
#                ok = False
#            if ok: result.addSuccess(self)
#        finally:
#            result.stopTest(self)
#
#    def __call__(self, *args, **kwds):
#        return self.run(*args, **kwds)
#
#    def debug(self):
#        """Run the test without collecting errors in a TestResult"""
#        self.setUp()
#        getattr(self, self.__testMethodName)()
#        self.tearDown()
#

class PyhistorianSuite(unittest.TestSuite):
    def __init__(self, *stories):
        self._tests = [_StoryCase(story) for story in stories]

    def __call__(self, result):
        for story in self._tests:
           story.run(result)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
