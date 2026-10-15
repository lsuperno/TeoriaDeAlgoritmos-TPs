"""
Genera los sets de datos del Ejercicio 1 en la carpeta sets/.

- Sets tipicos: generados con crear_mochila.py (provisto por la catedra),
  con una semilla fija para que la generacion sea reproducible.
- Sets de peor caso: armados manualmente para que las podas del
  backtracking sean poco efectivas (ver informe, seccion de sets de datos).

Uso: python3 generar_sets.py
"""

import os
import random
import importlib

SEMILLA = 2026

# Tamanios para fuerza bruta (y BT en el mismo rango, para comparar)
TAMANIOS_FB = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
# Tamanios adicionales solo para backtracking
TAMANIOS_BT = [50, 100, 200, 300, 500, 750, 1000, 1500, 2000]
# Tamanios de los sets de peor caso
TAMANIOS_PEOR_CASO = [10, 12, 14, 16, 18, 20, 22]

DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_SETS = os.path.join(DIR_BASE, "sets")
DIR_TP1 = os.path.dirname(DIR_BASE)  # crear_mochila.py esta en la carpeta TP1/


def generar_sets_tipicos():
    # crear_mochila.py escribe "mochila<n>.txt" en el directorio actual
    os.chdir(DIR_SETS)
    crear = importlib.import_module("crear_mochila")  # al importarlo genera mochila1000.txt
    random.seed(SEMILLA)                               # se fija la semilla despues del import
    for n in sorted(set(TAMANIOS_FB + TAMANIOS_BT)):
        crear.crear_mochila(n)                         # sobrescribe mochila1000.txt con la semilla
    os.chdir(DIR_BASE)


def generar_sets_peor_caso():
    # beneficio = peso, pesos pares y capacidad impar:
    # todos los items tienen la misma relacion beneficio/peso y ninguna
    # combinacion llena exactamente la mochila, por lo que la cota fraccional
    # siempre supera en 1 a la mejor solucion y casi nunca poda.
    rnd = random.Random(SEMILLA)
    for n in TAMANIOS_PEOR_CASO:
        pesos = [2 * rnd.randint(1, 100) for _ in range(n)]
        capacidad = sum(pesos) // 2
        if capacidad % 2 == 0:
            capacidad += 1
        with open(os.path.join(DIR_SETS, f"peor_caso{n}.txt"), "w") as f:
            f.write(f"{capacidad}\n")
            for p in pesos:
                f.write(f"{p},{p}\n")


def main():
    os.makedirs(DIR_SETS, exist_ok=True)
    import sys
    sys.path.insert(0, DIR_TP1)
    generar_sets_tipicos()
    generar_sets_peor_caso()
    print(f"Sets generados en {DIR_SETS}")


if __name__ == "__main__":
    main()
