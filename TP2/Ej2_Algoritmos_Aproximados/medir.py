import csv
import os
import time

from mochila_aproximada import lectura_archivo, mochila_aproximada

BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA_SETS = os.path.join(BASE, "sets")
CARPETA_RESULTADOS = os.path.join(BASE, "resultados")

TAMANIOS = [10, 20, 50, 100, 200]
EPSILONS = [0.9, 0.5, 0.25, 0.1]
LIMITE_CELDAS = 40_000_000  # cota n^3/eps: evita tablas que no entran en memoria


def mochila_optima(capacidad, elementos):
    # DP exacta por peso. Reemplazar por la función del TP1 si se prefiere.
    dp = [0] * (capacidad + 1)
    for peso, beneficio in elementos:
        for c in range(capacidad, peso - 1, -1):
            if dp[c - peso] + beneficio > dp[c]:
                dp[c] = dp[c - peso] + beneficio
    return dp[capacidad]


def main():
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    ruta_csv = os.path.join(CARPETA_RESULTADOS, "resultados_aproximado.csv")

    with open(ruta_csv, "w", newline="") as arch:
        escritor = csv.writer(arch)
        escritor.writerow(
            ["n", "epsilon", "beneficio_aprox", "beneficio_optimo", "cociente", "tiempo_s"]
        )

        for n in TAMANIOS:
            capacidad, elementos = lectura_archivo(
                os.path.join(CARPETA_SETS, f"mochila{n}.txt")
            )
            optimo = mochila_optima(capacidad, elementos)

            for epsilon in EPSILONS:
                if n**3 / epsilon > LIMITE_CELDAS:
                    print(f"n = {n}, eps = {epsilon}: omitido (tabla demasiado grande)") # Lo omito por que me queda muy grande
                    continue

                inicio = time.perf_counter()
                beneficio, _ = mochila_aproximada(capacidad, elementos, epsilon)
                tiempo = time.perf_counter() - inicio

                cociente = beneficio / optimo if optimo > 0 else 1
                escritor.writerow([n, epsilon, beneficio, optimo, f"{cociente:.4f}", f"{tiempo:.4f}"])
                print(f"n = {n}, eps = {epsilon}: {beneficio}/{optimo} en {tiempo:.3f} s")


if __name__ == "__main__":
    main()
