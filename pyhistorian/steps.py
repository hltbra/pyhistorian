import sys

class Step(object):
    '''Step is a baseclass for step directives'''

    name = 'step'

    def __init__(self, message, *args):
        self._message = message
        self._args = args
        self._context = sys._getframe(1)
        self._set_step_attrs(self._context.f_locals)
        step = self.__class__.name
        self._steps = self._context.f_locals['_%ss' % step]
        self._steps.append((None, self._message, self._args))

    def _set_step_attrs(self, local_attrs):
        """this method set _givens, _whens and _thens to the class,
        because the steps are called while the class is been defined"""
        attr_name = '_%ss' % self.name
        if not attr_name in local_attrs:
            local_attrs[attr_name] = []

    def __call__(self, method=None):
        del self._steps[-1]
        self._steps.append((method, self._message, self._args))
        return method


# english steps
class Given(Step):
    name = 'given'

class When(Step):
    name = 'when'

class Then(Step):
    name = 'then'


# portuguese steps
class DadoQue(Given):
    '''given in portuguese'''

class Quando(When):
    '''when in portuguese'''

class Entao(Then):
    '''then in portuguese'''


def pending(step_method):
    '''mark a step method as pending'''
    step_method.pending = True
    return step_method
