'''
>>> story.run()
>>> print output.getvalue()
Story: Faked story
As a fake
I want to run a simple story
So that it runs sucessfully and give me a good output
<BLANKLINE>
Scenario 1: Fake Title
  Given I run it   ... OK
  When I type X   ... OK
  Then it shows me X   ... OK
<BLANKLINE>
Ran 1 scenario with 0 failures, 0 errors and 0 steps pending
<BLANKLINE>
'''

from pyhistorian import Story
from cStringIO import StringIO
output = StringIO()

class FakeScenario(object):
    _givens = _whens = _thens = []
    _failures = _errors = _pendings = []
    title = 'Fake Title'

    def set_story(self, story):
        """default interface (should do nothing)"""

    def run(self):
        output.write('  Given I run it   ... OK\n')
        output.write('  When I type X   ... OK\n')
        output.write('  Then it shows me X   ... OK\n')
        return (self._failures, self._errors, self._pendings)

fake_scenario = FakeScenario()

class FakedStory(Story):
    """As a fake
       I want to run a simple story
       So that it runs sucessfully and give me a good output"""

story = FakedStory(output=output)
story.add_scenario(fake_scenario)
