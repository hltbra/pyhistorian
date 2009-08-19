#!/usr/bin/env python
# coding: utf-8
import doctest
import os
import sys
from pyhistorian import language
from pyhistorian import suite
import pyhistorian

FLAGS = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
THIS_DIRNAME = os.path.dirname(os.path.abspath(__file__))
PYHISTORIAN_DIRNAME = os.path.dirname(os.path.abspath(pyhistorian.__file__))

def run_all_python_modules(files, files_to_be_ignored=[]):
    status = 0
    for python_file in files:
        if python_file not in files_to_be_ignored:
            python_module = __import__(python_file[:-3])
            if python_module.__doc__:
                print 'Running doctest in %s' % os.path.abspath(python_file)
                status = doctest.testmod(python_module, optionflags=FLAGS)[0] or status
    return status

def run_python_modules_outhere():
    all_pyhistorian_python_files = ['pyhistorian.'+filename for filename in os.listdir(PYHISTORIAN_DIRNAME)
                                          if filename.endswith('.py')]

    run_all_python_modules(all_pyhistorian_python_files, ['__init__.py'])

def run_all_python_modules_here():
    all_python_files_here = [filename for filename in os.listdir(THIS_DIRNAME)
                                          if filename.endswith('.py')]
    run_all_python_modules(all_python_files_here, ['__init__.py',
                                                   'run_specs.py'])

if __name__ == '__main__':
    sys.exit(run_all_python_modules_here() or run_python_modules_outhere())
