# coding: utf-8
'''
>>> CalculadoraBrasileira.rodar()
True
>>> print OUTPUT.getvalue()
História: Calculadora brasileira
Como um matemático preguiçoso
Eu quero usar uma calculadora
Para que eu descanse minha mente
<BLANKLINE>
Cenário 1: Somando 1 e 1
  Dado que eu tenho uma calculadora   ... OK
  Quando eu entro com 1 + 1   ... OK
  Então eu tenho 2 como resultado   ... OK
<BLANKLINE>
Cenário 2: Fazendo subtracao duas vezes
  Dado que eu tenho uma calculadora   ... OK
  Quando eu entro com 22 - 11   ... OK
  E eu subtraio 2 desse resultado   ... OK
  Então eu tenho 9 como resultado   ... OK
<BLANKLINE>
Rodou 2 cenários com 0 falhas, 0 erros e 0 passos pendentes
<BLANKLINE>
>>>
'''

from pyhistorian import *
from should_dsl import *
from cStringIO import StringIO

OUTPUT = StringIO()

class Calculadora(object):
   def somar(self, n1, n2):
       return n1+n2

   def subtrair(self, n1, n2):
       return n1-n2

class Somando1E1(Cenario):
    @DadoQue('eu tenho uma calculadora')
    def cria_calculadora(self):
        self.calculadora = Calculadora()

    @Quando('eu entro com 1 + 1')
    def entrar_com_um_mais_um(self):
        self.resultado = self.calculadora.somar(1, 1)

    @Entao('eu tenho $valor como resultado', '2')
    def pegar_resultado(self, valor):
        self.resultado |should_be.equal_to| int(valor)

class FazendoSubtracaoDuasVezes(Cenario):
    DadoQue('eu tenho uma calculadora')

    @Quando('eu entro com 22 - 11')
    def entrar_com_dois_menos_um(self):
        self.resultado = self.calculadora.subtrair(22, 11)

    @Quando('eu subtraio 2 desse resultado')
    def subtrai_dois(self):
        self.resultado = self.calculadora.subtrair(self.resultado, 2)

    Entao('eu tenho 9 como resultado')


class CalculadoraBrasileira(Historia):
    """Como um matemático preguiçoso
       Eu quero usar uma calculadora
       Para que eu descanse minha mente"""
    saida = OUTPUT
    colorido = False
    cenarios = (Somando1E1, FazendoSubtracaoDuasVezes)
