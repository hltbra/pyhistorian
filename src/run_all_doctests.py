#!/usr/bin/env python
# coding: utf-8

import doctest
import os
import language

if __name__ == '__main__':
    doctests_path = os.path.join(os.path.dirname(__file__), 'doctests')
    for doctest_file in os.listdir(doctests_path):
        if not doctest_file.endswith('.txt'):
            continue
        doctest.testfile(os.path.join(doctests_path, doctest_file),
                         optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)
    doctest.testmod(language,
                    optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)
