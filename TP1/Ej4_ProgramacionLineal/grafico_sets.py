import os
import time
import matplotlib.pyplot as plt
import numpy as np

"""
Los sets utilizados son los mismos que se utilizan en el informe y se encuentran en sets/
"""

from mochila_programacion_lineal import mochila_pulp


def leer_mochila_desde_archivo(ruta: str) -> tuple[list[tuple[int, int]], int]:
    """Lee una mochila desde una ruta de archivo dada."""
    items = []
    with open(ruta, "r", encoding="utf-8") as arch:
        capacidad = int(arch.readline().strip())
        for linea in arch:
            linea = linea.strip()
            if linea:
                peso, benef = linea.split(",")
                items.append((int(peso), int(benef)))
    return items, capacidad


# Medir los tiempos cargando los sets de la carpeta sets/
tamanos = [10, 50, 100, 500, 1000, 2500, 5000, 10000, 20000, 30000, 40000]
tiempos = []

# Directorio base del script y carpeta sets
dir_base = os.path.dirname(os.path.abspath(__file__))
dir_sets = os.path.join(dir_base, "sets")

print("Midiendo tiempos sobre los sets de datos...")

for n in tamanos:
    ruta = os.path.join(dir_sets, f"mochila{n}.txt")
    if not os.path.exists(ruta):
        ruta = os.path.join(dir_base, f"mochila{n}.txt")

    if not os.path.exists(ruta):
        print(f"No se encontró archivo para n = {n}")
        continue

    items, capacidad = leer_mochila_desde_archivo(ruta)

    # Medir el tiempo de resolucion de PL
    inicio = time.perf_counter()
    beneficio = mochila_pulp(items, capacidad)
    fin = time.perf_counter()

    tiempo_total = fin - inicio
    tiempos.append(tiempo_total)
    print(f"  n = {n:<5} -> Tiempo: {tiempo_total:.4f} s (Beneficio: {beneficio})")

x_data = np.array(tamanos)
y_data = np.array(tiempos)

# Curva teórica O(2^n)
y_teorica = y_data[0] * (2 ** (x_data / 1500))

plt.figure(figsize=(10, 6))

# Dibujamos ambas curvas
plt.plot(x_data, y_teorica, "--", label="$O(2^n)$", color="red", linewidth=2)
plt.plot(x_data, y_data, "o-", label="Tiempo Medido", color="blue", linewidth=2.5)

plt.ylim(0, max(y_data) * 1.2)

plt.title("Tiempo de ejecución - Programacion lineal")
plt.xlabel("Cantidad de items (N)")
plt.ylabel("Tiempo de ejecución (segundos)")
plt.legend()
plt.grid(True)

plt.show()
