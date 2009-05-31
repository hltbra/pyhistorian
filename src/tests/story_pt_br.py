# coding: utf-8
'''
>>> calculadora_historia.run()
>>> print OUTPUT.getvalue()
História: Calculadora em pt-br
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
  Quando eu entro com 2 - 1   ... OK
  E eu subtraio 2 desse resultado   ... OK
  Então eu tenho -1 como resultado   ... OK
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

class SomaCenario(Scenario):
    @DadoQue('eu tenho uma calculadora')
    def cria_calculadora(self):
        self.calculadora = Calculadora()

    @Quando('eu entro com 1 + 1')
    def entrar_com_um_mais_um(self):
        self.resultado = self.calculadora.somar(1, 1)

    @Entao('eu tenho $valor como resultado', 2)
    def pegar_resultado(self, valor):
        self.resultado |should_be.equal_to| valor

class SubtracaoCenario(Scenario):
    DadoQue('eu tenho uma calculadora')

    @Quando('eu entro com 2 - 1')
    def entrar_com_dois_menos_um(self):
        self.resultado = self.calculadora.subtrair(2, 1)

    @Quando('eu subtraio 2 desse resultado')
    def subtrai_dois(self):
        self.resultado = self.calculadora.subtrair(self.resultado, 2)

    Entao('eu tenho -1 como resultado')

soma_cenario = SomaCenario('Somando 1 e 1')
subtracao_cenario = SubtracaoCenario('Fazendo subtracao duas vezes')

calculadora_historia = Story(title='Calculadora em pt-br',
                             as_a='matemático preguiçoso',
                             i_want_to='usar uma calculadora',
                             so_that='eu descanse minha mente',
                             language='pt-br',
                             output=OUTPUT)
(calculadora_historia.add_scenario(soma_cenario)
                     .add_scenario(subtracao_cenario))
