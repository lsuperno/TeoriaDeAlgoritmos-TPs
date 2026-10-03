import sys
sys.setrecursionlimit(100000)

def cota_superior(idx, peso_acum, beneficios, pesos, capacidad):
    cap_restante = capacidad - peso_acum
    cota = 0
    for i in range(idx, len(pesos)):
        if pesos[i] <= cap_restante:
            cota += beneficios[i]
            cap_restante -= pesos[i]
        else:
            cota += beneficios[i] * (cap_restante / pesos[i])
            break
    return cota

def bt(idx, peso_acum, benef_acum, mejor, capacidad, pesos, beneficios):
    n = len(pesos)
    if idx == n:
        if benef_acum > mejor[0]:
            mejor[0] = benef_acum
        return
    if benef_acum + cota_superior(idx, peso_acum, beneficios, pesos, capacidad) <= mejor[0]:
        return
    if peso_acum + pesos[idx] <= capacidad:
        bt(idx+1, peso_acum+pesos[idx], benef_acum+beneficios[idx], mejor, capacidad, pesos, beneficios)
    bt(idx+1, peso_acum, benef_acum, mejor, capacidad, pesos, beneficios)

def mochila_backtracking(capacidad, pesos, beneficios):
    mejor = [0]
    bt(0, 0, 0, mejor, capacidad, pesos, beneficios)
    return mejor[0]
