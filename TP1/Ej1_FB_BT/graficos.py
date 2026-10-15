"""
Genera los graficos del Ejercicio 1 a partir de los CSV de resultados/.
Los guarda en graficos/.

Curva teorica: T(n) = c * n * 2^n (complejidad O(n * 2^n) obtenida del
pseudocodigo). La constante c se ajusta con los tiempos medidos
(minimos cuadrados sobre log T), tomando solo tiempos >= 1e-4 s, porque
por debajo de ese valor domina el ruido de la medicion.

Uso: python3 graficos.py   (antes correr medir.py)
"""

import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_RES = os.path.join(DIR_BASE, "resultados")
DIR_GRAF = os.path.join(DIR_BASE, "graficos")

AZUL = "#2a78d6"     # medido
NARANJA = "#eb6834"  # teorico / segunda serie
VERDE = "#1baf7a"    # tercera serie
GRIS = "#6b6a63"

TIEMPO_MINIMO_AJUSTE = 1e-4


def leer(csv_nombre):
    with open(os.path.join(DIR_RES, csv_nombre)) as f:
        filas = list(csv.DictReader(f))
    ns = np.array([int(r["n"]) for r in filas])
    ts = np.array([float(r["tiempo_s"]) for r in filas])
    return ns, ts


def teorica(n):
    return n * 2.0 ** n


def ajustar_constante(ns, ts):
    """c tal que c * n * 2^n aproxima los tiempos (ajuste en escala log)."""
    mascara = ts >= TIEMPO_MINIMO_AJUSTE
    return math.exp(np.mean(np.log(ts[mascara]) - np.log(teorica(ns[mascara].astype(float)))))


def estilo(ax, titulo):
    ax.set_title(titulo, fontsize=12)
    ax.set_xlabel("n (cantidad de ítems)")
    ax.set_ylabel("Tiempo (segundos)")
    ax.grid(True, which="major", color="#d9d8d2", linewidth=0.6)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.legend(frameon=False)


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_GRAF, nombre), dpi=150)
    plt.close(fig)
    print(f"Generado graficos/{nombre}")


def grafico_fb():
    ns, ts = leer("fb_tipicos.csv")
    c = ajustar_constante(ns, ts)
    xs = np.linspace(ns.min(), ns.max(), 200)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    for ax, log in ((ax1, False), (ax2, True)):
        ax.plot(xs, c * teorica(xs), "--", color=NARANJA, linewidth=2,
                label=f"Teórica: c·n·2ⁿ (c = {c:.2e})")
        ax.plot(ns, ts, "o-", color=AZUL, linewidth=2, markersize=6, label="Medido")
        if log:
            ax.set_yscale("log")
        estilo(ax, "Fuerza bruta – escala " + ("logarítmica" if log else "lineal"))
    guardar(fig, "fb_tiempos.png")
    return c


def grafico_bt_peor_caso():
    ns, ts = leer("bt_peor_caso.csv")
    ns_fb, ts_fb = leer("fb_peor_caso.csv")
    c = ajustar_constante(ns, ts)
    xs = np.linspace(ns.min(), ns.max(), 200)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(xs, c * teorica(xs), "--", color=NARANJA, linewidth=2,
            label=f"Teórica BT: c·n·2ⁿ (c = {c:.2e})")
    ax.plot(ns, ts, "o-", color=AZUL, linewidth=2, markersize=6, label="BT medido")
    ax.plot(ns_fb, ts_fb, "s-", color=GRIS, linewidth=1.5, markersize=6,
            label="FB medido (mismos sets)")
    ax.set_yscale("log")
    estilo(ax, "Backtracking – sets de peor caso (escala logarítmica)")
    guardar(fig, "bt_peor_caso.png")
    return c


def grafico_bt_tipicos(c_peor_caso):
    ns, ts = leer("bt_tipicos.csv")

    # Ajuste empirico a*n^k para describir el comportamiento observado
    mascara = ns >= 50
    k, log_a = np.polyfit(np.log(ns[mascara]), np.log(ts[mascara]), 1)
    xs = np.linspace(ns.min(), ns.max(), 400)

    # Cota teorica de peor caso: solo se dibuja mientras entra en el grafico
    xs_cota = np.linspace(ns.min(), 40, 200)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(xs_cota, c_peor_caso * teorica(xs_cota), "--", color=NARANJA, linewidth=2,
            label="Cota teórica de peor caso: c·n·2ⁿ")
    ax.plot(xs, math.exp(log_a) * xs ** k, ":", color=VERDE, linewidth=2,
            label=f"Ajuste empírico: a·n^{k:.2f}")
    ax.plot(ns, ts, "o-", color=AZUL, linewidth=2, markersize=6, label="BT medido")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylim(ts.min() / 3, max(ts.max() * 30, 10))
    estilo(ax, "Backtracking – sets de crear_mochila.py (escala log-log)")
    guardar(fig, "bt_tipicos.png")
    return k


def grafico_comparativo():
    ns_fb, ts_fb = leer("fb_tipicos.csv")
    ns_bt, ts_bt = leer("bt_tipicos.csv")
    ns_pc, ts_pc = leer("bt_peor_caso.csv")
    rango = ns_bt <= ns_fb.max()

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(ns_fb, ts_fb, "o-", color=AZUL, linewidth=2, markersize=6,
            label="Fuerza bruta")
    ax.plot(ns_pc, ts_pc, "^-", color=NARANJA, linewidth=2, markersize=6,
            label="Backtracking – peor caso")
    ax.plot(ns_bt[rango], ts_bt[rango], "s-", color=VERDE, linewidth=2, markersize=6,
            label="Backtracking – crear_mochila.py")
    ax.set_yscale("log")
    estilo(ax, "Comparativo FB vs BT en el mismo rango de n (escala logarítmica)")
    guardar(fig, "comparativo.png")


def main():
    os.makedirs(DIR_GRAF, exist_ok=True)
    c_fb = grafico_fb()
    c_pc = grafico_bt_peor_caso()
    k = grafico_bt_tipicos(c_pc)
    grafico_comparativo()
    print(f"Constante FB: {c_fb:.3e} | constante BT peor caso: {c_pc:.3e} | "
          f"exponente empirico BT tipico: {k:.2f}")


if __name__ == "__main__":
    main()
