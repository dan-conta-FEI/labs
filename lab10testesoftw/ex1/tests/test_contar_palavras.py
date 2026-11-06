# EXERCICIO 1: CONTADOR DE PALAVRAS
#
# C) GIT LOG --ONELINE
# (COLE AQUI A SAIDA COMPLETA DE: git --no-pager log --oneline)
# NENHUM GREEN VEIO SEM UM RED ANTES.
# OS COMMITS "TESTE:" NAO SAO GREEN, PORQUE O TESTE JA PASSOU DE PRIMEIRA.
#
# D) TESTES QUE PASSARAM NA PRIMEIRA EXECUCAO
# "BOM DIA": O SPLIT() JA SEPARAVA POR ESPACO
# "DIA A DIA": O CONTAGEM.GET(PALAVRA, 0) + 1 JA CONTAVA REPETICAO
# "BOM\NDIA": O SPLIT() SEM ARGUMENTO SEPARA POR QUALQUER ESPACO EM BRANCO
# "BOM   DIA": O SPLIT() JUNTA ESPACOS SEGUIDOS NUM SEPARADOR SO
# "GUARDA-CHUVA": HIFEN NAO E SEPARADOR PRO SPLIT()
# ",DIA, ;DIA;": O STRIP() JA TIRAVA VARIOS SINAIS NAS DUAS BORDAS
# ":DIA: ?DIA?": OS SEIS SINAIS JA ESTAVAM NA LISTA DO STRIP()
# TODOS FICAM NA SUITE: NAO GUIARAM CODIGO NOVO, MAS DOCUMENTAM O CONTRATO
# E PROTEGEM CONTRA REGRESSAO.
#
# E) COBERTURA DE RAMOS E ESCORE DE MUTACAO DA SUITE FINAL
# COBERTURA DE RAMOS: 100% (7 STATEMENTS, 4 BRANCHES, NENHUM PERDIDO)
# MUTMUT ANTES DO TESTE NOVO: 12 DE 13 MORTOS (92,3%)
# SOBREVIVENTE: STRIP(".,;:!?") VIROU STRIP("XX.,;:!?XX")
# MOTIVO: NENHUM TESTE TINHA PALAVRA COM X NA BORDA, ENTAO NINGUEM
# NOTOU QUE O STRIP PASSOU A TIRAR LETRA TAMBEM
# TESTE NOVO: "XAXA, XOX!" DA {"XAXA": 1, "XOX": 1}
# MUTMUT DEPOIS DO TESTE NOVO: 13 DE 13 MORTOS (100%)
# COBERTURA 100% NAO GARANTE QUE OS TESTES PEGAM TUDO: A LINHA FOI
# EXECUTADA, MAS NENHUM TESTE CONFERIA O QUE ELA FAZ COM LETRAS

from contador import contar_palavras


def test_texto_vazio_devolve_dicionario_vazio():
    assert contar_palavras("") == {}


def test_uma_palavra_conta_uma_ocorrencia():
    assert contar_palavras("teste") == {"teste": 1}


def test_duas_palavras_viram_dois_itens():
    assert contar_palavras("bom dia") == {"bom": 1, "dia": 1}


def test_palavra_repetida_soma_ocorrencias():
    assert contar_palavras("dia a dia") == {"dia": 2, "a": 1}


def test_maiusculas_contam_como_minusculas():
    assert contar_palavras("Dia dia DIA") == {"dia": 3}


def test_quebra_de_linha_separa_palavras():
    assert contar_palavras("bom\ndia") == {"bom": 1, "dia": 1}


def test_espacos_multiplos_separam_duas_palavras():
    assert contar_palavras("bom   dia") == {"bom": 1, "dia": 1}


def test_hifen_interno_faz_parte_da_palavra():
    assert contar_palavras("guarda-chuva") == {"guarda-chuva": 1}


def test_sinais_nas_bordas_sao_ignorados():
    assert contar_palavras("fim. Fim!") == {"fim": 2}


def test_varios_sinais_nas_bordas_sao_ignorados():
    assert contar_palavras(",dia, ;dia;") == {"dia": 2}


def test_outros_sinais_nas_bordas_sao_ignorados():
    assert contar_palavras(":dia: ?dia?") == {"dia": 2}


def test_so_pontuacao_devolve_dicionario_vazio():
    assert contar_palavras("... !") == {}

def test_letras_nas_bordas_nao_sao_removidas():
    assert contar_palavras("xaxa, xox!") == {"xaxa": 1, "xox": 1}
