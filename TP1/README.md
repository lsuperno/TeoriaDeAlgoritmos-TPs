# TP1 – Problema de la Mochila

Teoría de Algoritmos (TB024) – Curso Echevarría – Grupo 7

## Requisitos

Python 3.9.6. Instalar las bibliotecas desde esta carpeta (`TP1/`):

```bash
pip install -r requirements.txt
```

| Biblioteca | Versión | Uso |
|---|---|---|
| matplotlib | 3.9.4 | Gráficos |
| numpy | 2.0.2 | Ajuste de curvas teóricas |
| pulp | 4.0.0 | Modelado y resolución de Programación Lineal |

## Ejercicio 1 – Fuerza Bruta vs. Backtracking

```bash
cd Ej1_FB_BT
```

Resolver un set:

```bash
python3 mochila_fuerza_bruta.py sets/mochila20.txt
python3 mochila_backtracking.py sets/mochila2000.txt
```

Medir tiempos y generar gráficos:

```bash
python3 medir.py
python3 graficos.py
```

Regenerar los sets (opcional, ya están en `sets/`):

```bash
python3 generar_sets.py
```

## Ejercicio 2 – Greedy

```bash
cd Ej2_Greedy
```

```bash
python3 mochila_greedy.py
```

Medir tiempos y generar gráficos:

```bash
python3 medir.py
python3 graficos.py
```
Regenerar los sets (opcional, ya están en sets/):

```bash
python3 generar_sets.py
```

_Completar._

## Ejercicio 3 – Programación Dinámica

_Completar._

## Ejercicio 4 – Programación Lineal

```bash
cd Ej4_ProgramacionLineal
```

Ejecutar una prueba individual (por defecto resuelve una instancia creada aleatoriamente de n = 10000), muestra tiempo y beneficio:

```bash
python3 mochila_programacion_lineal.py
```

Medir los tiempos sobre todos los sets de datos (`sets/`) y generar el gráfico comparativo:

```bash
python3 grafico_sets.py
```
