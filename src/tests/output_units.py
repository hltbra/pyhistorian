'''
    >>> language = StoryLanguage('en-us')
    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, language)
    >>> output_writer.output_ok_step_line('then', 'it works')
    >>> stringio.getvalue() == green_colored("""  Then it works   ... OK
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, language)
    >>> output_writer.output_pending_step_line('then', 'it works')
    >>> stringio.getvalue() == blue_colored("""  Then it works   ... PENDING
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, language)
    >>> output_writer.output_fail_step_line('then', 'it works')
    >>> stringio.getvalue() == red_colored("""  Then it works   ... FAIL
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, language)
    >>> output_writer.output_error_step_line('then', 'it works')
    >>> stringio.getvalue() == red_colored("""  Then it works   ... ERROR
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, language, should_be_colored=False)
    >>> output_writer.output_ok_step_line('then', 'it is not colored')
    >>> print stringio.getvalue()
      Then it is not colored   ... OK
    <BLANKLINE>

'''

from termcolor import colored
from pyhistorian.language import StoryLanguage
from pyhistorian.output import OutputWriter
from cStringIO import StringIO

def green_colored(msg):
    return colored(msg, 'green')

def blue_colored(msg):
    return colored(msg, 'blue')

def red_colored(msg):
    return colored(msg, 'red')
