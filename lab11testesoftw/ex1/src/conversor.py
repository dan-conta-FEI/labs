class CotacaoIndisponivel(Exception):
    pass


class ConversorFrete:
    def __init__(self, cotacao):
        self.cotacao = cotacao

    def em_centavos_de_real(self, centavos_de_dolar):
        try:
            taxa = self.cotacao.dolar()
        except TimeoutError as e:
            raise CotacaoIndisponivel() from e
        if taxa <= 0:
            raise ValueError("taxa invalida")
        return round(centavos_de_dolar * taxa)
