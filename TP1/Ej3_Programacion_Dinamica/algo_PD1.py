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

def mochila_max_beneficio(elementos, W):

    n = len(elementos)

    matriz = [[0 for _ in range(n + 1)] for _ in range(W + 1)]

    for i in range(1, n + 1):
        peso_actual, beneficio_actual = elementos[i-1]
        
        for w in range(W + 1):
            if peso_actual > w:
                matriz[w][i] = matriz[w][i-1]
            else:
                no_incluir = matriz[w][i-1]
                incluir = beneficio_actual + matriz[w - peso_actual][i-1]
                matriz[w][i] = max(no_incluir, incluir)

    lista_elementos = []
    w_restante = W
    for i in range(n, 0, -1):
        if matriz[w_restante][i] != matriz[w_restante][i-1]:
            elemento_incluido = elementos[i-1]
            lista_elementos.append(elemento_incluido)
            w_restante -= elemento_incluido[0]

    return matriz[W][n], lista_elementos[::-1]

def main():
    nombre_archivo = "sets/mochila100.txt"

    W, elementos = leer_mochila(nombre_archivo)
    beneficio, items = mochila_max_beneficio(elementos, W)
    print(f"Beneficio máximo = {beneficio}")
    print(f"Elementos elegidos = {(items)}")

if __name__ == "__main__":
    main()