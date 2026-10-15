import sys
import time


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


def mochila_fuerza_bruta(capacidad, pesos, beneficios):
    n = len(pesos)
    mejor_beneficio = 0
    mejor_mascara = 0  # mochila vacia: siempre es una solucion valida

    # Cada mascara de 0 a 2^n - 1 representa un subconjunto de items
    for mascara in range(2 ** n):
        peso_total = 0
        beneficio_total = 0
        for i in range(n):
            if mascara & (1 << i):  # el bit i esta prendido: el item i va en la mochila
                peso_total += pesos[i]
                beneficio_total += beneficios[i]
        if peso_total <= capacidad and beneficio_total > mejor_beneficio:
            mejor_beneficio = beneficio_total
            mejor_mascara = mascara

    # Traducir la mascara a la lista de items elegidos
    items = [i for i in range(n) if mejor_mascara & (1 << i)]
    return mejor_beneficio, items


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 mochila_fuerza_bruta.py <archivo_mochila>")
        sys.exit(1)

    capacidad, pesos, beneficios = leer_mochila(sys.argv[1])

    inicio = time.perf_counter()
    beneficio, items = mochila_fuerza_bruta(capacidad, pesos, beneficios)
    tiempo = time.perf_counter() - inicio

    print(f"Capacidad: {capacidad} | Items: {len(pesos)}")
    print(f"Beneficio optimo: {beneficio}")
    print(f"Peso usado: {sum(pesos[i] for i in items)}")
    print(f"Items elegidos: {items}")
    print(f"Tiempo: {tiempo:.6f} s")


if __name__ == "__main__":
    main()
