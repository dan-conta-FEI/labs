class Fila:
    def __init__(self):
        self._normais = 0

    def emitir(self, tipo):
        self._normais += 1
        return f"N{self._normais}"

    @property
    def aguardando(self):
        return 0
