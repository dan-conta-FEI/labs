import pytest
from conversor import ConversorFrete


class CotacaoStub:
    def __init__(self, taxa):
        self.taxa = taxa

    def dolar(self):
        return self.taxa


@pytest.mark.parametrize(
    "centavos, taxa, esperado",
    [
        (100, 5.0, 500),
        (0, 5.0, 0),
        (100, 5.25, 525),
        (1, 2.5, 2),
        (3, 2.5, 8),
        (1, 3.5, 4),
    ],
)
def test_conversao(centavos, taxa, esperado):
    conversor = ConversorFrete(CotacaoStub(taxa))
    assert conversor.em_centavos_de_real(centavos) == esperado


# PERGUNTA: por que este teste nao deve usar um servico real de cotacao?
# RESPOSTA: o servico real e lento, depende de rede e pode cair, e a taxa
# muda toda hora, entao o resultado nao e repetivel (teste instavel). Alem
# disso nao da pra forcar o TimeoutError quando eu quiser, e pode ter custo
# ou limite de chamadas. Teste de unidade tem que testar so a logica do
# conversor, de forma rapida e deterministica, entao uso stub e Mock.


# PERGUNTA: por que este teste nao deve usar um servico real de cotacao?
# RESPOSTA: o servico real e lento, depende de rede e pode cair, e a taxa
# muda toda hora, entao o resultado nao e repetivel (teste instavel).
# Alem disso nao da pra forcar o TimeoutError quando eu quiser, e pode ter
# custo ou limite de chamadas. Teste de unidade tem que testar so a logica
# do conversor, de forma rapida e deterministica, entao uso stub e Mock.
