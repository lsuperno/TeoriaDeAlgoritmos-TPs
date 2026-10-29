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
| pandas | 2.2.3 | Lectura y procesamiento de resultados |
| pulp | 3.3.1 | Modelado y resolución de Programación Lineal |

El Ejercicio 4 y la comparación final usan además el solver **CBC**, que no se instala con pip:

```bash
brew install cbc        # macOS
sudo apt install coinor-cbc   # Linux (Debian/Ubuntu)
```

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

Resolver una instancia:

```bash
python3 mochila_greedy.py
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

## Ejercicio 3 – Programación Dinámica

```bash
cd Ej3_Programacion_Dinamica
```

# Resolver un set de datos (si no se indica nada, usa `sets/mochila120.txt` por default):
Ejecucion del algoritmo tradicional:
```bash
python3 mochila_programacion_dinamica1.py sets/mochila20.txt        
```
Ejecucion del algoritmo alternativo con B como resultado del algoritmo tradicional:
```bash
python3 mochila_programacion_dinamica2.py sets/mochila20.txt        
```
Ejecucion del algoritmo alternativo con un B ingresado por consola:
```bash
python3 mochila_programacion_dinamica2.py sets/mochila20.txt 3000   
```

Medir tiempos y generar gráficos (guarda `resultados/resultados_pd.csv` y los gráficos en `graficos/`:

```bash
python3 graficos_pd.py
```

Regenerar los sets (ya están en `sets/`; usa semilla fija y produce los mismos archivos):

```bash
python3 generar_sets.py
```

## Ejercicio 4 – Programación Lineal

```bash
cd Ej4_ProgramacionLineal
```

Ejecutar una prueba individual (por defecto resuelve una instancia creada aleatoriamente de n = 10000); muestra tiempo y beneficio:

```bash
python3 mochila_programacion_lineal.py
```

Medir los tiempos sobre todos los sets de datos (`sets/`) y generar el gráfico comparativo:

```bash
python3 grafico_sets.py
```

## Comparación de los 6 algoritmos (Conclusión)

```bash
cd Comparacion
python3 comparar.py
```

Ejecuta los seis algoritmos sobre los mismos sets (los de `Ej1_FB_BT/sets/`) y guarda la tabla de tiempos en `resultados/comparacion.csv` y el gráfico en `graficos/comparacion.png`. Tarda unos 2 minutos.
