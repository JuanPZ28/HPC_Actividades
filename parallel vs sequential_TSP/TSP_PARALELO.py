import time
import networkx as nx
import matplotlib.pyplot as plt
import itertools
from multiprocessing import Process, Queue

Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F = [], [], [], [], [], []
RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F = {}, {}, {}, {}, {}, {}
Lista_ciudades = ["A","B","C","D","E","F"]
combinaciones = list(itertools.permutations(Lista_ciudades, 6))

#Grafo dirigido
grafo = nx.DiGraph()
grafo.add_nodes_from(Lista_ciudades)
#Direcciones Al
grafo.add_edge("A","B", peso=3)
grafo.add_edge("A","C", peso=4)
grafo.add_edge("A","D", peso=9)
grafo.add_edge("A","E", peso=8)
grafo.add_edge("A","F", peso=5)
#Direcciones B
grafo.add_edge("B","A", peso=3)
grafo.add_edge("B","C", peso=7)
grafo.add_edge("B","D", peso=9)
grafo.add_edge("B","E", peso=2)
grafo.add_edge("B","F", peso=3)
#Direcciones C
grafo.add_edge("C","A", peso=4)
grafo.add_edge("C","B", peso=7)
grafo.add_edge("C","D", peso=5)
grafo.add_edge("C","E", peso=10)
grafo.add_edge("C","F", peso=4)
#Direcciones D
grafo.add_edge("D","A", peso=9)
grafo.add_edge("D","B", peso=9)
grafo.add_edge("D","C", peso=5)
grafo.add_edge("D","E", peso=1)
grafo.add_edge("D","F", peso=5)
#Direcciones E
grafo.add_edge("E","A", peso=8)
grafo.add_edge("E","B", peso=2)
grafo.add_edge("E","C", peso=10)
grafo.add_edge("E","D", peso=1)
grafo.add_edge("E","F", peso=4)
#Direcciones F
grafo.add_edge("F","A", peso=5)
grafo.add_edge("F","B", peso=3)
grafo.add_edge("F","C", peso=4)
grafo.add_edge("F","D", peso=5)
grafo.add_edge("F","E", peso=4)

def filtro(Lista_ciudades,Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F):

  contador=0
  while contador <= 5:
    filtrado=[
      list(p) for p in combinaciones if p[0]==Lista_ciudades[contador]
    ]
    for p in filtrado:
        p.append(Lista_ciudades[contador])

    if Lista_ciudades[contador] == "F":
       Lista_F.extend(filtrado)

    elif Lista_ciudades[contador] == "E":
       Lista_E.extend(filtrado)

    elif Lista_ciudades[contador] == "D":
       Lista_D.extend(filtrado)

    elif Lista_ciudades[contador] == "C":
       Lista_C.extend(filtrado)

    elif Lista_ciudades[contador] == "B":
       Lista_B.extend(filtrado)

    elif Lista_ciudades[contador] == "A":
       Lista_A.extend(filtrado)

    contador+=1
  return Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F

def fuerza_bruta(grafo,Lista_ciudades,Lista_1, Lista_2, Lista_3,RECORRIDOS_1, RECORRIDOS_2, RECORRIDOS_3,result_queue,worker_id):
  valor_recorrido_total=0
  lista_acciones = [Lista_1, Lista_2, Lista_3]
  lista_recorridos = [RECORRIDOS_1, RECORRIDOS_2, RECORRIDOS_3]
  resultados_proceso=[]
  for i in range(len(lista_acciones)):
    for recorrido in lista_acciones[i]:
          valor_recorrido_total = 0
          for j in range(len(recorrido)-1):
            origen = recorrido[j]
            destino = recorrido[j + 1]
            valor_recorrido = grafo[origen][destino]['peso']
            valor_recorrido_total += valor_recorrido
            lista_recorridos[i][str(recorrido)] = valor_recorrido_total
          lista_recorridos[i] = dict(sorted(lista_recorridos[i].items(), key=lambda item: item[1]))
    resultados_proceso.append(lista_recorridos[i])

    time.sleep(1)

  result_queue.put((worker_id,resultados_proceso))
  print(f"\nWorker {worker_id} con codigo ha completado su trabajo y envió resultados")



def main(grafo,Lista_ciudades,Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F,RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F):
  # Primero ejecutar el filtro para llenar las listas
  filtro(Lista_ciudades,Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F)
  Lista_asignacion_orden=[Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F]
  Lista_asignaicon_recorridos=[RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F]
  contador_asignacion_1=0
  contador_asignacion_2=1
  contador_asignacion_3=2

  result_queue = Queue()
  todos_resultados = []
  procesos=[]
  inicio = time.perf_counter()
  for x in range(2):
    p = Process(
        target=fuerza_bruta,
        args=(
            grafo,
            Lista_ciudades[contador_asignacion_1:contador_asignacion_3],
            Lista_asignacion_orden[contador_asignacion_1],
            Lista_asignacion_orden[contador_asignacion_2],
            Lista_asignacion_orden[contador_asignacion_3],
            Lista_asignaicon_recorridos[contador_asignacion_1],
            Lista_asignaicon_recorridos[contador_asignacion_2],
            Lista_asignaicon_recorridos[contador_asignacion_3],
            result_queue,
            x
        )
    )
    procesos.append(p)
    contador_asignacion_1 += 3
    contador_asignacion_2 += 3
    contador_asignacion_3 += 3

  for p in procesos:
    p.start()
    print(f"Worker iniciado: {p.pid}")

  print("Recolectando resultados...")

  for p in range(2):
        worker_id, resultados = result_queue.get()
        print(f"Recibidos resultados del Worker {worker_id}")
        todos_resultados.extend(resultados)

  for p in procesos:
    p.join()
    print(f"Worker {p.pid} terminado")
  fin = time.perf_counter()

  print(f"Tiempo de ejecucion: {fin - inicio} segundos")
  print(f"Total de resultados recibidos: {len(todos_resultados)}")

  for i, resultado in enumerate(todos_resultados):
      print(f"---Mejores recorridos de {Lista_ciudades[i]} ---")
      mejores_recorridos = list(resultado.items())[:2]
      for j, (clave, valor) in enumerate(mejores_recorridos, 1):
          print(f"Recorrido: {clave}, costo: {valor}")
      print()

  for i, resultado in enumerate(todos_resultados):
      print(f"--- Recorridos de {Lista_ciudades[i]} ---")
      for clave, valor in resultado.items():
          print(f"Recorrido: {clave}, costo: {valor}")
      print()

  print(f"EJECUCION COMPLETADA")

  #Posicionar adecuadamente los vertices
  posiciones= nx.spring_layout(grafo, seed=10)
  #Poner pesos
  pesos= nx.get_edge_attributes(grafo,"peso")
  #Dibujar grafos
  nx.draw(grafo,posiciones,with_labels=True)
  #Dibujar pesos
  nx.draw_networkx_edge_labels(grafo,posiciones,edge_labels=pesos)
  plt.show()

if __name__ == '__main__':
    main(grafo,Lista_ciudades,Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F,RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F)