'''
    >>> GettingSomeMoney().run()
    True
    >>> output_file = open(output_filename)
    >>> print output_file.read()
    Story: Getting some money
      As a bank user
      I want to get some money
      So that I can pay my bills
    <BLANKLINE>
      Scenario 1: I have U$10 and want to get U$5
        Given I have U$10 at my account   ... PENDING
        When I request U$5   ... PENDING
        Then the machine throws my money   ... PENDING
        And if I request my balance I see U$5   ... PENDING
    <BLANKLINE>
      Ran 1 scenario with 0 failures, 0 errors and 4 pending steps
    <BLANKLINE>
    >>> output_file.close()
    >>> remove(output_filename)
'''

from pyhistorian import (Story,
                         Scenario,
                         Given,
                         When,
                         Then,)
from cStringIO import StringIO
from os.path import dirname, abspath
from os import remove

this_dir = dirname(abspath(__file__))
output_filename = this_dir + '/outputs/money_output.txt'

class GettingSomeMoney(Story):
    """As a bank user
       I want to get some money
       So that I can pay my bills"""
    output = output_filename
    colored = False
    

class IHaveMoney(Scenario):
    """I have U$10 and want to get U$5"""
    Given('I have U$10 at my account')
    When('I request U$5')
    Then('the machine throws my money')
    Then('if I request my balance I see U$5')
