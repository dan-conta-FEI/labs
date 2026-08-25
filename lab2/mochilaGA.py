import random

caixas = [
    [4, 12],  # Verde
    [10, 4],  # Amarela
    [2, 1],   # Cinza
    [2, 2],   # Azul
    [1, 1]    # Laranja
]
LIMITE_PESO = 15

TAM_POPULACAO = 50
GERACOES = 100
TAXA_CROSSOVER = 0.8
TAXA_MUTACAO = 0.2

# Fitness
def calcular_fitness(indivíduo):
    peso_total = sum(indivíduo[i] * caixas[i][1] for i in range(5))
    valor_total = sum(indivíduo[i] * caixas[i][0] for i in range(5))
    if peso_total > LIMITE_PESO:
        return 0
    return valor_total

# Pop inicial
def criar_populacao():
    return [[random.randint(0, 3) for _ in range(5)] for _ in range(TAM_POPULACAO)]

# Roleta
def selecao_roleta(populacao, fitnesses):
    soma_fitness = sum(fitnesses)
    if soma_fitness == 0:
        return random.choice(populacao)
    pick = random.uniform(0, soma_fitness)
    atual = 0
    for i, f in enumerate(fitnesses):
        atual += f
        if atual >= pick:
            return populacao[i]
    return populacao[-1]

# Crossover
def crossover(pai1, pai2):
    if random.random() < TAXA_CROSSOVER:
        ponto = random.randint(1, 4)
        filho1 = pai1[:ponto] + pai2[ponto:]
        filho2 = pai2[:ponto] + pai1[ponto:]
        return filho1, filho2
    return pai1.copy(), pai2.copy()

# Mutação
def mutacao(indivíduo):
    if random.random() < TAXA_MUTACAO:
        gene = random.randint(0, 4)
        variacao = random.choice([-1, 1])
        indivíduo[gene] = max(0, indivíduo[gene] + variacao)
    return indivíduo

populacao = criar_populacao()

for geracao in range(GERACOES):
    fitnesses = [calcular_fitness(ind) for ind in populacao]
    nova_populacao = []
    
    while len(nova_populacao) < TAM_POPULACAO:
        pai1 = selecao_roleta(populacao, fitnesses)
        pai2 = selecao_roleta(populacao, fitnesses)
        filho1, filho2 = crossover(pai1, pai2)
        nova_populacao.append(mutacao(filho1))
        if len(nova_populacao) < TAM_POPULACAO:
            nova_populacao.append(mutacao(filho2))
            
    populacao = nova_populacao

fitnesses = [calcular_fitness(ind) for ind in populacao]
melhor_idx = fitnesses.index(max(fitnesses))
melhor_solucao = populacao[melhor_idx]

print(f"Melhor combinação (Qtd de cada caixa): {melhor_solucao}")
print(f"Valor Total: R$ {calcular_fitness(melhor_solucao)}")
print(f"Peso Total: {sum(melhor_solucao[i] * caixas[i][1] for i in range(5))} kg")