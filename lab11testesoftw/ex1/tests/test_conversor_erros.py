import pytest
from unittest.mock import Mock
from conversor import ConversorFrete, CotacaoIndisponivel


def test_timeout_vira_cotacao_indisponivel():
    cotacao = Mock()
    cotacao.dolar.side_effect = TimeoutError
    conversor = ConversorFrete(cotacao)
    with pytest.raises(CotacaoIndisponivel):
        conversor.em_centavos_de_real(100)


@pytest.mark.parametrize("taxa", [0, -1, -0.5])
def test_taxa_invalida_levanta_value_error(taxa):
    cotacao = Mock()
    cotacao.dolar.return_value = taxa
    conversor = ConversorFrete(cotacao)
    with pytest.raises(ValueError):
        conversor.em_centavos_de_real(100)
