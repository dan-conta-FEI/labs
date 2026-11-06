class Fila:
    def __init__(self):
        self._contadores = {"normal": 0, "prioritaria": 0}
        self._normais = []
        self._prioritarias = []

    def emitir(self, tipo):
        if tipo not in self._contadores:
            raise ValueError("tipo invalido")
        self._contadores[tipo] += 1
        prefixo = "N" if tipo == "normal" else "P"
        senha = f"{prefixo}{self._contadores[tipo]}"
        lista = self._normais if tipo == "normal" else self._prioritarias
        lista.append(senha)
        return senha

    def chamar(self):
        if self._prioritarias:
            return self._prioritarias.pop(0)
        return self._normais.pop(0)

    @property
    def aguardando(self):
        return len(self._normais) + len(self._prioritarias)
