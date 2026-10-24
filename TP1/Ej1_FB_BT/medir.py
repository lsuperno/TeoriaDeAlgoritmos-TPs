"""
Mide los tiempos de fuerza bruta y backtracking sobre los sets de sets/
y guarda los resultados en resultados/.

Para cada set se registra: tamanio, capacidad, beneficio optimo, peso usado,
items elegidos y tiempo de ejecucion. Ademas se verifica que fuerza bruta y
backtracking obtengan el mismo beneficio en todos los sets donde corren ambos.

Uso: python3 medir.py   (antes correr generar_sets.py)
"""

import csv
import os
import time

from mochila_fuerza_bruta import leer_mochila, mochila_fuerza_bruta
from mochila_backtracking import mochila_backtracking
from generar_sets import TAMANIOS_FB, TAMANIOS_BT, TAMANIOS_PEOR_CASO

DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_SETS = os.path.join(DIR_BASE, "sets")
DIR_RES = os.path.join(DIR_BASE, "resultados")

REPETICIONES = 5
UMBRAL_REPETIR = 0.5  # segundos: si una corrida tarda mas, no se repite


def medir(algoritmo, capacidad, pesos, beneficios):
    """Ejecuta el algoritmo y devuelve (resultado, tiempo minimo).
    Las corridas rapidas se repiten y se toma el minimo para reducir ruido."""
    inicio = time.perf_counter()
    resultado = algoritmo(capacidad, pesos, beneficios)
    mejor_tiempo = time.perf_counter() - inicio
    if mejor_tiempo < UMBRAL_REPETIR:
        for _ in range(REPETICIONES - 1):
            inicio = time.perf_counter()
            algoritmo(capacidad, pesos, beneficios)
            mejor_tiempo = min(mejor_tiempo, time.perf_counter() - inicio)
    return resultado, mejor_tiempo


def correr(algoritmo, nombre_alg, archivos, salida_csv):
    filas = []
    for archivo in archivos:
        capacidad, pesos, beneficios = leer_mochila(os.path.join(DIR_SETS, archivo))
        (beneficio, items), tiempo = medir(algoritmo, capacidad, pesos, beneficios)
        peso_usado = sum(pesos[i] for i in items)
        filas.append({
            "archivo": archivo,
            "n": len(pesos),
            "capacidad": capacidad,
            "beneficio": beneficio,
            "peso_usado": peso_usado,
            "tiempo_s": f"{tiempo:.9f}",
            "items": " ".join(map(str, items)),
        })
        print(f"{nombre_alg:<4} {archivo:<20} n={len(pesos):<5} "
              f"beneficio={beneficio:<8} tiempo={tiempo:.6f} s")
    with open(os.path.join(DIR_RES, salida_csv), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        writer.writeheader()
        writer.writerows(filas)
    return filas


def verificar(filas_fb, filas_bt, salida):
    bt_por_archivo = {f["archivo"]: f for f in filas_bt}
    lineas = []
    todo_ok = True
    for f in filas_fb:
        b = bt_por_archivo[f["archivo"]]
        ok = f["beneficio"] == b["beneficio"]
        todo_ok = todo_ok and ok
        lineas.append(f"{f['archivo']}: FB={f['beneficio']} BT={b['beneficio']} "
                      f"{'OK' if ok else 'DISTINTO'}")
    with open(os.path.join(DIR_RES, salida), "w") as out:
        out.write("\n".join(lineas) + "\n")
    print(f"Verificacion FB vs BT ({salida}): {'todos coinciden' if todo_ok else 'HAY DIFERENCIAS'}")
    return todo_ok


def main():
    os.makedirs(DIR_RES, exist_ok=True)

    tipicos_fb = [f"mochila{n}.txt" for n in TAMANIOS_FB]
    tipicos_bt = [f"mochila{n}.txt" for n in TAMANIOS_FB + TAMANIOS_BT]
    peor_caso = [f"peor_caso{n}.txt" for n in TAMANIOS_PEOR_CASO]

    fb = correr(mochila_fuerza_bruta, "FB", tipicos_fb, "fb_tipicos.csv")
    bt = correr(mochila_backtracking, "BT", tipicos_bt, "bt_tipicos.csv")
    fb_pc = correr(mochila_fuerza_bruta, "FB", peor_caso, "fb_peor_caso.csv")
    bt_pc = correr(mochila_backtracking, "BT", peor_caso, "bt_peor_caso.csv")

    verificar(fb, bt, "verificacion_tipicos.txt")
    verificar(fb_pc, bt_pc, "verificacion_peor_caso.txt")


if __name__ == "__main__":
    main()
