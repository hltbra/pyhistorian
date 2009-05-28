When scenarios ran successful
------------------------------
When a scenario runs successfuly it outputs ... OK at the end of each successful step, for example:

::

    Story: Specifying my new calculator
    As a lazy mathematician
    I want to use a calculator
    So that I don't waste my time thinking
    
    Scenario 1: Sum of 1 and 1
      Given I have a calculator   ... OK
      When I enter with 1 + 1   ... OK
      Then I have 2 as result   ... OK



When scenarios fail
===================
When a scenario fail somewhere, due to any kind of exception, it put ... FAIL in the end of step line and outputs the ``Exception`` message in the *Fails* part (in the end of the scenario), for example:

::

    Story: Specifying my new calculator
    As a lazy mathematician
    I want to use a calculator
    So that I don't waste my time thinking

    Scenario 1: Sum of 1 and 1
      Given I have a calculator   ... OK
      When I enter with 1 + 1   ... OK
      Then I have 2 as result   ... FAIL


    Fails:
      2 is not equal to 3


So, the basic idea is to output OK when it is successful and FAIL when it was not successful
--------------------------------------------------------------------------------------------

It's not possible to know where exactly the error occurred (line, statement or expression), but if you write well your stories, you will know where look for and it will be easy to fix.
