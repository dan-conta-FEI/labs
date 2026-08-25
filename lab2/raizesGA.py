import random

def calcular_fitness(individuo):
    x, y, z = individuo
    erro = x**2 + y**2 + z**2
    
    return 1 / (1 + erro)

TAM_POPULACAO = 50
GERACOES = 100
TAXA_MUTACAO = 0.1
INTERVALO_MIN = -10.0
INTERVALO_MAX = 10.0


populacao = [
    [random.uniform(INTERVALO_MIN, INTERVALO_MAX) for _ in range(3)]
    for _ in range(TAM_POPULACAO)
]

for geracao in range(GERACOES):
    avaliados = [(ind, calcular_fitness(ind)) for ind in populacao]
    avaliados.sort(key=lambda item: item[1], reverse=True)
    
    nova_populacao = [ind for ind, fit in avaliados[:5]]
    
    while len(nova_populacao) < TAM_POPULACAO:
        pai1 = max(random.sample(avaliados, 3), key=lambda x: x[1])[0]
        pai2 = max(random.sample(avaliados, 3), key=lambda x: x[1])[0]
        
        filho = [
            (pai1[i] + pai2[i]) / 2
            for i in range(3)
        ]
        
        for i in range(3):
            if random.random() < TAXA_MUTACAO:
                filho[i] += random.gauss(0, 0.5)
                filho[i] = max(INTERVALO_MIN, min(INTERVALO_MAX, filho[i]))
                
        nova_populacao.append(filho)
        
    populacao = nova_populacao

melhor_solucao = max(populacao, key=calcular_fitness)
x, y, z = melhor_solucao
resultado_f = x**2 + y**2 + z**2

print(f"--- Melhor Indivíduo Encontrado ---")
print(f"x = {x:.6f}")
print(f"y = {y:.6f}")
print(f"z = {z:.6f}")
print(f"f(x, y, z) = {resultado_f:.8f}  (aproximar de 0)")