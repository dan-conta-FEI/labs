import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


X, y = fetch_california_housing(return_X_y=True)


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


def avaliar(nome, modelo, Xtr, Xte, ytr, yte):
    y_pred_train = modelo.predict(Xtr)
    y_pred_test = modelo.predict(Xte)

    metrics_train = {
        "MAE": mean_absolute_error(ytr, y_pred_train),
        "MSE": mean_squared_error(ytr, y_pred_train),
        "RMSE": np.sqrt(mean_squared_error(ytr, y_pred_train)),
        "R2": r2_score(ytr, y_pred_train),
    }
    metrics_test = {
        "MAE": mean_absolute_error(yte, y_pred_test),
        "MSE": mean_squared_error(yte, y_pred_test),
        "RMSE": np.sqrt(mean_squared_error(yte, y_pred_test)),
        "R2": r2_score(yte, y_pred_test),
    }

    print(f"\n--- {nome} ---")
    print("Treino:", {k: round(v, 4) for k, v in metrics_train.items()})
    print("Teste: ", {k: round(v, 4) for k, v in metrics_test.items()})

    r2_gap = metrics_train["R2"] - metrics_test["R2"]
    if r2_gap > 0.1:
        print(f"    -> possivel overfitting (gap R2 treino-teste = {r2_gap:.4f})")
    elif metrics_train["R2"] < 0.5 and metrics_test["R2"] < 0.5:
        print("    -> possivel underfitting (R2 baixo em treino e teste)")

    return {
        "nome": nome,
        "modelo": modelo,
        "metrics_train": metrics_train,
        "metrics_test": metrics_test,
        "y_pred_test": y_pred_test,
    }


resultados = []


lin_reg = LinearRegression()
lin_reg.fit(X_train_scaled, y_train)
resultados.append(
    avaliar("Regressao Linear (com scaling)", lin_reg, X_train_scaled, X_test_scaled, y_train, y_test)
)


ks = [3, 5, 7, 9, 15]
for k in ks:
    knn_reg = KNeighborsRegressor(n_neighbors=k)
    knn_reg.fit(X_train_scaled, y_train)
    resultados.append(
        avaliar(f"KNN Regressor (K={k}, com scaling)", knn_reg, X_train_scaled, X_test_scaled, y_train, y_test)
    )

knn_sem_scaling = KNeighborsRegressor(n_neighbors=5)
knn_sem_scaling.fit(X_train, y_train)
resultados.append(
    avaliar("KNN Regressor (K=5, SEM scaling)", knn_sem_scaling, X_train, X_test, y_train, y_test)
)


melhor = max(resultados, key=lambda r: r["metrics_test"]["R2"])
print(f"\nMelhor modelo: {melhor['nome']} | R2 teste = {melhor['metrics_test']['R2']:.4f}")


plt.figure(figsize=(6, 6))
plt.scatter(y_test, melhor["y_pred_test"], alpha=0.3, s=10)
lims = [min(y_test.min(), melhor["y_pred_test"].min()), max(y_test.max(), melhor["y_pred_test"].max())]
plt.plot(lims, lims, "r--", label="Previsao perfeita")
plt.xlabel("Valor real")
plt.ylabel("Valor previsto")
plt.title(f"Previsto x Real - {melhor['nome']}")
plt.legend()
plt.tight_layout()
plt.savefig("regressao_previsto_vs_real.png", dpi=150)
plt.close()
print("Grafico salvo: regressao_previsto_vs_real.png")


nomes = [r["nome"] for r in resultados]
r2_train = [r["metrics_train"]["R2"] for r in resultados]
r2_test = [r["metrics_test"]["R2"] for r in resultados]

x = np.arange(len(nomes))
width = 0.35

plt.figure(figsize=(12, 6))
plt.bar(x - width / 2, r2_train, width, label="Treino")
plt.bar(x + width / 2, r2_test, width, label="Teste")
plt.xticks(x, nomes, rotation=45, ha="right")
plt.ylabel("R2")
plt.title("Comparacao de R2 (treino x teste) entre modelos")
plt.legend()
plt.tight_layout()
plt.savefig("regressao_r2_comparacao.png", dpi=150)
plt.close()
print("Grafico salvo: regressao_r2_comparacao.png")