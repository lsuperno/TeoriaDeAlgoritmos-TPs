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

_Completar._

## Ejercicio 3 – Programación Dinámica

_Completar._

## Ejercicio 4 – Programación Lineal

_Completar._
