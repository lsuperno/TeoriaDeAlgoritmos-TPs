"""
Conclusion del TP1: compara los 6 algoritmos sobre los MISMOS sets de datos.

Usa los sets de TP1/Ej1_FB_BT/sets (generados con crear_mochila.py y semilla fija)
y las implementaciones de cada ejercicio, sin modificarlas.
Cada algoritmo se ejecuta solo hasta el tamanio en que su tiempo o su memoria
siguen siendo razonables (ver LIMITES).

Uso (desde TP1/Comparacion):  python3 comparar.py
Salida: resultados/comparacion.csv y graficos/comparacion.png
"""

import ast
import csv
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_TP1 = os.path.dirname(DIR_BASE)
DIR_SETS = os.path.join(DIR_TP1, "Ej1_FB_BT", "sets")
DIR_RES = os.path.join(DIR_BASE, "resultados")
DIR_GRAF = os.path.join(DIR_BASE, "graficos")

TAMANIOS = [10, 14, 18, 22, 50, 100, 200, 300, 500, 1000, 2000]

# Tamanio maximo con el que se ejecuta cada algoritmo
LIMITES = {
    "Fuerza bruta": 22,           # exponencial: n=22 ya tarda varios segundos
    "Backtracking": 2000,
    "Greedy": 2000,
    "PD tradicional": 500,        # tabla de n*W = 50*n^2 celdas
    "PD alternativa": 200,        # tabla de n*B celdas, con B ~ 400*n
    "Programacion lineal": 2000,
}

REPETICIONES = 5
UMBRAL_REPETIR = 0.5


def cargar_funciones(ruta):
    """Carga solo las funciones (y los import) de un archivo, sin ejecutar su main."""
    with open(ruta, encoding="utf-8") as f:
        arbol = ast.parse(f.read())
    nodos = []
    for nodo in arbol.body:
        if isinstance(nodo, ast.FunctionDef):
            nodos.append(nodo)
        elif isinstance(nodo, (ast.Import, ast.ImportFrom)):
            texto = ast.dump(nodo)
            # Se omiten los import que generan archivos o que importan otros modulos del TP
            if ("crear_mochila" not in texto and "algo_PD" not in texto
                    and "mochila_programacion" not in texto):
                nodos.append(nodo)
    modulo = ast.Module(body=nodos, type_ignores=[])
    espacio = {}
    exec(compile(modulo, ruta, "exec"), espacio)
    return espacio


sys.path.insert(0, os.path.join(DIR_TP1, "Ej1_FB_BT"))
from mochila_fuerza_bruta import leer_mochila, mochila_fuerza_bruta  # noqa: E402
from mochila_backtracking import mochila_backtracking  # noqa: E402

greedy = cargar_funciones(os.path.join(DIR_TP1, "Ej2_Greedy", "mochila_greedy.py"))
def archivo_ej3(*nombres):
    """Devuelve el primer archivo existente (el Ej. 3 usa nombres distintos segun la version)."""
    for nombre in nombres:
        ruta = os.path.join(DIR_TP1, "Ej3_Programacion_Dinamica", nombre)
        if os.path.exists(ruta):
            return ruta
    raise FileNotFoundError(f"No se encontro ninguno de {nombres} en Ej3_Programacion_Dinamica")


pd1 = cargar_funciones(archivo_ej3("algo_PD1.py", "mochila_programacion_dinamica1.py"))
pd2 = cargar_funciones(archivo_ej3("algo_PD2.py", "mochila_programacion_dinamica2.py"))
try:
    pl = cargar_funciones(os.path.join(DIR_TP1, "Ej4_ProgramacionLineal",
                                       "mochila_programacion_lineal.py"))
except ImportError:
    pl = None


# Adaptadores: cada algoritmo recibe (capacidad, pesos, beneficios) y devuelve un numero
def a_fb(cap, p, b):
    return mochila_fuerza_bruta(cap, p, b)[0]


def a_bt(cap, p, b):
    return mochila_backtracking(cap, p, b)[0]


def a_greedy(cap, p, b):
    # Incluye el ordenamiento por beneficio/peso, que en Ej2 se hace al leer el archivo
    elementos = sorted(zip(p, b), key=lambda x: x[1] / x[0], reverse=True)
    return greedy["mochila_greedy"](cap, elementos)


