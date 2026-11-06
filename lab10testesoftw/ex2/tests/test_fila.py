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
#
# C) QUAL TESTE OBRIGOU A CONTAR E QUAL OBRIGOU A ZERAR
# CONTAR AS PRIORITARIAS SEGUIDAS: TESTE 11 (DEPOIS DE 2 PRIORITARIAS
# SEGUIDAS, COM NORMAL ESPERANDO, CHAMA NORMAL). SEM O CONTADOR, O CHAMAR
# DEVOLVIA P1, P2, P3 E O RED FALHAVA
# ZERAR A CONTAGEM: TESTE 12 (P1, P2, N1, P3, P4, N2). SEM ZERAR, DEPOIS DE
# CHAMAR N1 A CONTAGEM CONTINUAVA EM 2 E O CHAMAR DEVOLVIA N2 NO LUGAR DE P3
#
# D) TESTE QUE MOSTRA QUE O LIMITE DE 2 NAO VALE SEM NORMAL ESPERANDO
# TESTE 13: COM P1, P2 E P3 EMITIDAS E NENHUMA NORMAL, AS CHAMADAS SAEM
# P1, P2, P3 SEGUIDAS. PASSOU DE PRIMEIRA PORQUE O CHAMAR JA TINHA A
# CONDICAO "AND SELF._NORMAIS", QUE SO TROCA PARA NORMAL SE HOUVER ALGUMA
# ESPERANDO. FICA NA SUITE PARA PROTEGER ESSA CONDICAO
#
# E) COBERTURA E MUTMUT
# COBERTURA DE RAMOS: 100% (27 STATEMENTS, 6 BRANCHES, NENHUM PERDIDO)
# MUTMUT ANTES DO TESTE NOVO: 48 DE 52 MORTOS (92,3%)
# VIVOS EMITIR 2, 3 E 4: SO MUDAM O TEXTO DA MENSAGEM DO VALUEERROR (NONE,
# "XXTIPO INVALIDOXX", "TIPO INVALIDO" EM MAIUSCULAS). A ESPECIFICACAO SO
# PEDE VALUEERROR E NAO DEFINE A MENSAGEM, ENTAO NAO INDICAM COMPORTAMENTO
# SEM TESTE
# VIVO CHAMAR 14: O SELF._SEGUIDAS = 0 VIROU SELF._SEGUIDAS = 1 NO CASO DE
# CHAMAR NORMAL POR FALTA DE PRIORITARIA. LACUNA REAL: NENHUM TESTE
# CONFERIA QUE ESSA CHAMADA TAMBEM ZERA A CONTAGEM
# TESTE NOVO: N1 CHAMADA POR FALTA DE PRIORITARIA, DEPOIS P1, P2, N2, N3
# MUTMUT DEPOIS DO TESTE NOVO: 49 DE 52 MORTOS (94,2%), SOBRAM SO OS 3 DA
# MENSAGEM DO ERRO

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


def test_aguardando_sobe_na_emissao_e_desce_na_chamada():
    fila = Fila()
    fila.emitir("normal")
    fila.emitir("prioritaria")
    assert fila.aguardando == 2
    fila.chamar()
    assert fila.aguardando == 1


def test_chamar_com_fila_vazia_lanca_index_error():
    fila = Fila()
    with pytest.raises(IndexError):
        fila.chamar()


def test_so_normais_seguem_ordem_de_chegada():
    fila = Fila()
    fila.emitir("normal")
    fila.emitir("normal")
    assert fila.chamar() == "N1"
    assert fila.chamar() == "N2"


def test_prioritaria_passa_na_frente_de_normal():
    fila = Fila()
    fila.emitir("normal")
    fila.emitir("prioritaria")
    assert fila.chamar() == "P1"


def test_so_prioritarias_seguem_ordem_de_chegada():
    fila = Fila()
    fila.emitir("prioritaria")
    fila.emitir("prioritaria")
    assert fila.chamar() == "P1"
    assert fila.chamar() == "P2"


def test_depois_de_duas_prioritarias_chama_normal():
    fila = Fila()
    for _ in range(3):
        fila.emitir("prioritaria")
    fila.emitir("normal")
    chamadas = [fila.chamar() for _ in range(4)]
    assert chamadas == ["P1", "P2", "N1", "P3"]


def test_chamar_normal_zera_a_contagem_de_prioritarias():
    fila = Fila()
    for _ in range(4):
        fila.emitir("prioritaria")
    fila.emitir("normal")
    fila.emitir("normal")
    chamadas = [fila.chamar() for _ in range(6)]
    assert chamadas == ["P1", "P2", "N1", "P3", "P4", "N2"]


def test_sem_normal_esperando_limite_de_duas_nao_vale():
    fila = Fila()
    for _ in range(3):
        fila.emitir("prioritaria")
    chamadas = [fila.chamar() for _ in range(3)]
    assert chamadas == ["P1", "P2", "P3"]


def test_chamar_normal_por_falta_de_prioritaria_zera_a_contagem():
    fila = Fila()
    fila.emitir("normal")
    assert fila.chamar() == "N1"
    fila.emitir("prioritaria")
    fila.emitir("prioritaria")
    fila.emitir("normal")
    fila.emitir("normal")
    chamadas = [fila.chamar() for _ in range(4)]
    assert chamadas == ["P1", "P2", "N2", "N3"]
