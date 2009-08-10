'''
    >>> UsingInOrderTo.run()
    >>> print output.getvalue()
    Story: Using in order to
    In order to avoid hard understandable stories
    As a business analyst
    I want to be able to write "In order to/As a/I want to"
    <BLANKLINE>
    Scenario 1: Empty scenario
    <BLANKLINE>
    Ran 1 scenario with 0 failures, 0 erros and 0 steps pending
    <BLANKLINE>

    >>> UsingInOrderTo.run()
    Traceback ...
    ...
    InvalidStoryHeader: Invalid Story Header!
'''

from pyhistorian import *
from cStringIO import StringIO

output = StringIO()
output2 = StringIO()

class UsingInOrderTo(Story):
    """In order to avoid hard understandable stories
    As a story writer
    I want to be able to write "In order to/As a/I want to\""""
    output = output

class EmptyScenario(Scenario):
    pass

class UsingWrongInOrderTo(Story):
    """In order to don't accept invalid headers
    This line is wrong
    I want to be safe the header is been parsed
    """
