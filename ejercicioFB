def mochila_fuerza_bruta(capacidad, pesos, beneficios):
    n=len(pesos)
    mejor_beneficio=0
    for mascara in range(2**n):
        peso_total = 0
        beneficio_total = 0
        for i in range (n):
            if mascara & (1 << i):
                peso_total += pesos[i]
                beneficio_total += beneficios[i]
        if peso_total <= capacidad and beneficio_total > mejor_beneficio:
            mejor_beneficio = beneficio_total
            mejor_mascara = mascara
    return mejor_beneficio, mejor_mascara;
