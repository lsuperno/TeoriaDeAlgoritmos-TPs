from itertools import combinations
from random import randint


def crear_mochila(n: int) -> None:
    """
    Funcion de crear mochila de la catedra.
    """
    nombre = "mochila" + str(n) + ".txt"
    with open(nombre, "w") as arch:
        cap = n * 50
        arch.write(str(cap) + "\n")
        for _ in range(n):
            peso = randint(1, 200)
            benef = randint(1, 1000)
            arch.write(str(peso) + "," + str(benef) + "\n")


def leer_mochila(n: int) -> tuple[list[tuple[int, int]], int]:
    """
    Lee una mochila desde un archivo y devuelve las caracteristicas de la misma.
    - Entrada: n (int): Numero que identifica el archivo ('mochilaN.txt').
    - Salida: items (list[tuple[int, int]]): Lista de tuplas (peso, beneficio).
              capacidad (int): Capacidad maxima de la mochila.
    """
    nombre = "mochila" + str(n) + ".txt"
    items: list[tuple[int, int]] = []

    with open(nombre, "r") as arch:
        capacidad = int(arch.readline().strip())
        for linea in arch:
            peso, benef = linea.strip().split(",")
            items.append((int(peso), int(benef)))

    return items, capacidad


def completar_con_greedy(
    items: list[tuple[int, int]], capacidad: int, items_fijos: tuple[int, ...]
) -> tuple[int, set[int]]:
    """
    Completa la mochila de forma greedy a partir de un conjunto de items ya fijados.
    Asume que los items estan ordenados de mayor a menor por beneficio/peso.
    - Entrada: items (list[tuple[int, int]]): Lista de tuplas (peso, beneficio).
               capacidad (int): Capacidad maxima de la mochila.
               items_fijos (tuple[int, ...]): Indices de los items fijados.
    - Salida: beneficio_greedy (int): Beneficio sumado por el greedy.
              items_greedy (set[int]): Indices de los items agregados por el greedy.
    """
    # Restamos el peso de los items fijos (posicion 0 de cada tupla) a la capacidad total
    peso_fijos = sum(items[i][0] for i in items_fijos)
    capacidad_libre = capacidad - peso_fijos

    beneficio_greedy = 0
    items_greedy: set[int] = set()

    # Recorremos los items ordenados y agregamos los que entren en el espacio libre
    for i, (peso, beneficio) in enumerate(items):
        if i not in items_fijos and peso <= capacidad_libre:
            beneficio_greedy += beneficio
            capacidad_libre -= peso
            items_greedy.add(i)

    return beneficio_greedy, items_greedy


def sahni(items: list[tuple[int, int]], capacidad: int, k: int) -> tuple[int, set[int]]:
    """
    Resuelve el problema de la mochila de forma aproximada mediante el algoritmo de Sahni.
    - Entrada: items (list[tuple[int, int]]): Lista de tuplas (peso, beneficio).
               capacidad (int): Capacidad maxima de la mochila.
               k (int): Cantidad maxima de elementos a fijar por combinacion.
    - Salida: mejor_beneficio (int): Mejor beneficio aproximado encontrado.
              mejores_items (set[int]): Indices (en la lista ordenada) de los items elegidos.
    """
    # Ordenamos las tuplas (peso, beneficio) de mayor a menor segun beneficio / peso
    items_ordenados = sorted(items, key=lambda item: item[1] / item[0], reverse=True)

    cantidad_items = len(items_ordenados)
    mejor_beneficio = 0
    mejores_items: set[int] = set()

    # Probamos fijar combinaciones de 0, 1, ..., hasta k elementos
    for cant_fijos in range(k + 1):
        for items_fijos in combinations(range(cantidad_items), cant_fijos):
            peso_fijos = sum(items_ordenados[i][0] for i in items_fijos)

            # Solo evaluamos la combinacion si los items fijados entran en la mochila
            if peso_fijos <= capacidad:
                beneficio_greedy, items_greedy = completar_con_greedy(
                    items_ordenados, capacidad, items_fijos
                )

                beneficio_fijos = sum(items_ordenados[i][1] for i in items_fijos)
                beneficio_total = beneficio_fijos + beneficio_greedy

                # Si esta combinacion supera el mejor beneficio guardado, actualizamos el record
                if beneficio_total > mejor_beneficio:
                    mejor_beneficio = beneficio_total
                    mejores_items = items_greedy.union(items_fijos)

    return mejor_beneficio, mejores_items


if __name__ == "__main__":
    n = int(input("Ingrese la cantidad de elementos (n): "))
    k = 1
    crear_mochila(n)
    items, capacidad = leer_mochila(n)
    beneficio, elegidos = sahni(items, capacidad, k)
    print(
        f"Sahni (k={k}) -> Beneficio: {beneficio}, Cantidad de items: {len(elegidos)}, elegidos(ordenados): {elegidos}"
    )
