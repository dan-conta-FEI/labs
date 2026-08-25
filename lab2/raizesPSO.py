import random

def calcular_fitness(posicao):
    x, y, z = posicao
    erro = x**2 + y**2 + z**2
    return erro

NUM_PARTICULAS = 40
ITERATIVAS = 100
W, C1, C2 = 0.5, 1.5, 1.5

class Particula:
    def __init__(self):
        self.posicao = [random.uniform(-10, 10) for _ in range(3)]
        self.velocidade = [random.uniform(-1, 1) for _ in range(3)]
        self.melhor_posicao = list(self.posicao)
        self.melhor_erro = calcular_fitness(self.posicao)

enxame = [Particula() for _ in range(NUM_PARTICULAS)]
gbest_posicao = list(enxame[0].posicao)
gbest_erro = calcular_fitness(gbest_posicao)

for p in enxame:
    if p.melhor_erro < gbest_erro:
        gbest_erro = p.melhor_erro
        gbest_posicao = list(p.posicao)

for t in range(ITERATIVAS):
    for p in enxame:
        for i in range(3):
            r1, r2 = random.random(), random.random()
            p.velocidade[i] = (W * p.velocidade[i] + 
                               C1 * r1 * (p.melhor_posicao[i] - p.posicao[i]) + 
                               C2 * r2 * (gbest_posicao[i] - p.posicao[i]))
            p.posicao[i] += p.velocidade[i]
            
        erro_atual = calcular_fitness(p.posicao)
        if erro_atual < p.melhor_erro:
            p.melhor_erro = erro_atual
            p.melhor_posicao = list(p.posicao)
            if erro_atual < gbest_erro:
                gbest_erro = erro_atual
                gbest_posicao = list(p.posicao)

x, y, z = gbest_posicao
print(f"--- Melhor Solução PSO ---")
print(f"x = {x:.8f}, y = {y:.8f}, z = {z:.8f}")
print(f"f(x, y, z) = {gbest_erro:.10f}")