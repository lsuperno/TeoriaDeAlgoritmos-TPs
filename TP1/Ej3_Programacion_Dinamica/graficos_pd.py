"""
Ejercicio 3 - Medición de tiempos y gráficos de los dos planteos de programación dinámica.

Lee los sets de la carpeta sets/ (los mismos que se entregan), mide los dos
algoritmos, ajusta la curva teórica y guarda:
    resultados/resultados_pd.csv               tabla de mediciones
    graficos/grafico_pd_max_beneficio.png      algoritmo 1: medido vs. teórico c·n·W
    graficos/grafico_pd_min_peso.png           algoritmo 2: medido vs. teórico c·n·B
    graficos/grafico_pd_comparacion.png        comparación de los dos algoritmos

Uso (parado en la carpeta Ej3_Programacion_Dinamica):
    python3 graficos_pd.py

Requiere numpy y matplotlib (pip install numpy matplotlib).
"""

import csv
import gc
import os
import platform
import sys
import time

import matplotlib

matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import numpy as np

from mochila_programacion_dinamica1 import leer_mochila, mochila_max_beneficio
from mochila_programacion_dinamica2 import mochila_min_peso

TAMANIOS = [20, 40, 80, 120, 160, 200, 250]   
REPETICIONES = 3                              
CARPETA_SETS = "sets"
CARPETA_RESULTADOS = "resultados"
CARPETA_GRAFICOS = "graficos"


def medir(funcion, *argumentos):
    """Ejecuta la función REPETICIONES veces y devuelve (menor tiempo, resultado)."""
    tiempos = []
    resultado = None
    for _ in range(REPETICIONES):
        gc.collect()
        gc.disable()                      
        inicio = time.perf_counter()
        resultado = funcion(*argumentos)
        tiempos.append(time.perf_counter() - inicio)
        gc.enable()
    return min(tiempos), resultado


def ajustar(t, f):
    """Ajuste por cuadrados mínimos de t = c·f. Devuelve (c, R²)."""
    t, f = np.array(t), np.array(f, dtype=float)
    c = np.sum(t * f) / np.sum(f * f)
    ss_res = np.sum((t - c * f) ** 2)
    ss_tot = np.sum((t - t.mean()) ** 2)
    return c, 1 - ss_res / ss_tot


def grafico(ns, series, titulo, archivo):
    plt.figure(figsize=(7, 4.5))
    for valores, formato, etiqueta in series:
        plt.plot(ns, valores, formato, label=etiqueta)
    plt.xlabel("Tamaño del problema (n)")
    plt.ylabel("Tiempo (s)")
    plt.title(titulo)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, archivo), dpi=150)
    plt.close()


def main():
    print(f"Python {sys.version.split()[0]} - {platform.platform()}")
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)   # crea las carpetas si no existen
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    filas = []   

    for n in TAMANIOS:
        ruta = os.path.join(CARPETA_SETS, f"mochila{n}.txt")
        if not os.path.exists(ruta):
            print(f"No existe {ruta}. Ejecutar desde la carpeta Ej3_Programacion_Dinamica.")
            sys.exit(1)
        W, elementos = leer_mochila(ruta)

      
        t1, (beneficio_max, items1) = medir(mochila_max_beneficio, elementos, W)

        
        B = beneficio_max
        t2, (peso_min, items2) = medir(mochila_min_peso, elementos, B)

        
        assert peso_min <= W, "el peso mínimo no puede superar la capacidad"
        assert sum(b for _, b in items1) == beneficio_max
        assert sum(p for p, _ in items1) <= W
        assert sum(b for _, b in items2) == B

        filas.append((n, W, B, t1, t2, peso_min))
        print(f"n={n:<4} W={W:<6} B={B:<7} t1={t1:.4f}s  t2={t2:.4f}s  peso_min={peso_min}")

    ns = [f[0] for f in filas]
    t1 = [f[3] for f in filas]
    t2 = [f[4] for f in filas]
    f1 = [f[0] * f[1] for f in filas]    # n * W
    f2 = [f[0] * f[2] for f in filas]    # n * B

    c1, r2_1 = ajustar(t1, f1)
    c2, r2_2 = ajustar(t2, f2)

    grafico(ns, [(t1, "o-", "Tiempo medido"),
                 ([c1 * f for f in f1], "s--", "Teórico O(n·W)")],
            "PD - Maximizar beneficio: medido vs. teórico", "grafico_pd_max_beneficio.png")
    grafico(ns, [(t2, "o-", "Tiempo medido"),
                 ([c2 * f for f in f2], "s--", "Teórico O(n·B)")],
            "PD - Minimizar peso: medido vs. teórico", "grafico_pd_min_peso.png")
    grafico(ns, [(t1, "o-", "Maximizar beneficio (capacidad W)"),
                 (t2, "s-", "Minimizar peso (beneficio B)")],
            "Comparación de los dos algoritmos de PD", "grafico_pd_comparacion.png")

    with open(os.path.join(CARPETA_RESULTADOS, "resultados_pd.csv"), "w", newline="") as arch:
        w = csv.writer(arch)
        w.writerow(["n", "W", "B", "tiempo_max_beneficio_s", "tiempo_min_peso_s", "peso_min"])
        w.writerows(filas)

    print(f"\nGuardados: {CARPETA_RESULTADOS}/resultados_pd.csv y los 3 gráficos en {CARPETA_GRAFICOS}/")


if __name__ == "__main__":
    main()
