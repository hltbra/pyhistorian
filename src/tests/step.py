'''
>>> sc = myScenario('lol', output=myscenario_output)
>>> sc.run()
>>> sc._givens
[(<function given_1 at ...>, 'given 1', ()), (<function given_0 at ...>, 'given 0', ())]
>>> sc._whens
[(<function when_1 at ...>, 'when 1', ()), (<function when_2 at ...>, 'when 2', ())]
>>> print myscenario_output.getvalue()
  Given given 1   ... OK
  And given 0   ... OK
  When when 1   ... OK
  And when 2   ... OK

'''
from pyhistorian import Step, Scenario
from cStringIO import StringIO

myscenario_output = StringIO()

class myGiven(Step):
    name = 'given'

class myWhen(Step):
    name = 'when'

class myScenario(Scenario):
    @myGiven('given 1')
    def given_1(self):
        pass

    @myGiven('given 0')
    def given_0(self):
        pass

    @myWhen('when 1')
    def when_1(self):
        pass
     
    @myWhen('when 2')
    def when_2(self):
        pass
