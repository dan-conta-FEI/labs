import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


scaler_std = StandardScaler()
X_train_std = scaler_std.fit_transform(X_train)
X_test_std = scaler_std.transform(X_test)

scaler_norm = MinMaxScaler()
X_train_norm = scaler_norm.fit_transform(X_train)
X_test_norm = scaler_norm.transform(X_test)

datasets = {
    "Sem scaling": (X_train, X_test),
    "Padronizado (Standard)": (X_train_std, X_test_std),
    "Normalizado (MinMax)": (X_train_norm, X_test_norm),
}

ks = [1, 3, 5, 7]

resultados = []  
for nome_dataset, (Xtr, Xte) in datasets.items():
    for k in ks:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(Xtr, y_train)

        y_pred_train = knn.predict(Xtr)
        y_pred_test = knn.predict(Xte)

        acc_train = accuracy_score(y_train, y_pred_train)
        acc_test = accuracy_score(y_test, y_pred_test)

        resultados.append(
            {
                "dataset": nome_dataset,
                "k": k,
                "acc_train": acc_train,
                "acc_test": acc_test,
                "y_pred_test": y_pred_test,
                "modelo": knn,
            }
        )

        print(f"[{nome_dataset}] K={k} | Acuracia treino: {acc_train:.4f} | Acuracia teste: {acc_test:.4f}")
        diff = acc_train - acc_test
        if diff > 0.05:
            print(f"    -> possivel overfitting (gap treino-teste = {diff:.4f})")
        elif acc_train < 0.9 and acc_test < 0.9:
            print(f"    -> possivel underfitting (ambas as acuracias baixas)")
        print()


print("\n" + "=" * 70)
print("RELATORIOS DE CLASSIFICACAO (conjunto de teste)")
print("=" * 70)
for r in resultados:
    print(f"\n--- {r['dataset']} | K={r['k']} ---")
    print(classification_report(y_test, r["y_pred_test"], target_names=["maligno", "benigno"]))


fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for nome_dataset in datasets.keys():
    accs_train = [r["acc_train"] for r in resultados if r["dataset"] == nome_dataset]
    accs_test = [r["acc_test"] for r in resultados if r["dataset"] == nome_dataset]
    axes[0].plot(ks, accs_train, marker="o", label=nome_dataset)
    axes[1].plot(ks, accs_test, marker="o", label=nome_dataset)

axes[0].set_title("Acuracia no treino x K")
axes[0].set_xlabel("K (n_neighbors)")
axes[0].set_ylabel("Acuracia")
axes[0].set_xticks(ks)
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].set_title("Acuracia no teste x K")
axes[1].set_xlabel("K (n_neighbors)")
axes[1].set_ylabel("Acuracia")
axes[1].set_xticks(ks)
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("classificacao_acuracia_k.png", dpi=150)
plt.close()
print("\nGrafico salvo: classificacao_acuracia_k.png")


melhor = max(resultados, key=lambda r: r["acc_test"])
print(
    f"\nMelhor modelo: {melhor['dataset']} | K={melhor['k']} "
    f"| Acuracia teste = {melhor['acc_test']:.4f}"
)

cm = confusion_matrix(y_test, melhor["y_pred_test"])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["maligno", "benigno"])
disp.plot(cmap="Blues")
plt.title(f"Matriz de Confusao - {melhor['dataset']}, K={melhor['k']}")
plt.tight_layout()
plt.savefig("classificacao_matriz_confusao.png", dpi=150)
plt.close()
print("Grafico salvo: classificacao_matriz_confusao.png")