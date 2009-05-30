#!/usr/bin/env python
# coding: utf-8

import doctest
import os
import language
import suite
import pyhistorian
import should_dsl
from cStringIO import StringIO

pyhistorian_globs = {'Scenario': pyhistorian.Scenario,
                     'Story': pyhistorian.Story,
                     'Step': pyhistorian.Step,
                     'Given': pyhistorian.Given,
                     'When': pyhistorian.When, 
                     'Then': pyhistorian.Then,
                     'DadoQue': pyhistorian.DadoQue,
                     'Quando': pyhistorian.Quando,
                     'Entao': pyhistorian.Entao,}

should_dsl_globs = { 'should_be': should_dsl.should_be, 
                     'should_not_be': should_dsl.should_not_be,
                     'should_have': should_dsl.should_have,
                     'should_not_have': should_dsl.should_not_have, }

all_globs = pyhistorian_globs
all_globs.update(should_dsl_globs)
all_globs.update({'StringIO': StringIO,})

FLAGS = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS

if __name__ == '__main__':
    doctests_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
    'doctests'))
    for doctest_file in os.listdir(doctests_path):
       if not doctest_file.endswith('.txt'):
           continue
       doctest.testfile(os.path.join(doctests_path, doctest_file),
                        optionflags=FLAGS,
                        module_relative=False,
                        globs=all_globs)

    for module in [language, suite]:
        doctest.testmod(module,
                    optionflags=FLAGS,)
