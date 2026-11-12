import frete
from estoque import Estoque
from pedido import fechar


def test_pedido_fechado_com_partes_reais():
    estoque = Estoque({"livro": 10})
    r = fechar("livro", 2, 4000, 1, "SP", estoque, frete.calcular)
    assert r == {"status": "fechado", "total": 9700}
    assert estoque.itens["livro"] == 8


def test_outra_uf_frete_mais_caro():
    estoque = Estoque({"livro": 10})
    r = fechar("livro", 2, 4000, 1, "RJ", estoque, frete.calcular)
    assert r == {"status": "fechado", "total": 10700}


def test_sem_estoque_com_partes_reais():
    estoque = Estoque({"livro": 1})
    r = fechar("livro", 2, 4000, 1, "SP", estoque, frete.calcular)
    assert r == {"status": "sem estoque"}
    assert estoque.itens["livro"] == 1


def test_sistema_tres_pedidos_ate_esgotar():
    estoque = Estoque({"livro": 4})
    pedidos = [
        fechar("livro", 2, 4000, 1, "SP", estoque, frete.calcular)
        for _ in range(3)
    ]
    assert pedidos == [
        {"status": "fechado", "total": 9700},
        {"status": "fechado", "total": 9700},
        {"status": "sem estoque"},
    ]
    assert estoque.itens["livro"] == 0


# (b) DEFEITOS DE INTERFACE encontrados:
# 1. Estoque.reservar devolve None quando da certo e levanta SemEstoque
#    quando falta, mas o pedido esperava True/False. Como "not None" e
#    True, todo pedido virava "sem estoque". Correcao em pedido.py:
#    try/except SemEstoque.
# 2. frete.calcular recebe (peso_kg, uf) e o pedido chamava
#    frete(uf, peso_kg), com os argumentos trocados. Correcao:
#    frete(peso_kg, uf).
# 3. Unidades: o contrato e em centavos, mas os stubs usavam reais
#    (40.0 e 15.0). Corrigido: 4000 e 1700, total 9700.
# O Mock aceita qualquer chamada e qualquer retorno, por isso o teste
# de unidade passava mesmo com os tres defeitos.
#
# (c) Os stubs de test_pedido.py agora seguem o contrato real: reservar
# devolve None ou levanta SemEstoque, e o frete e conferido com os
# argumentos na ordem certa (1, "SP") e o valor em centavos.
#
# (e) TOP-DOWN: comeca pelo modulo de cima. Real: pedido.fechar.
# Stub: Estoque (reservar) e frete.calcular. Depois troca os stubs
# pelos reais, um de cada vez, ate ter tudo integrado.
