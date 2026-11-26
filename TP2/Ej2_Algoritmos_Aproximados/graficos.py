import csv
import os

import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(BASE, "resultados", "resultados_aproximado.csv")
CARPETA_GRAFICOS = os.path.join(BASE, "graficos")


def leer_resultados():
    with open(RUTA_CSV, newline="") as arch:
        return [
            {
                "n": int(f["n"]),
                "epsilon": float(f["epsilon"]),
                "cociente": float(f["cociente"]),
                "tiempo": float(f["tiempo_s"]),
            }
            for f in csv.DictReader(arch)
        ]


def guardar(nombre):
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, nombre), dpi=150)
    plt.close()


def main():
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    datos = leer_resultados()
    epsilons = sorted({d["epsilon"] for d in datos}, reverse=True)
    tamanios = sorted({d["n"] for d in datos})

    # Tiempo en función de n: medido vs teórico c·n³/ε, una curva por epsilon
    colores = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for i, eps in enumerate(epsilons):
        pts = [d for d in datos if d["epsilon"] == eps]
        ns = [d["n"] for d in pts]
        tiempos = [d["tiempo"] for d in pts]
        teorico = [n**3 / eps for n in ns]
        c = sum(t * f for t, f in zip(tiempos, teorico)) / sum(f * f for f in teorico)
        color = colores[i % len(colores)]
        plt.plot(ns, tiempos, marker="o", color=color, label=f"Medido (ε = {eps})")
        plt.plot(ns, [c * f for f in teorico], "--", color=color, label=f"Teórico c·n³/ε (ε = {eps})")
    plt.xscale("log")
    plt.xlabel("n (cantidad de elementos) - Escala logarítmica")
    plt.ylabel("Tiempo de ejecución (s)")
    plt.title("Tiempo de ejecución - Aproximado (escala semilog-X)")
    plt.legend(fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.5)
    guardar("tiempo_vs_n.png")

    # Tiempo en función de 1/epsilon, una curva por n
    for n in tamanios:
        pts = [d for d in datos if d["n"] == n]
        plt.plot([1 / d["epsilon"] for d in pts], [d["tiempo"] for d in pts], marker="o", label=f"n = {n}")
    plt.xlabel("1 / ε")
    plt.ylabel("Tiempo de ejecución (s)")
    plt.title("Tiempo en función de 1/ε")
    plt.legend()
    plt.grid(True)
    guardar("tiempo_vs_inv_epsilon.png")

    # Cociente aproximado/óptimo contra la cota (1 - epsilon)
    for n in tamanios:
        pts = [d for d in datos if d["n"] == n]
        plt.plot([d["epsilon"] for d in pts], [d["cociente"] for d in pts], marker="o", label=f"n = {n}")
    xs = sorted({d["epsilon"] for d in datos})
    plt.plot(xs, [1 - e for e in xs], "k--", label="cota 1 − ε")
    plt.xlabel("ε")
    plt.ylabel("Beneficio aproximado / óptimo")
    plt.title("Calidad de la aproximación")
    plt.legend()
    plt.grid(True)
    guardar("cociente_vs_epsilon.png")


if __name__ == "__main__":
    main()
