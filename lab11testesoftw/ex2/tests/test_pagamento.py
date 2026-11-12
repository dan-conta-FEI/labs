import pytest
from unittest.mock import Mock, call
from pagamento import confirmar


def test_aprovado_de_primeira():
    gateway = Mock()
    gateway.cobrar.return_value = "aprovado"
    email = Mock()
    r = confirmar("p1", 5000, gateway, email)
    assert r == "aprovado"
    gateway.cobrar.assert_called_once_with("p1", 5000)
    email.enviar.assert_called_once_with("p1", "pedido confirmado")


def test_negado_nao_envia_email():
    gateway = Mock()
    gateway.cobrar.return_value = "negado"
    email = Mock()
    r = confirmar("p1", 5000, gateway, email)
    assert r == "negado"
    gateway.cobrar.assert_called_once_with("p1", 5000)
    email.enviar.assert_not_called()


def test_erro_e_depois_aprovado():
    gateway = Mock()
    gateway.cobrar.side_effect = [ConnectionError(), "aprovado"]
    email = Mock()
    r = confirmar("p1", 5000, gateway, email)
    assert r == "aprovado"
    assert gateway.cobrar.call_count == 2
    gateway.cobrar.assert_has_calls([call("p1", 5000), call("p1", 5000)])
    email.enviar.assert_called_once_with("p1", "pedido confirmado")


def test_falha_em_todas_as_tentativas():
    gateway = Mock()
    gateway.cobrar.side_effect = ConnectionError
    email = Mock()
    with pytest.raises(ConnectionError):
        confirmar("p1", 5000, gateway, email)
    assert gateway.cobrar.call_count == 3
    email.enviar.assert_called_once_with("p1", "falha na cobranca")


def test_tentativas_personalizadas():
    gateway = Mock()
    gateway.cobrar.side_effect = ConnectionError
    email = Mock()
    with pytest.raises(ConnectionError):
        confirmar("p1", 5000, gateway, email, tentativas=5)
    assert gateway.cobrar.call_count == 5


def test_uma_tentativa_so():
    gateway = Mock()
    gateway.cobrar.side_effect = ConnectionError
    email = Mock()
    with pytest.raises(ConnectionError):
        confirmar("p1", 5000, gateway, email, tentativas=1)
    assert gateway.cobrar.call_count == 1
    email.enviar.assert_called_once_with("p1", "falha na cobranca")


# PERGUNTA: por que, aqui, conferir as chamadas nao e excesso?
# RESPOSTA: porque a chamada e o proprio requisito. O que importa nao
# aparece no retorno: quantas vezes cobrou (cobrar demais cobra o cliente em
# duplicidade), com quais argumentos (pedido e valor certos) e quais e-mails
# saem (falha so depois da ultima tentativa, confirmacao so se aprovado,
# nada se negado). O retorno "aprovado" sozinho nao mostra nada disso.


# PERGUNTA: por que, aqui, conferir as chamadas nao e excesso?
# RESPOSTA: porque a chamada e o proprio requisito. O que importa nao
# aparece no retorno: quantas vezes cobrou (cobrar demais cobra o cliente
# em duplicidade), com quais argumentos (pedido e valor certos) e quais
# e-mails saem (falha so depois da ultima tentativa, confirmacao so se
# aprovado, nada se negado). O retorno "aprovado" sozinho nao mostra isso.
