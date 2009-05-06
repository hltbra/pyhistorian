# coding: utf-8
from should_dsl import DSLObject as _
from pyhistorian import *

class Calculadora(object):
    def somar(self, n1, n2):
        return n1+n2

    def subtrair(self, n1, n2):
        return n1-n2

    def dividir(self, n1, n2):
        return n1/n2

    def multiplicar(self, n1, n2):
        return n1*n2

class SomaCenario(Scenario):
    @DadoQue('eu tenho uma calculadora')
    def criar_calculadora(self):
        self.calculadora = Calculadora()

    @Quando('eu entro com 1 \+ 1')
    def somar_um_e_um(self):
        self.resultado = self.calculadora.somar(1, 1)

    @Entao('eu tenho $valor como resultado', '2')
    def pegar_resultado(self, valor):
        _(self.resultado).should_be.equal_to(int(valor))


class SomaESubtracaoCenario(Scenario):
    DadoQue('eu tenho uma calculadora')

    Quando('eu entro com 1 + 1')

    @Quando('eu subtraio 3 do resultado atual')
    def subtrair_tres_do_resultado_atual(self):
        self.resultado = self.calculadora.subtrair(self.resultado, 3)

    Entao('eu tenho -1 como resultado')


class DivisaoCenario(Scenario):
    DadoQue('eu tenho uma calculadora')

    @Quando('eu entro com 5 / 2')
    def cinco_dividido_por_2(self):
        self.resultado = self.calculadora.dividir(5, 2)

    Entao('eu tenho 2 como resultado')


class MultiplyScenario(Scenario):
    DadoQue('eu tenho uma calculadora')

    @Quando('eu entro com 2 * 3')
    def multiplicar_dois_por_tres(self):
        self.resultado = self.calculadora.multiplicar(2, 3)

    Entao('eu tenho 6 como resultado')


if __name__ == '__main__':
    calculadora_historia = Story(title='Especificando minha nova calculadora',
                             as_a='matemático preguiçoso',
                             i_want_to='usar uma calculadora',
                             so_that='eu não gastei tempo pensando',
                             language='pt-br')
    (calculadora_historia
                        .add_scenario(SomaCenario('Soma de 1 e 1'))
                        .add_scenario(SomaESubtracaoCenario('Subtração de uma soma'))
                        .add_scenario(DivisaoCenario('Divisão de inteiros'))
                        .add_scenario(MultiplyScenario('Multiplicação simples'))
                        .run())
