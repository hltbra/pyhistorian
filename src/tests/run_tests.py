#!/usr/bin/env python
# coding: utf-8
import doctest
import os
import sys
from pyhistorian import language
from pyhistorian import suite

FLAGS = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
THIS_DIRNAME = os.path.dirname(os.path.abspath(__file__))

def run_all_python_modules_here():
    status = 0
    all_python_files_here = [filename for filename in os.listdir(THIS_DIRNAME)
                                          if filename.endswith('.py')]

    for python_file in all_python_files_here:
        if python_file not in ['run_tests.py', '__init__.py']:
            python_module = __import__(python_file[:-3])
            status = doctest.testmod(python_module, optionflags=FLAGS)[0] or status
    return status

def run_python_modules_outhere():
    status = 0
    for module in [language, suite]:
        status = doctest.testmod(module,
                                optionflags=FLAGS,)[0] or status
    return status

if __name__ == '__main__':
    sys.exit( run_all_python_modules_here() or run_python_modules_outhere())
