# coding: utf-8
"""
    >>> CorrigindoBugDeHeranca.rodar()
    True
    >>> print saida.getvalue()
    História: Corrigindo bug de heranca
      Como um cara enpenhado em corrigir bugs
      Eu quero corrigir o bug de heranca no pyhistorian
      Para que uma nova versao seja lancada
    <BLANKLINE>
      Cenário 1: Ficticio
        Então deve estar pendente!   ... PENDENTE
    <BLANKLINE>
      Rodou 1 cenário com 0 falhas, 0 erros e 1 passo pendente
    <BLANKLINE>
"""

from cStringIO import StringIO
from pyhistorian import Cenario, Historia, Entao

saida = StringIO()

class CorrigindoBugDeHeranca(Historia):
    """Como um cara enpenhado em corrigir bugs
    Eu quero corrigir o bug de heranca no pyhistorian
    Para que uma nova versao seja lancada"""
    saida = saida
    colorido = False

class Ficticio(Cenario):
    Entao('deve estar pendente!')
    
