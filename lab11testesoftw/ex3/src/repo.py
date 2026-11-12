import sqlite3


class EmailDuplicado(Exception):
    pass


class RepoSqlite:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute(
            "CREATE TABLE usuarios "
            "(email TEXT PRIMARY KEY COLLATE NOCASE, nome TEXT)"
        )

    def salvar(self, email, nome):
        try:
            self.conn.execute(
                "INSERT INTO usuarios (email, nome) VALUES (?, ?)",
                (email, nome),
            )
        except sqlite3.IntegrityError:
            raise EmailDuplicado(email)

    def buscar(self, email):
        linha = self.conn.execute(
            "SELECT nome FROM usuarios WHERE email = ?", (email,)
        ).fetchone()
        return linha[0] if linha else None


class FakeIngenuo:
    def __init__(self):
        self.d = {}

    def salvar(self, email, nome):
        self.d[email] = nome

    def buscar(self, email):
        return self.d.get(email)


class FakeFiel:
    def __init__(self):
        self.d = {}

    def salvar(self, email, nome):
        chave = email.lower()
        if chave in self.d:
            raise EmailDuplicado(email)
        self.d[chave] = nome

    def buscar(self, email):
        return self.d.get(email.lower())
