import sys
import time

sys.setrecursionlimit(10000)


def leer_mochila(archivo):
    with open(archivo) as f:
        lineas = f.read().splitlines()
    capacidad = int(lineas[0])
    pesos = []
    beneficios = []
    for linea in lineas[1:]:
        if linea.strip():
            p, b = linea.split(",")
            pesos.append(int(p))
            beneficios.append(int(b))
    return capacidad, pesos, beneficios


def cota_superior(idx, peso_acum, pesos, beneficios, capacidad):
    # Maximo beneficio alcanzable desde idx si se permitieran fracciones.
    # Es una cota valida porque los items estan ordenados por beneficio/peso.
    cap_restante = capacidad - peso_acum
    cota = 0
    for i in range(idx, len(pesos)):
        if pesos[i] <= cap_restante:
            cota += beneficios[i]
            cap_restante -= pesos[i]
        else:
            cota += beneficios[i] * (cap_restante / pesos[i])
            break
    return cota


def bt(idx, peso_acum, benef_acum, seleccion, mejor, capacidad, pesos, beneficios):
    n = len(pesos)

    # Caso base: ya se decidieron todos los items
    if idx == n:
        if benef_acum > mejor[0]:
            mejor[0] = benef_acum
            mejor[1] = seleccion.copy()
        return

    # Poda por cota: esta rama no puede superar a la mejor solucion
    if benef_acum + cota_superior(idx, peso_acum, pesos, beneficios, capacidad) <= mejor[0]:
        return

    # Rama 1: incluir el item idx (poda por capacidad)
    if peso_acum + pesos[idx] <= capacidad:
        seleccion.append(idx)
        bt(idx + 1, peso_acum + pesos[idx], benef_acum + beneficios[idx],
           seleccion, mejor, capacidad, pesos, beneficios)
        seleccion.pop()

    # Rama 2: no incluir el item idx
    bt(idx + 1, peso_acum, benef_acum, seleccion, mejor, capacidad, pesos, beneficios)


def mochila_backtracking(capacidad, pesos, beneficios):
    n = len(pesos)

    # Ordenar los indices por beneficio/peso descendente
    orden = sorted(range(n), key=lambda i: beneficios[i] / pesos[i], reverse=True)
    pesos_ord = [pesos[i] for i in orden]
    beneficios_ord = [beneficios[i] for i in orden]

    mejor = [0, []]  # [mejor beneficio, mejor seleccion (indices del orden nuevo)]
    bt(0, 0, 0, [], mejor, capacidad, pesos_ord, beneficios_ord)

    # Traducir la seleccion a los indices originales
    items = sorted(orden[i] for i in mejor[1])
    return mejor[0], items


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 mochila_backtracking.py <archivo_mochila>")
        sys.exit(1)

    capacidad, pesos, beneficios = leer_mochila(sys.argv[1])

    inicio = time.perf_counter()
    beneficio, items = mochila_backtracking(capacidad, pesos, beneficios)
    tiempo = time.perf_counter() - inicio

    print(f"Capacidad: {capacidad} | Items: {len(pesos)}")
    print(f"Beneficio optimo: {beneficio}")
    print(f"Peso usado: {sum(pesos[i] for i in items)}")
    print(f"Items elegidos: {items}")
    print(f"Tiempo: {tiempo:.6f} s")


if __name__ == "__main__":
    main()
