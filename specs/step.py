'''
>>> story = MyStory()
>>> story.run()
True
>>> print myscenario_output.getvalue()
Story: My story
In order to check the steps order
As a story writer
I want to see "given 1" before "given 0"
<BLANKLINE>
Scenario 1: my scenario
  Given given 1   ... OK
  And given 0   ... OK
  When when 1   ... OK
  And when 2   ... OK
<BLANKLINE>
Ran 1 scenario with 0 failures, 0 errors and 0 pending steps
<BLANKLINE>
'''
from pyhistorian import Step, Scenario, Story
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

class MyStory(Story):
    """In order to check the steps order
       As a story writer
       I want to see "given 1" before "given 0"
    """
    output = myscenario_output
    colored = False
    scenarios = [myScenario]
