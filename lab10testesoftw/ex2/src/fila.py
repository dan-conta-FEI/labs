class Fila:
    def __init__(self):
        self._contadores = {"normal": 0, "prioritaria": 0}
        self._espera = []

    def emitir(self, tipo):
        if tipo not in self._contadores:
            raise ValueError("tipo invalido")
        self._contadores[tipo] += 1
        prefixo = "N" if tipo == "normal" else "P"
        senha = f"{prefixo}{self._contadores[tipo]}"
        self._espera.append(senha)
        return senha

    def chamar(self):
        return self._espera.pop(0)

    @property
    def aguardando(self):
        return len(self._espera)
