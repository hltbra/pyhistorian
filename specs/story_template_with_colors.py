'''
    >>> StoryTemplateWithColors.run()
    True
    >>> yellow_colored("""Story: Story template with colors
    ... """) in output.getvalue()
    True
    >>> yellow_colored("""  In order to avoid distractions
    ... """) in output.getvalue()
    True
    >>> yellow_colored("""  As a distracted person
    ... """) in output.getvalue()
    True
    >>> yellow_colored("""  I want to color the story template
    ... """) in output.getvalue()
    True

    >>> yellow_colored("""
    ...   Scenario 1: Black color
    ... """) in output.getvalue()
    True

    >>> yellow_colored("""
    ...   Ran 1 scenario with 0 failures, 0 errors and 0 pending steps
    ... """) in output.getvalue()
    True
'''
from pyhistorian.output import colored
from pyhistorian import Story, Scenario, Then
from cStringIO import StringIO


output = StringIO()

def yellow_colored(msg):
    return colored(msg, 'yellow')


class StoryTemplateWithColors(Story):
    """In order to avoid distractions
    As a distracted person
    I want to color the story template"""

    output = output
    template_color = 'yellow'

class BlackColor(Scenario):
    pass
