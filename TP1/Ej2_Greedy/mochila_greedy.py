import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crear_mochila import crear_mochila

def lectura_archivo(nombre):

    with open(nombre, "r") as arch:

        capacidad = int(arch.readline().strip())
        elementos = []

        for linea in arch:
            peso, beneficio = linea.strip().split(",")
            peso = int(peso)
            beneficio = int(beneficio)

            elementos.append((peso, beneficio))

    # Ordeno segun relacion valor/peso
    elementos_ordenados = sorted(elementos, key=lambda x: x[1] / x[0], reverse=True)

    return capacidad, elementos_ordenados

def mochila_greedy(capacidad, elementos):

    peso_actual = 0
    beneficio_total = 0

    for peso, beneficio in elementos:
        if peso_actual + peso <= capacidad:
            peso_actual += peso
            beneficio_total += beneficio

    mejor_elemento = 0

    # Garantida de calidad 1/2

    for peso, beneficio in elementos:
        if peso <= capacidad:
            if beneficio > mejor_elemento:
                mejor_elemento = beneficio

    return max(beneficio_total, mejor_elemento)

def main():

    nombre_archivo = "mochila1000.txt"

    capacidad, elementos = lectura_archivo(nombre_archivo)
    beneficio_maximo = mochila_greedy(capacidad, elementos)

    print(f"Capacidad de la mochila: {capacidad}")
    print(f"Beneficio máximo obtenido: {beneficio_maximo}")


main()