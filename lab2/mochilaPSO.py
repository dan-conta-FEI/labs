import random

caixas = [
    [4, 12],  # Verde
    [10, 4],  # Amarela
    [2, 1],   # Cinza
    [2, 2],   # Azul
    [1, 1]    # Laranja
]
LIMITE_PESO = 15

NUM_PARTICULAS = 50
ITERATIVEIS = 100
W = 0.5   
C1 = 1.5 
C2 = 1.5

# Fitness
def calcular_fitness(posicao):
    qtds = [max(0, int(round(p))) for p in posicao]
    peso_total = sum(qtds[i] * caixas[i][1] for i in range(5))
    valor_total = sum(qtds[i] * caixas[i][0] for i in range(5))
    
    if peso_total > LIMITE_PESO:
        return 0
    return valor_total

# Inicialização da Partícula
class Particula:
    def __init__(self):
        self.posicao = [random.uniform(0, 3) for _ in range(5)]
        self.velocidade = [random.uniform(-1, 1) for _ in range(5)]
        self.melhor_posicao = list(self.posicao)
        self.melhor_fitness = calcular_fitness(self.posicao)

# Criar enxame
enxame = [Particula() for _ in range(NUM_PARTICULAS)]
gbest_posicao = list(enxame[0].posicao)
gbest_fitness = -1

# Identificar o melhor global inicial
for p in enxame:
    if p.melhor_fitness > gbest_fitness:
        gbest_fitness = p.melhor_fitness
        gbest_posicao = list(p.posicao)

for t in range(ITERATIVEIS):
    for p in enxame:
        for i in range(5):
            r1, r2 = random.random(), random.random()
            
            cognitivo = C1 * r1 * (p.melhor_posicao[i] - p.posicao[i])
            social = C2 * r2 * (gbest_posicao[i] - p.posicao[i])
            p.velocidade[i] = W * p.velocidade[i] + cognitivo + social
            
            p.posicao[i] += p.velocidade[i]
            
            p.posicao[i] = max(0, min(5, p.posicao[i]))
            
        fitness_atual = calcular_fitness(p.posicao)
        
        if fitness_atual > p.melhor_fitness:
            p.melhor_fitness = fitness_atual
            p.melhor_posicao = list(p.posicao)
            
            if fitness_atual > gbest_fitness:
                gbest_fitness = fitness_atual
                gbest_posicao = list(p.posicao)

melhor_qtds = [max(0, int(round(p))) for p in gbest_posicao]
print(f"Melhor combinação (Qtd de cada caixa): {melhor_qtds}")
print(f"Valor Total: R$ {gbest_fitness}")
print(f"Peso Total: {sum(melhor_qtds[i] * caixas[i][1] for i in range(5))} kg")