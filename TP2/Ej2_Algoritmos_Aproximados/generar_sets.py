import os
import random
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE, ".."))

from crear_mochila import crear_mochila

TAMANIOS = [10, 20, 50, 100, 200]
CARPETA_SETS = os.path.join(BASE, "sets")


def main():
    os.makedirs(CARPETA_SETS, exist_ok=True)
    os.chdir(BASE)

    for n in TAMANIOS:
        random.seed(n)  # misma instancia en cada corrida
        crear_mochila(n)
        os.replace(f"mochila{n}.txt", os.path.join(CARPETA_SETS, f"mochila{n}.txt"))
        print(f"Set generado: n = {n}")


if __name__ == "__main__":
    main()
