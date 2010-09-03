'''
    >>> StoryWithBlueColorsToFailures.run()
    False
    >>> blue_colored("""    Then it will be blue   ... FAIL
    ... """) in output.getvalue()
    True

    >>> blue_colored("""
    ...   Failures:
    ... """) in output.getvalue()
    True
    >>> failure_msg = """    File "%s", line ..., in fail
    ...       assert 1 == 2
    ...     AssertionError
    ... 
    ... """ % os.path.abspath(__file__)
    >>> expected_output = "...%s..." % (blue_colored(failure_msg))
    >>> checker.check_output(expected_output, output.getvalue(), doctest.ELLIPSIS)
    True
'''
from pyhistorian import *
from pyhistorian.output import colored
from cStringIO import StringIO
import os
import doctest

output = StringIO()
checker = doctest.OutputChecker()

def blue_colored(msg):
    return colored(msg, 'blue')


class StoryWithBlueColorsToFailures(Story):
    """In order to avoid distractions
    As a distracted person
    I want to change failures colors"""

    failure_color = 'blue'
    output = output

class ScenarioWithBlueFailures(Scenario):
    @Then('it will be blue')
    def fail(self):
        assert 1 == 2
