# coding: utf-8
'''
    >>> colored('green color', 'green') == green_colored('green color')
    True

    >> colored('no colors', 'term') == 'no colors'
    True

    >>> english = StoryLanguage('en-us')
    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, english)
    >>> output_writer.output_ok_step_line('then', 'it works')
    >>> stringio.getvalue() == green_colored("""    Then it works   ... OK
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, english)
    >>> output_writer.output_pending_step_line('then', 'it works')
    >>> stringio.getvalue() == blue_colored("""    Then it works   ... PENDING
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, english)
    >>> output_writer.output_fail_step_line('then', 'it works')
    >>> stringio.getvalue() == red_colored("""    Then it works   ... FAIL
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, english)
    >>> output_writer.output_error_step_line('then', 'it works')
    >>> stringio.getvalue() == red_colored("""    Then it works   ... ERROR
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, english, should_be_colored=False)
    >>> output_writer.output_ok_step_line('then', 'it is not colored')
    >>> print stringio.getvalue()
        Then it is not colored   ... OK
    <BLANKLINE>

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, english)
    >>> output_writer.output_failures_info(['hello', 'world'], 'red')
    >>> stringio.getvalue() == red_colored("""
    ...   Failures:
    ... """) + red_colored("""hello
    ... """) + red_colored("""world
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, english)
    >>> output_writer.output_errors_info(['hello', 'world'], 'red')
    >>> stringio.getvalue() == red_colored("""
    ...   Errors:
    ... """) + red_colored("""hello
    ... """) + red_colored("""world
    ... """)
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, english)
    >>> output_writer.output_errors_info([], 'red')
    >>> stringio.getvalue() == ''
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio, english)
    >>> output_writer.output_failures_info([], 'red')
    >>> stringio.getvalue() == ''
    True

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio,
    ...                              english,
    ...                              should_be_colored=False)
    >>> output_writer.output_statistics(number_of_scenarios=1,
    ...                                 number_of_failures=2,
    ...                                 number_of_errors=3,
    ...                                 number_of_pendings=4)
    >>> print stringio.getvalue()
    <BLANKLINE>
    Ran 1 scenario with 2 failures, 3 errors and 4 pending steps
    <BLANKLINE>

    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio,
    ...                              english,
    ...                              should_be_colored=False)
    >>> output_writer.output_statistics(number_of_scenarios=0,
    ...                                 number_of_failures=1,
    ...                                 number_of_errors=1,
    ...                                 number_of_pendings=1)
    >>> print stringio.getvalue()
    <BLANKLINE>
    Ran 0 scenarios with 1 failure, 1 error and 1 pending step
    <BLANKLINE>

    >>> portuguese = StoryLanguage('pt-br')
    >>> stringio = StringIO()
    >>> output_writer = OutputWriter(stringio,
    ...                              portuguese,
    ...                              should_be_colored=True)
    >>> output_writer.output_statistics(number_of_scenarios=0,
    ...                                 number_of_failures=1,
    ...                                 number_of_errors=1,
    ...                                 number_of_pendings=1,
    ...                                 color='green')
    >>> stringio.getvalue() == green_colored("""
    ...   Rodou 0 cenários com 1 falha, 1 erro e 1 passo pendente
    ... """)
    True
'''

from pyhistorian.language import StoryLanguage
from pyhistorian.output import OutputWriter, colored
from cStringIO import StringIO

def green_colored(msg):
    return colored(msg, 'green')

def blue_colored(msg):
    return colored(msg, 'blue')

def red_colored(msg):
    return colored(msg, 'red')
