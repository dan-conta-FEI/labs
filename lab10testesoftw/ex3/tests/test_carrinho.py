# EXERCICIO 3: REGRAS NOVAS NO CARRINHO
#
# A) TESTES ATUAIS QUE CONTRADIZEM AS REGRAS NOVAS
# "CUPOM EM 5000 DA 4500": O DEZ AGORA SO VALE A PARTIR DE 10000, ENTAO
# 5000 FICA SEM DESCONTO (5000)
# "1000 APOS O CUPOM DA 900": 1000 ESTA ABAIXO DO MINIMO, ENTAO NAO TEM
# DESCONTO (1000)
# OS OUTROS (VAZIO, 2500, QUANTIDADE=2, PRECO 0, CUPOM XYZ) CONTINUAM VALENDO
# O QUE FAZER ANTES DE MUDAR O CODIGO: ATUALIZAR ESSES DOIS TESTES PARA OS
# VALORES NOVOS E VER FALHAR (RED). ASSIM A REGRA NOVA MANDA NO TESTE E O
# CODIGO SO MUDA DEPOIS
#
# C) O QUE MOSTRA QUE O REFACTOR NAO MUDOU NADA
# A SUITE ESTAVA VERDE ANTES DE GUARDAR PORCENTAGEM E MINIMO JUNTOS EM
# CUPONS E CONTINUOU VERDE DEPOIS, SEM ALTERAR NENHUM TESTE
#
# D) VALORES DE QUANTIDADE TESTADOS E POR QUE
# 1: MENOR VALOR VALIDO (FRONTEIRA DE DENTRO)
# 0: PRIMEIRO VALOR INVALIDO (FRONTEIRA DE FORA)
# -1: NEGATIVO, OUTRO LADO DO INVALIDO
# 1.5: NUMERO NAO INTEIRO, PASSARIA NO TESTE "MENOR QUE 1" SE SO ISSO
# EXISTISSE
# "2": TIPO ERRADO, NAO PODE VIRAR TYPEERROR NA COMPARACAO
# 2: VALOR COMUM, JA COBERTO PELO TESTE DA TEORIA (2500 X 2 DA 5000)

import pytest
from carrinho import Carrinho


def test_carrinho_vazio_total_zero():
    carrinho = Carrinho()
    assert carrinho.total == 0


def test_um_item_de_2500_total_2500():
    carrinho = Carrinho()
    carrinho.adicionar(2500)
    assert carrinho.total == 2500


def test_quantidade_2_dobra_o_total():
    carrinho = Carrinho()
    carrinho.adicionar(2500, quantidade=2)
    assert carrinho.total == 5000


def test_preco_zero_e_rejeitado():
    carrinho = Carrinho()
    with pytest.raises(ValueError):
        carrinho.adicionar(0)


def test_cupom_dez_abaixo_do_minimo_fica_sem_desconto():
    carrinho = Carrinho()
    carrinho.adicionar(5000)
    carrinho.aplicar_cupom("DEZ")
    assert carrinho.total == 5000


def test_cupom_desconhecido_e_rejeitado():
    carrinho = Carrinho()
    with pytest.raises(ValueError):
        carrinho.aplicar_cupom("XYZ")


def test_item_abaixo_do_minimo_apos_o_cupom_fica_sem_desconto():
    carrinho = Carrinho()
    carrinho.aplicar_cupom("DEZ")
    carrinho.adicionar(1000)
    assert carrinho.total == 1000


def test_dez_no_minimo_exato_tem_desconto():
    carrinho = Carrinho()
    carrinho.adicionar(10000)
    carrinho.aplicar_cupom("DEZ")
    assert carrinho.total == 9000


def test_dez_um_abaixo_do_minimo_nao_tem_desconto():
    carrinho = Carrinho()
    carrinho.adicionar(9999)
    carrinho.aplicar_cupom("DEZ")
    assert carrinho.total == 9999


def test_desconto_passa_a_valer_quando_subtotal_chega_ao_minimo():
    carrinho = Carrinho()
    carrinho.aplicar_cupom("DEZ")
    carrinho.adicionar(6000)
    assert carrinho.total == 6000
    carrinho.adicionar(4000)
    assert carrinho.total == 9000


def test_vinte_em_30000_da_24000():
    carrinho = Carrinho()
    carrinho.adicionar(30000)
    carrinho.aplicar_cupom("VINTE")
    assert carrinho.total == 24000


def test_vinte_abaixo_de_30000_nao_tem_desconto():
    carrinho = Carrinho()
    carrinho.adicionar(29999)
    carrinho.aplicar_cupom("VINTE")
    assert carrinho.total == 29999
