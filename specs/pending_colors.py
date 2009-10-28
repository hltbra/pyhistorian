'''
    >>> StoryWithRedColorsToPendingStuff.run()
    True
    >>> colored("""    Then it will be red   ... PENDING
    ... """, 'red') in output.getvalue()
    True

'''
from pyhistorian import *
from pyhistorian.output import colored
from cStringIO import StringIO

output = StringIO()

class StoryWithRedColorsToPendingStuff(Story):
    """In order to avoid distractions
    As a distracted person
    I want to change pending colors"""

    pending_color = 'red'
    output = output

class ScenarioWithRedPending(Scenario):
    Then('it will be red')
