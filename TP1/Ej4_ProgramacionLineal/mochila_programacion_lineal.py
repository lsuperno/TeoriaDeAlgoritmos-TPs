import pulp
from random import randint
import time

"""
Instrucciones de ejecución:
1 Asegurarse de tener instalada la biblioteca pulp
2 Ejecutar: python3 mochila_programacion_lineal.py

Nota: El script creara un archivo.txt con los datos aleatorios de los items
"""


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


def leer_mochila(n: int) -> list[tuple[int, int]]:
    """
    Lee una mochila desde un archivo y devuelve las caracteristicas de la misma
    -Entrada: n (int): Número que identifica el archivo ('mochilaN.txt').
    -Salida: items (list[tuple[int, int]]): Lista de tuplas (peso, beneficio).
             capacidad (int): Capacidad máxima de la mochila.
    """
    nombre = "mochila" + str(n) + ".txt"
    items = []

    with open(nombre, "r") as arch:
        capacidad = int(arch.readline().strip())
        for linea in arch:
            peso, benef = linea.strip().split(",")
            items.append((int(peso), int(benef)))

    return items, capacidad


def mochila_pulp(items: list[tuple[int, int]], capacidad: int) -> float:
    """
    Resuelve el problema de la mochila usando programación lineal y Pulp
    Para cada ítem se crea una variable binaria x[i] (0 o 1) que indica si el
    ítem se incluye en la mochila. Se maximiza la suma de beneficios sin que
    la suma de pesos supere la capacidad total de la mochila
    -Entrada: items (list[tuple[int, int]]): Lista de tuplas (peso, beneficio).
              capacidad (int): Capacidad máxima de la mochila.
    -Salida: float: Valor del beneficio total.
    """
    n = len(items)

    problema = pulp.LpProblem("Mochila", pulp.LpMaximize)

    x = []
    beneficio = []
    peso = []

    for i in range(n):
        nueva_variable = problema.add_variable(f"item{i}", 0, 1, pulp.LpBinary)
        x.append(nueva_variable)

        beneficio_item = items[i][1]
        beneficio.append(beneficio_item * nueva_variable)

        peso_item = items[i][0]
        peso.append(peso_item * nueva_variable)

    problema += pulp.lpSum(beneficio), "Beneficio"
    problema += pulp.lpSum(peso) <= capacidad, "Capacidad"

    problema.solve(pulp.COIN_CMD(msg=False))
    return pulp.value(problema.objective)


def main():
    """
    Medición de tiempos del problema de la mochila hasta 40000 elementos
    """
    tamanos = [10, 50, 100, 500, 1000, 2500, 5000, 10000, 20000, 30000, 40000]
    tiempos_medidos = []

    print("Iniciando medición de tiempos...")

    for n in tamanos:
        # 1. Preparar los datos
        crear_mochila(n)
        elementos, capacidad = leer_mochila(n)

        # 2. Medir tiempo exclusivamente del solver
        inicio = time.time()
        mochila_pulp(elementos, capacidad)
        fin = time.time()

        tiempo_ejecucion = fin - inicio
        tiempos_medidos.append(tiempo_ejecucion)
        print(tiempos_medidos)


if __name__ == "__main__":
    main()
