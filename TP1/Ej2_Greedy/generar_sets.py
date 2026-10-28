import os
import sys
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
raiz_tp = os.path.dirname(script_dir)
sys.path.append(raiz_tp)

from crear_mochila import crear_mochila

os.makedirs("sets", exist_ok=True)

tamanos = [100, 500, 1000, 5000, 10000, 50000, 100000, 200000, 500000]

os.chdir(raiz_tp)

for n in tamanos:
    print(f"Generando set para N = {n}...")
    crear_mochila(n)
    
    archivo_origen = f"mochila{n}.txt"
    archivo_destino = os.path.join(script_dir, "sets", f"mochila{n}.txt")

    shutil.move(archivo_origen, archivo_destino)

os.chdir(script_dir)

print("Listos todos los archivos de prueba en la carpeta sets.")