import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Universo de discurso e variaveis linguisticas
universo = np.arange(0, 101, 1)

distancia = ctrl.Antecedent(universo, 'distancia')
velocidade = ctrl.Antecedent(universo, 'velocidade')
pressao = ctrl.Consequent(universo, 'pressao')

distancia['curta'] = fuzz.trimf(distancia.universe, [0, 0, 40])
distancia['media']  = fuzz.trimf(distancia.universe, [20, 50, 80])
distancia['longa']  = fuzz.trimf(distancia.universe, [60, 100, 100])

velocidade['lenta']     = fuzz.trimf(velocidade.universe, [0, 0, 40])
velocidade['moderada']  = fuzz.trimf(velocidade.universe, [20, 50, 80])
velocidade['rapida']    = fuzz.trimf(velocidade.universe, [60, 100, 100])

pressao['suave'] = fuzz.trimf(pressao.universe, [0, 0, 40])
pressao['media'] = fuzz.trimf(pressao.universe, [20, 50, 80])
pressao['forte'] = fuzz.trimf(pressao.universe, [60, 100, 100])

# 2. Regras 
regras = [
    ctrl.Rule(distancia['curta'] & velocidade['lenta'],     pressao['media']),
    ctrl.Rule(distancia['curta'] & velocidade['moderada'],  pressao['forte']),
    ctrl.Rule(distancia['curta'] & velocidade['rapida'],    pressao['forte']),

    ctrl.Rule(distancia['media'] & velocidade['lenta'],     pressao['suave']),
    ctrl.Rule(distancia['media'] & velocidade['moderada'],  pressao['media']),
    ctrl.Rule(distancia['media'] & velocidade['rapida'],    pressao['forte']),

    ctrl.Rule(distancia['longa'] & velocidade['lenta'],     pressao['suave']),
    ctrl.Rule(distancia['longa'] & velocidade['moderada'],  pressao['suave']),
    ctrl.Rule(distancia['longa'] & velocidade['rapida'],    pressao['media']),
]

sistema_ctrl = ctrl.ControlSystem(regras)
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)


def calcular_pressao(dist_m: float, vel_kmh: float) -> float:
    """Recebe distancia (m) e velocidade (km/h) e retorna a pressao no freio (%)."""
    sistema.input['distancia'] = dist_m
    sistema.input['velocidade'] = vel_kmh
    sistema.compute()
    return sistema.output['pressao']


if __name__ == "__main__":
    casos_teste = [
        (0,   100),  # pior caso
        (5,   90),   
        (100, 0),    # melhor caso
        (95,  5),
        (50,  50),   # caso intermediario
        (10,  10),  
        (90,  90),   
    ]

    print(f"{'Distância(m)':>13} | {'Velocidade(km/h)':>17} | {'Pressao no freio(%)':>19}")
    print("-" * 56)
    for d, v in casos_teste:
        p = calcular_pressao(d, v)
        print(f"{d:>13} | {v:>17} | {p:>19.2f}")

    valores = []
    for d in range(0, 101, 2):
        for v in range(0, 101, 2):
            valores.append(calcular_pressao(d, v))

    print("\nValor minimo de pressao obtido:", round(min(valores), 2), "%")
    print("Valor maximo de pressao obtido:", round(max(valores), 2), "%")