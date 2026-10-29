"""
Ejercicio 3 - Generación de los sets de datos.

Usa la función crear_mochila de la cátedra (copiada sin cambios en su cuerpo) y
genera un archivo sets/mochila<n>.txt por cada tamaño de TAMANIOS.

Para que los sets sean reproducibles se fija la semilla del generador antes de
crear cada uno. Los archivos que ya vienen en la entrega son exactamente los que
produce este script: no hace falta volver a generarlos para medir.

Uso (desde la carpeta Ej3_Programacion_Dinamica):
    python3 generar_sets.py
"""

import os
import random
from random import randint

TAMANIOS = [20, 40, 80, 120, 160, 200, 250]
SEMILLA_BASE = 2026
CARPETA_SETS = "sets"


# Función de la cátedra (crear_mochila.py)
def crear_mochila(n):
    nombre = "mochila" + str(n) + ".txt"
    arch = open(nombre, "w")
    cap = n * 50
    arch.write(str(cap) + "\n")
    for i in range(n):
        peso = randint(1, 200)
        benef = randint(1, 1000)
        arch.write(str(peso) + "," + str(benef) + "\n")
    arch.close()



def main():
    os.makedirs(CARPETA_SETS, exist_ok=True)
    carpeta_original = os.getcwd()
    os.chdir(CARPETA_SETS)          
    try:
        for n in TAMANIOS:
            random.seed(SEMILLA_BASE + n)
            crear_mochila(n)
            print(f"Generado {CARPETA_SETS}/mochila{n}.txt (n = {n}, W = {50 * n})")
    finally:
        os.chdir(carpeta_original)


if __name__ == "__main__":
    main()
