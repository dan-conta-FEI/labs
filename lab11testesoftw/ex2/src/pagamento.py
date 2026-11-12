def confirmar(pedido, centavos, gateway, email, tentativas=3):
    tentativa = 0
    while True:
        tentativa += 1
        try:
            status = gateway.cobrar(pedido, centavos)
            break
        except ConnectionError:
            if tentativa >= tentativas:
                email.enviar(pedido, "falha na cobranca")
                raise
    if status == "aprovado":
        email.enviar(pedido, "pedido confirmado")
    return status
