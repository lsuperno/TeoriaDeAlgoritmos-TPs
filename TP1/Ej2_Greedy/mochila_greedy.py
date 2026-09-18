import crear_mochila

def lectura_archivo(nombre):

    with open(nombre, "r") as arch:

        capacidad = int(arch.readline().strip())
        elementos = []

        for linea in arch:
            peso, beneficio = linea.strip().split(",")
            peso = int(peso)
            beneficio = int(beneficio)

            elementos.append((peso, beneficio))

    # Ordeno segun relacion valor/peso
    elementos_ordenados = sorted(elementos, key=lambda x: x[1] / x[0], reverse=True)

    return capacidad, elementos_ordenados

