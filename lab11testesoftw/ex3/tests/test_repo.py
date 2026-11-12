import pytest
from repo import RepoSqlite, FakeIngenuo, FakeFiel, EmailDuplicado


@pytest.fixture(
    params=[
        RepoSqlite,
        pytest.param(
            FakeIngenuo,
            marks=pytest.mark.xfail(reason="fake ingenuo viola o contrato"),
        ),
        FakeFiel,
    ]
)
def repo(request):
    return request.param()


def test_buscar_inexistente_devolve_none(repo):
    assert repo.buscar("a@x.com") is None


def test_salvar_e_buscar(repo):
    repo.salvar("a@x.com", "Ana")
    assert repo.buscar("a@x.com") == "Ana"


def test_busca_ignora_maiusculas(repo):
    repo.salvar("Ana@X.com", "Ana")
    assert repo.buscar("ana@x.com") == "Ana"
    assert repo.buscar("ANA@X.COM") == "Ana"


def test_salvar_duplicado_levanta(repo):
    repo.salvar("a@x.com", "Ana")
    with pytest.raises(EmailDuplicado):
        repo.salvar("a@x.com", "Outra")


def test_duplicado_ignora_maiusculas(repo):
    repo.salvar("a@x.com", "Ana")
    with pytest.raises(EmailDuplicado):
        repo.salvar("A@X.COM", "Outra")


def test_duplicado_nao_sobrescreve(repo):
    repo.salvar("a@x.com", "Ana")
    with pytest.raises(EmailDuplicado):
        repo.salvar("a@x.com", "Outra")
    assert repo.buscar("a@x.com") == "Ana"


# (d) INTERPRETACAO DAS FALHAS (rode com: pytest --runxfail)
# O FakeIngenuo falha em 4 testes, por 2 causas:
# 1. Nao ignora maiusculas: o dict usa a string exata como chave, entao
#    "ANA@X.COM" nao acha "ana@x.com" (falha na busca).
# 2. Nao detecta e-mail repetido: salvar so faz d[email] = nome, entao nao
#    levanta EmailDuplicado (3 falhas: igual, com caixa diferente e
#    "nao sobrescreve", ja que o nome antigo seria perdido).
# O FakeFiel normaliza o e-mail com lower() e checa se a chave ja existe
# antes de gravar, o mesmo comportamento do RepoSqlite (COLLATE NOCASE).
#
# PERGUNTA: o que aconteceria com os testes de unidade que usassem o fake
# ingenuo?
# RESPOSTA: ficariam verdes mesmo com o codigo dependente errado, porque
# o fake aceita duplicado e diferencia maiusculas, coisas que o repositorio
# real nao faz. O erro so apareceria na integracao ou em producao. A suite
# de contrato roda nos dois e mantem o fake igual ao real.
