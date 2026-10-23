import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

os.makedirs("graficos", exist_ok=True)

df = pd.read_csv("resultados/mediciones_greedy.csv")
tamanos_n = df["n"].values
tiempos_medidos = df["tiempo_seg"].values

n_log_n = tamanos_n * np.log2(tamanos_n)
c = np.mean(tiempos_medidos[4:] / n_log_n[4:])

n_continuo = np.logspace(np.log10(min(tamanos_n)), np.log10(max(tamanos_n)), 500)
tiempos_teoricos_suave = c * n_continuo * np.log2(n_continuo)

plt.figure(figsize=(9, 5))
plt.plot(tamanos_n, tiempos_medidos, marker='o', color='blue', linestyle='-', linewidth=1.8, label='Greedy Medido')
plt.plot(n_continuo, tiempos_teoricos_suave, color='red', linestyle='--', linewidth=2, label='Teórico c·N·log(N)')

plt.xscale('log')
plt.title("Tiempo de Ejecución - Greedy Modificado (Escala Semilog-X)", fontsize=13, pad=10)
plt.xlabel("Cantidad de elementos (N) - Escala Logarítmica", fontsize=11)
plt.ylabel("Tiempo de ejecución (segundos)", fontsize=11)
plt.grid(True, which="major", linestyle='--', alpha=0.5)
plt.legend(fontsize=10, loc='upper left')

plt.savefig("graficos/grafico_greedy_limpio.png", dpi=300, bbox_inches='tight')

print("Imagen generada con éxito en graficos/grafico_greedy_limpio.png.")
