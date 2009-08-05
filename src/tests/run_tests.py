#!/usr/bin/env python
# coding: utf-8
import doctest
import os
from pyhistorian import language
from pyhistorian import suite

FLAGS = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
THIS_DIRNAME = os.path.dirname(os.path.abspath(__file__))

def run_all_python_modules_here():
    all_python_files_here = [filename for filename in os.listdir(THIS_DIRNAME)
                                          if filename.endswith('.py')]

    for python_file in all_python_files_here:
        python_module = __import__(python_file[:-3])
        doctest.testmod(python_module, optionflags=FLAGS)

def run_python_modules_outhere():
    for module in [language, suite]:
        doctest.testmod(module,
                    optionflags=FLAGS,)

if __name__ == '__main__':
    run_all_python_modules_here()
    run_python_modules_outhere()
