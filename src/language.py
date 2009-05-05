# coding: utf-8

_english = dict(story='Story',
                as_a='As a',
                i_want_to='I want to',
                so_that='So that',
                scenario='Scenario',
                given='Given',
                when='When',
                then='Then',
                fail='Fail',
                and_word='And',
                empty_story_title='Empty Story',
                empty_scenario_title='Empty Sceario',
                exception_thrown='Exception %s was thrown!',
                undefined_step='Undefined Step',
                )

_portuguese = dict(story='HistÛria',
                as_a='Como um',
                i_want_to='Eu quero',
                so_that='Para que',
                scenario='Cen·rio',
                given='Dado que',
                when='Quando',
                then='Ent„o',
                fail='Falha',
                and_word='E',
                empty_story_title='HistÛria Vazia',
                empty_scenario_title='Cen·rio Vazio',
                exception_thrown='A ExceÁ„o %s foi levantada!',
                undefined_step='Passo n„o definido',
                )

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
        Hist√≥ria
    '''
    def __init__(self, language):
        if language not in _LANGUAGES:
            raise StoryLanguageError('There is no language %s' % language)
        self._language = _LANGUAGES[language]

    def __getitem__(self, term):
        if term not in self._language:
            raise StoryLanguageError('There is no term %s' % term)
        return self._language[term]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
