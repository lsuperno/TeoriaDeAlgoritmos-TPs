import os
import time
import pandas as pd
from mochila_greedy import mochila_greedy as resolver_mochila_greedy_modificado

os.makedirs("resultados", exist_ok=True)

tamanos = [100, 500, 1000, 5000, 10000, 50000, 100000, 200000, 500000]
resultados = []

for n in tamanos:
    filepath = f"sets/mochila{n}.txt"
    with open(filepath, 'r') as f:
        capacidad = int(f.readline())
        pesos, beneficios = [], []
        for line in f:
            if line.strip():
                p, b = map(int, line.strip().split(','))
                pesos.append(p)
                beneficios.append(b)

    elementos = list(zip(pesos, beneficios))
    reps = 50 if n <= 10000 else 5
    tiempos = []
    
    for _ in range(reps):
        t0 = time.perf_counter()
        beneficio_opt = resolver_mochila_greedy_modificado(capacidad, elementos)
        t1 = time.perf_counter()
        tiempos.append(t1 - t0)
    
    resultados.append({
        "n": n,
        "tiempo_seg": min(tiempos),
        "beneficio": beneficio_opt
    })

df = pd.DataFrame(resultados)
df.to_csv("resultados/mediciones_greedy.csv", index=False)

print("Mediciones finalizadas. Guardadas en resultados/mediciones_greedy.csv.")