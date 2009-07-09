#!/usr/bin/env python
# coding: utf-8

import doctest
import os
from pyhistorian import language
from pyhistorian import suite
from pyhistorian.tests import run_tests

FLAGS = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS

if __name__ == '__main__':
    run_tests()
    for module in [language, suite]:
        doctest.testmod(module,
                    optionflags=FLAGS,)
