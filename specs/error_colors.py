'''
    >>> StoryWithBlueColorsToErrors.run()
    >>> blue_colored("""    Then it will be blue   ... ERROR
    ... """) in output.getvalue()
    True

    >>> blue_colored("""
    ...   Errors:
    ... """) in output.getvalue()
    True
    >>> error_msg = """    File "/home/hugo/pyhistorian/src/specs/error_colors.py", line 40, in do_error
    ...       raise Exception("an error occurred!")
    ...     Exception: an error occurred!
    ... 
    ... """
    >>> blue_colored(error_msg) in output.getvalue()
    True
'''
from pyhistorian import *
from pyhistorian.output import colored
from cStringIO import StringIO

output = StringIO()

def blue_colored(msg):
    return colored(msg, 'blue')


class StoryWithBlueColorsToErrors(Story):
    """In order to avoid distractions
    As a distracted person
    I want to change errors colors"""

    error_color = 'blue'
    output = output

class ScenarioWithBlueErrors(Scenario):
    @Then('it will be blue')
    def do_error(self):
        raise Exception("an error occurred!")