def a_pd1(cap, p, b):
    return pd1["mochila_max_beneficio"](list(zip(p, b)), cap)[0]


def a_pd2(cap, p, b, B):
    # Devuelve el peso minimo para alcanzar el beneficio B (el optimo)
    return pd2["mochila_min_peso"](list(zip(p, b)), B)[0]


def a_pl(cap, p, b):
    return round(pl["mochila_pulp"](list(zip(p, b)), cap))


def medir(funcion, *args):
    inicio = time.perf_counter()
    resultado = funcion(*args)
    mejor = time.perf_counter() - inicio
    if mejor < UMBRAL_REPETIR:
        for _ in range(REPETICIONES - 1):
            inicio = time.perf_counter()
            funcion(*args)
            mejor = min(mejor, time.perf_counter() - inicio)
    return resultado, mejor


def main():
    if pl is None:
        sys.exit("ERROR: falta la biblioteca PuLP. Instalala con: pip install pulp")
    import pulp
    if not pulp.COIN_CMD(msg=False).available():
        sys.exit("ERROR: el Ej. 4 usa el solver cbc y no esta instalado. "
                 "En Mac: brew install cbc")
    os.makedirs(DIR_RES, exist_ok=True)
    os.makedirs(DIR_GRAF, exist_ok=True)

    algoritmos = [
        ("Fuerza bruta", a_fb),
        ("Backtracking", a_bt),
        ("Greedy", a_greedy),
        ("PD tradicional", a_pd1),
        ("PD alternativa", a_pd2),
        ("Programacion lineal", a_pl if pl else None),
    ]

    filas = []
    for n in TAMANIOS:
        cap, p, b = leer_mochila(os.path.join(DIR_SETS, f"mochila{n}.txt"))
        optimo, _ = mochila_backtracking(cap, p, b)  # referencia (verificado contra FB en Ej1)
        for nombre, funcion in algoritmos:
            if funcion is None or n > LIMITES[nombre]:
                continue
            args = (cap, p, b, optimo) if nombre == "PD alternativa" else (cap, p, b)
            try:
                resultado, t = medir(funcion, *args)
            except Exception as e:  # p. ej., falta el solver de PuLP
                print(f"{nombre:<20} n={n:<5} ERROR: {e}")
                continue
            if nombre == "PD alternativa":
                detalle = f"peso minimo={resultado}"
                calidad = 1.0
            else:
                detalle = f"beneficio={resultado}"
                calidad = resultado / optimo
            filas.append({"algoritmo": nombre, "n": n, "tiempo_s": f"{t:.9f}",
                          "resultado": resultado, "optimo": optimo,
                          "calidad": f"{calidad:.6f}",
                          "es_optimo": "si" if calidad == 1.0 else "no"})
            print(f"{nombre:<20} n={n:<5} t={t:.6f} s  {detalle}  "
                  f"(optimo={optimo}, calidad={calidad:.6f})")

    with open(os.path.join(DIR_RES, "comparacion.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    # Grafico comparativo (escala log-log)
    colores = {"Fuerza bruta": "#2a78d6", "Backtracking": "#eb6834", "Greedy": "#1baf7a",
               "PD tradicional": "#eda100", "PD alternativa": "#e87ba4",
               "Programacion lineal": "#6b6a63"}
    marcadores = {"Fuerza bruta": "o", "Backtracking": "s", "Greedy": "^",
                  "PD tradicional": "D", "PD alternativa": "v", "Programacion lineal": "P"}
    fig, ax = plt.subplots(figsize=(9, 5.4))
    for nombre, _ in algoritmos:
        datos = [(int(r["n"]), float(r["tiempo_s"])) for r in filas if r["algoritmo"] == nombre]
        if datos:
            xs, ys = zip(*datos)
            ax.plot(xs, ys, marker=marcadores[nombre], color=colores[nombre],
                    linewidth=2, markersize=6, label=nombre)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("n (cantidad de ítems)")
    ax.set_ylabel("Tiempo (segundos)")
    ax.set_title("Comparación de los 6 algoritmos sobre los mismos sets (escala log-log)")
    ax.grid(True, which="major", color="#d9d8d2", linewidth=0.6)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_GRAF, "comparacion.png"), dpi=150)
    print("Generados resultados/comparacion.csv y graficos/comparacion.png")


if __name__ == "__main__":
    main()
