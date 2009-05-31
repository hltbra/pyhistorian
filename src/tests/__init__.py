import doctest
# tests follow
import bug_regex
import colors
import scenario
import step
import story
import unittest_integration
import stringio_feature
import story_pt_br

FLAGS=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
def run_tests():
    for test in [bug_regex,
                 colors,
                 scenario,
                 step,
                 story,
                 unittest_integration,
                 stringio_feature,
                 story_pt_br,]:
        doctest.testmod(test, optionflags=FLAGS)

if __name__ == '__main__':
    run_tests()
