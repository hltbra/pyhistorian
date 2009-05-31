'''
>>> story.run()
>>> print output.getvalue()
Story: Hacker Story
As a hacker
I want to hack it
So that it is hacked!
<BLANKLINE>
Scenario 1: Fake Title
  Given I run it   ... OK
  When I type X   ... OK
  Then it shows me X   ... OK
<BLANKLINE>

'''

from pyhistorian import Story
from cStringIO import StringIO
output = StringIO()

class FakeScenario(object):
    _givens = _whens = _thens = []
    title = 'Fake Title'

    def set_story(self, story): pass

    def run(self):
        output.write('  Given I run it   ... OK\n')
        output.write('  When I type X   ... OK\n')
        output.write('  Then it shows me X   ... OK\n')
fake_scenario = FakeScenario()

story = Story(title='Hacker Story',
              as_a='hacker',
              i_want_to='hack it',
              so_that='it is hacked!',
              output=output)
story.add_scenario(fake_scenario)

