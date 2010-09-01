# coding: utf-8
"""
    this module contains all stuff related to
    internationalization and messages
"""
import traceback
import re


__all__ = ['TEMPLATE_PATTERN',
           'convert_from_cammel_case_to_spaces',
           'StoryLanguage',
           'format_traceback',
           'pluralize',]


TEMPLATE_PATTERN = r'\$[a-zA-Z]\w*'


def convert_from_cammel_case_to_spaces(text):
    """
        >>> convert_from_cammel_case_to_spaces('HelloWorld')
        'Hello world'
        >>> convert_from_cammel_case_to_spaces('helloMotto')
        'hello motto'
    """
    spaced_text = text[0]
    for char in text[1:]:
        if char == char.capitalize():
            spaced_text += ' ' + char.lower()
        else:
            spaced_text += char
    return spaced_text


def format_traceback(exc, value, tb, language):
    """format the traceback to show the user a nice and
    internationalized message"""
    def remove_initial_blanks(msg):
        return re.sub('^\s*', '', msg)

    def translate_file_word(msg):
        return re.sub(r'^File', language['file'].capitalize(), msg)

    def translate_line_word(msg):
        return re.sub(r', line ', ', %s ' %language['line'].lower(), msg)

    def translate_in_word(msg):
        return re.sub(r', in ', ', %s ' % language['in'].lower(), msg)

    info_msg = ''
    # skip the first item because it is the pyhistorian's call
    for info in traceback.format_tb(tb)[1:]:
        info_lines = map(remove_initial_blanks, info.split('\n')[:-1])

        if len(info_lines) == 1:
            file_info, call_info = info_lines[0], ''
        else:
            file_info, call_info = info_lines

        file_info = translate_in_word(
                      translate_line_word(
                        translate_file_word(file_info)))
        info_msg += '    %s\n      %s\n'% (file_info, call_info)
    last_line = '    ' + traceback.format_exception_only(exc, value)[-1]
    return info_msg + last_line


def pluralize(word, size):
    if size >= 2 or size == 0:
        return word+'s'
    return word


_english = {
           'story': 'Story',
           'as_a': 'As a',
           'i_want_to': 'I want to',
           'so_that': 'So that',
           'in_order_to': 'In order to',
           'scenario': 'Scenario',
           'given': 'Given',
           'when': 'When',
           'then': 'Then',
           'fail': 'Fail',
           'failure': 'Failure',
           'error': 'Error',
           'and': 'And',
           'empty_story_title': 'Empty Story',
           'empty_scenario_title': 'Empty Sceario',
           'exception_thrown': 'Exception %s was thrown!',
           'undefined_step': 'Undefined Step',
           'ran': 'Ran',
           'with': 'with',
           'pending': 'pending',
           'step': 'step',
           'file': 'File',
           'line': 'line',
           'in': 'in',
           'ok': 'ok',
           }

_portuguese = {
              'story': 'História',
              'as_a': 'Como um',
              'i_want_to': 'Eu quero',
              'so_that': 'Para que',
              'in_order_to': 'Para que',
              'scenario': 'Cenário',
              'given': 'Dado que',
              'when': 'Quando',
              'then': 'Então',
              'fail': 'Falha',
              'failure': 'Falha',
              'error': 'Erro',
              'and': 'E',
              'empty_story_title': 'História Vazia',
              'empty_scenario_title': 'Cenário Vazio',
              'exception_thrown': 'A Exceção %s foi levantada!',
              'undefined_step': 'Passo não definido',
              'ran': 'Rodou',
              'with': 'com',
              'pending': 'pendente',
              'step': 'passo',
              'file': 'Arquivo',
              'line': 'linha',
              'in': 'em',
              'ok': 'ok',
              }

_LANGUAGES = {'en-us': _english,
              'pt-br' : _portuguese}

class StoryLanguageError(Exception):
    '''raised when the user wants a non-existent language or
    some non-existent term
    '''


class StoryLanguage(object):
    '''
        >>> en_us = StoryLanguage('en-us')
        >>> print en_us['story']
        Story
        >>> pt_br = StoryLanguage('pt-br')
        >>> print pt_br['story']
        História
    '''
    def __init__(self, language):
        if language not in _LANGUAGES:
            raise StoryLanguageError('There is no language %s' % language)
        self._language = _LANGUAGES[language]

    def __getitem__(self, term):
        if term not in self._language:
            raise StoryLanguageError('There is no term "%s"' % term)
        return self._language[term]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
