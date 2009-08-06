"""
    >>> FormattingExceptions.run()
    >>> print english_output.getvalue()
    Story: Formatting exceptions
    As a user interested in rastreability
    I want to know where the erros come from
    So that I can go to the root of all evil
    <BLANKLINE>
    Scenario 1: Raising an exception
      Then raise an exception with "Hello Motto"   ... ERROR
    <BLANKLINE>
    Errors:
      File ".../tests/traceback_message.py", line ..., in raise_hello_motto
        raise Exception("Hello Motto")
    Exception: Hello Motto
    <BLANKLINE>
    <BLANKLINE>
    Ran 1 scenario with 0 failures, 1 error and 0 steps pending
    <BLANKLINE>

      
"""

#    #>>> language = StoryLanguage('en-us')
#    #>>> try:
#    #...     raise_and_exception_with_message('Hello Motto')
#    #... except:
#    #...     print format_exc(language)
#    File ".../tests/module_with_exception_definition.py", line 2, in raise_and_exception_with_message
#      raise Exception(msg)
#    Exception: Hello Motto
#    #<BLANKLINE>
#
#    #>>> language = StoryLanguage('pt-br')
#    #>>> try:
#    #...     raise_and_exception_with_message('Oi Motto')
#    #... except:
#    #...     print format_exc(language)
#    Arquivo ".../tests/module_with_exception_definition.py", linha 2, em raise_and_exception_with_message
#      raise Exception(msg)
#    Exception: Oi Motto
#    #<BLANKLINE>
#

from pyhistorian.scenario import format_exc
from pyhistorian.language import StoryLanguage
from pyhistorian import Story, Scenario, Then
from module_with_exception_definition import raise_and_exception_with_message
from cStringIO import StringIO

english_output = StringIO()


class FormattingExceptions(Story):
    """As a user interested in rastreability
    I want to know where the erros come from
    So that I can go to the root of all evil"""
    scenarios = ('RaisingAnException',)
    colored = False
    output = english_output

class RaisingAnException(Scenario):
    @Then('raise an exception with "Hello Motto"')
    def raise_hello_motto(self):
        raise Exception("Hello Motto")


#class FormatandoExcecoes(Historia):

