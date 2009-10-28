# coding: utf-8
"""
    >>> FormattingExceptions.run()
    False
    >>> print english_output.getvalue()
    Story: Formatting exceptions
    As a user interested in rastreability
    I want to know where the errors come from
    So that I can go to the root of all evil
    <BLANKLINE>
    Scenario 1: Raising an exception
      Then raise an exception with "Hello Motto"   ... ERROR
    <BLANKLINE>
    Errors:
      File ".../specs/traceback_message.py", line ..., in raise_hello_motto
        raise Exception("Hello Motto")
    Exception: Hello Motto
    <BLANKLINE>
    <BLANKLINE>
    Ran 1 scenario with 0 failures, 1 error and 0 pending steps
    <BLANKLINE>

    >>> FormatandoExcecoes.run()
    False
    >>> print portuguese_output.getvalue()
    História: Formatando excecoes 
    Como um usuário interessado em rastreabilidade
    Eu quero saber de onde os erros vem
    Para que eu possa ir para a raiz de todo o mal
    <BLANKLINE>
    Cenário 1: Levantando uma excecao
      Então levante uma excecao com "Oi Motto"   ... ERRO
    <BLANKLINE>
    Erros:
      Arquivo ".../specs/traceback_message.py", linha ..., em levantar_oi_motto
        raise Exception("Oi Motto")
    Exception: Oi Motto
    <BLANKLINE>
    <BLANKLINE>
    Rodou 1 cenário com 0 falhas, 1 erro e 0 passos pendentes
    <BLANKLINE>
 
"""
from pyhistorian import *
from cStringIO import StringIO

english_output = StringIO()
portuguese_output = StringIO()


class FormattingExceptions(Story):
    """As a user interested in rastreability
    I want to know where the errors come from
    So that I can go to the root of all evil"""
    scenarios = ('RaisingAnException',)
    colored = False
    output = english_output

class RaisingAnException(Scenario):
    @Then('raise an exception with "Hello Motto"')
    def raise_hello_motto(self):
        raise Exception("Hello Motto")


class FormatandoExcecoes(Historia):
    """Como um usuário interessado em rastreabilidade
    Eu quero saber de onde os erros vem
    Para que eu possa ir para a raiz de todo o mal"""
    cenarios = ('LevantandoUmaExcecao',)
    colorido = False
    saida = portuguese_output

class LevantandoUmaExcecao(Cenario):
    @Entao('levante uma excecao com "Oi Motto"')
    def levantar_oi_motto(self):
        raise Exception("Oi Motto")

