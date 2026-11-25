import math
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crear_mochila import crear_mochila


def lectura_archivo(nombre):

    with open(nombre, "r") as arch:

        capacidad = int(arch.readline().strip())
        elementos = []

        for linea in arch:
            linea_limpia = linea.strip()
            if linea_limpia != "":
                peso, beneficio = linea_limpia.split(",")
                peso = int(peso)
                beneficio = int(beneficio)
                elementos.append((peso, beneficio))

    return capacidad, elementos


def mochila_aproximada(capacidad, elementos, epsilon):

    # Epsilon debe ser positivo, si no b no esta bien definido
    if epsilon <= 0:
        raise ValueError("epsilon debe ser mayor que 0")

    # Nos quedamos solo con los elementos que entran en la mochila
    elementos_validos = []
    for peso, beneficio in elementos:
        if peso <= capacidad and beneficio > 0:
            elementos_validos.append((peso, beneficio))

    n = len(elementos_validos)
    if n == 0:
        return 0, []

    # Calculamos b = (epsilon / 2n) * max(v_i) y reescalamos hacia arriba
    max_beneficio = max(beneficio for _, beneficio in elementos_validos)
    b = (epsilon / (2 * n)) * max_beneficio

    beneficios_escalados = []
    for _, beneficio in elementos_validos:
        if b <= 1:
            beneficios_escalados.append(beneficio)
        else:
            beneficios_escalados.append(math.ceil(beneficio / b))

    suma_beneficios = sum(beneficios_escalados)

    # Matriz OPT[i][V]: menor peso para alcanzar el beneficio escalado V usando i items
    infinito = float("inf")
    opt = []
    for _ in range(n + 1):
        fila = [infinito] * (suma_beneficios + 1)
        fila[0] = 0
        opt.append(fila)

    for i in range(1, n + 1):
        peso, _ = elementos_validos[i - 1]
        v_esc = beneficios_escalados[i - 1]

        for v in range(suma_beneficios + 1):
            opt[i][v] = opt[i - 1][v]

            if v >= v_esc:
                peso_con_item = opt[i - 1][v - v_esc] + peso
                if peso_con_item < opt[i][v]:
                    opt[i][v] = peso_con_item

    # Buscamos el mayor beneficio escalado que no supere la capacidad
    mejor_v = 0
    v = suma_beneficios
    encontrado = False

    while v >= 0 and not encontrado:
        if opt[n][v] <= capacidad:
            mejor_v = v
            encontrado = True
        else:
            v -= 1

    # Reconstruimos los items agregados y sumamos sus beneficios reales
    beneficio_total = 0
    items_agregados = []
    v_actual = mejor_v

    for i in range(n, 0, -1):
        if opt[i][v_actual] != opt[i - 1][v_actual]:
            peso, beneficio_real = elementos_validos[i - 1]
            beneficio_total += beneficio_real
            items_agregados.append((peso, beneficio_real))
            v_actual -= beneficios_escalados[i - 1]

    items_agregados.reverse()
    return beneficio_total, items_agregados


def ejecutar(n, epsilon):
    """Corre el algoritmo sobre la instancia de tamaño n y mide el tiempo.

    Devuelve (capacidad, beneficio, items, tiempo_en_segundos).
    Mas que nada para los tests y el grafico
    """
    nombre_archivo = f"mochila{n}.txt"

    if not os.path.exists(nombre_archivo):
        crear_mochila(n)

    capacidad, elementos = lectura_archivo(nombre_archivo)

    inicio = time.perf_counter()
    beneficio, items = mochila_aproximada(capacidad, elementos, epsilon)
    tiempo = time.perf_counter() - inicio

    return capacidad, beneficio, items, tiempo


def main():

    # Uso: python mochila_aproximada.py [n] [epsilon]
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    epsilon = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25

    capacidad, beneficio_maximo, items_agregados, tiempo = ejecutar(n, epsilon)

    print(f"Capacidad de la mochila: {capacidad}")
    print(f"Epsilon: {epsilon}")
    print(f"Beneficio máximo obtenido: {beneficio_maximo}")
    print(f"Items agregados ({len(items_agregados)}): {items_agregados}")
    print(f"Tiempo de ejecución: {tiempo:.4f} s")


if __name__ == "__main__":
    main()