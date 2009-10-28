'''
>>> story.run()
True
>>> print output.getvalue()
Story: Faked Story #1
In order to write specifications
As a python developer
I want to write them in Python language
<BLANKLINE>
Scenario 1: Fake scenario
  Given I run it   ... OK
  When I type X   ... OK
  Then it shows me X   ... OK
<BLANKLINE>
Ran 1 scenario with 0 failures, 0 errors and 0 pending steps
<BLANKLINE>
'''

from pyhistorian import Story
from cStringIO import StringIO
output = StringIO()

class FakeScenario(object):
    _givens = _whens = _thens = []
    title = 'Fake scenario'

    def __init__(self, story):
        """default interface (should do nothing)"""

    def run(self):
        output.write('  Given I run it   ... OK\n')
        output.write('  When I type X   ... OK\n')
        output.write('  Then it shows me X   ... OK\n')
        return [], [], []


class FakedStory(Story):
    """In order to write specifications
       As a python developer
       I want to write them in Python language"""
    output = output
    scenarios = [FakeScenario]
    title = 'Faked Story #1'

story = FakedStory()
