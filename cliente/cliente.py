import itertools
import requests

ciudades = ["A","B","C","D","E","F"]
mejor_distancia = float("inf")#maximo valor posible para comparar
mejor_ruta = None

for perm in itertools.permutations(ciudades):
    ruta = list(perm) + [perm[0]]  # cerramos ciclo A...A

    response = requests.post(
        url = "http://127.0.0.1:5000/calcular_distancia",
        json={"path": ruta}
    )

    distancia = response.json()["distancia_total"]

    if distancia < mejor_distancia:
        mejor_distancia = distancia
        mejor_ruta = ruta

print("Mejor ruta:", mejor_ruta)
print("Distancia:", mejor_distancia)