class Fila:
    def __init__(self):
        self._contadores = {"normal": 0, "prioritaria": 0}

    def emitir(self, tipo):
        self._contadores[tipo] += 1
        prefixo = "N" if tipo == "normal" else "P"
        return f"{prefixo}{self._contadores[tipo]}"

    @property
    def aguardando(self):
        return 0
