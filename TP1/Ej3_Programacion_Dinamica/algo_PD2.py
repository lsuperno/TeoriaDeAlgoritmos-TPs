import os
import sys

def leer_mochila(nombre):
    with open(nombre) as arch:
        capacidad = int(arch.readline())
        elementos = []
        for linea in arch:
            peso, beneficio = linea.strip().split(",")
            elementos.append((int(peso), int(beneficio)))
        return capacidad, elementos


def mochila_min_peso(elementos, B):

    n = len(elementos)
    N = float('inf')

    matriz = [[N for _ in range(B + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        matriz[i][0] = 0

    for i in range(1, n + 1):
        peso_actual, beneficio_actual = elementos[i-1]
        
        for b in range(1, B + 1):
            if beneficio_actual > b:
                matriz[i][b] = matriz[i-1][b]
            else:
                no_incluir = matriz[i-1][b]
                incluir = peso_actual + matriz[i-1][b - beneficio_actual]
                matriz[i][b] = min(no_incluir, incluir)
    if matriz[n][B] == N:
        return None

    lista_elementos = []
    b_restante = B
    for i in range(n, 0, -1):
        if matriz[i][b_restante] != matriz[i-1][b_restante]:
            elemento_incluido = elementos[i-1]
            lista_elementos.append(elemento_incluido)
            b_restante -= elemento_incluido[1]

    return matriz[n][B], lista_elementos[::-1]

def main():
    nombre_archivo = "sets/mochila100.txt"

    B, elementos = leer_mochila(nombre_archivo)

    resultado = mochila_min_peso(elementos, B)
    if resultado is None:
        print(f"No existe una combinación con beneficio exactamente {B}")
        return
    
    peso_min, items = resultado
    print(f"Peso mínimo = {peso_min}")
    print(f"Elementos elegidos = {len(items)}")

if __name__ == "__main__":
    main()