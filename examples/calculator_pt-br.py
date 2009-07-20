# coding: utf-8
from should_dsl import *
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

    @Quando('eu entro com 1 + 1')
    def somar_um_e_um(self):
        self.resultado = self.calculadora.somar(1, 1)

    @Entao('eu tenho $valor como resultado', 2)
    def pegar_resultado(self, valor):
        self.resultado |should_be| valor


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
    calculadora_historia = Historia('Especificando minha nova calculadora',
                             como_um='matemático preguiçoso',
                             eu_quero='usar uma calculadora',
                             para_que='eu não gastei tempo pensando',
                             colorido=True)
    (calculadora_historia
                        .adicionar_cenario(SomaCenario('Soma de 1 e 1'))
                        .adicionar_cenario(SomaESubtracaoCenario('Subtração de uma soma'))
                        .adicionar_cenario(DivisaoCenario('Divisão de inteiros'))
                        .adicionar_cenario(MultiplyScenario('Multiplicação simples'))
                        .run())
