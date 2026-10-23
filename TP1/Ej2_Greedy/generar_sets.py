import os
import subprocess

os.makedirs("sets", exist_ok=True)

tamanos = [100, 500, 1000, 5000, 10000, 50000, 100000, 200000, 500000]

for n in tamanos:
    cmd = f"python3 ../crear_mochila.py {n} > sets/mochila{n}.txt"
    subprocess.run(cmd, shell=True)

print("Listos los archivos de prueba en la carpeta sets.")
