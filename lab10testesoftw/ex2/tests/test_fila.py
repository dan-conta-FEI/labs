# EXERCICIO 2: FILA DE ATENDIMENTO
#
# A) LISTA DE TESTES (DO MAIS SIMPLES AO MAIS EXIGENTE)
# 1. FILA NOVA: AGUARDANDO E 0
# 2. EMITIR NORMAL DEVOLVE N1
# 3. DUAS NORMAIS SEGUIDAS: N1, N2
# 4. EMITIR PRIORITARIA DEVOLVE P1 (NUMERACAO INDEPENDENTE POR TIPO)
# 5. TIPO INVALIDO LANCA VALUEERROR
# 6. AGUARDANDO SOBE A CADA EMISSAO E DESCE A CADA CHAMADA
# 7. CHAMAR COM FILA VAZIA LANCA INDEXERROR
# 8. SO NORMAIS: CHAMAR SEGUE A ORDEM DE CHEGADA
# 9. PRIORITARIA PASSA NA FRENTE DE NORMAL QUE CHEGOU ANTES
# 10. SO PRIORITARIAS: CHAMAR SEGUE A ORDEM DE CHEGADA
# 11. DEPOIS DE 2 PRIORITARIAS SEGUIDAS, COM NORMAL ESPERANDO, CHAMA NORMAL
# 12. CHAMAR UMA NORMAL ZERA A CONTAGEM (P1, P2, N1, DEPOIS P3, P4, N2)
# 13. SEM NORMAL ESPERANDO, O LIMITE DE 2 NAO VALE (P1, P2, P3 SEGUIDAS)

import pytest
from fila import Fila


def test_fila_nova_nao_tem_ninguem_aguardando():
    fila = Fila()
    assert fila.aguardando == 0


def test_emitir_normal_devolve_n1():
    fila = Fila()
    assert fila.emitir("normal") == "N1"


def test_duas_normais_seguidas_numeram_n1_n2():
    fila = Fila()
    assert fila.emitir("normal") == "N1"
    assert fila.emitir("normal") == "N2"


def test_prioritaria_tem_numeracao_propria():
    fila = Fila()
    fila.emitir("normal")
    assert fila.emitir("prioritaria") == "P1"


def test_tipo_invalido_lanca_value_error():
    fila = Fila()
    with pytest.raises(ValueError):
        fila.emitir("vip")
