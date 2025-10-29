#IMPORTACION DE LIBRERIAS
import time
import networkx as nx
import matplotlib.pyplot as plt
import itertools
#DECLARACION DE LISTAS Y DICCIONARIOS PARA EL ALAMACENAMIENTO DE RESULTADOS
Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F = [], [], [], [], [], []
RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F = {}, {}, {}, {}, {}, {}
Lista_ciudades = ["A","B","C","D","E","F"]
# GENERAMOS TODAS LAS PERMUTACIONE SPOSIBLES PARA LA LISTA DE CIUDADES, LO QUE PERMITE TRABAJAR CON FUERZA BRUTA EVLAUANDO TODAS LAS FORMAS POSIBLES
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
#FUNCION DE FILTRO, PARA SEGMENTAR LAS PARMUTACIONES DE ACUERDO A LA LETRA CON LA QUE INICIEN
def filtro(Lista_ciudades,Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F):

  contador=0
  while contador <= 5:
      #LISTA FILTRADO DONDE SE ALMACENAN LAS FORMAS POSIBLES DE ACUERDO A LA PRIMERA LETRA
    filtrado=[
      list(p) for p in combinaciones if p[0]==Lista_ciudades[contador]
    ]
      #AÑADIR ULTIMA LETRA COMO LA MISMA DE INICIO
    for p in filtrado:
        p.append(Lista_ciudades[contador])
    #ENCONTRAR A QUE LISTA PERTENCE EL FILTRADO
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

def fuerza_bruta(grafo,Lista_ciudades,Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F,RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F):
  valor_recorrido_total=0
  lista_acciones = [Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F]
  lista_recorridos = [RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F]
  for i in range(len(lista_acciones)):
      #ENTRAR EN CADA LISTA DE LA lista_acciones
    for recorrido in lista_acciones[i]:
          #ENTRAR A CADA VALOR DE CADA LISTA QUE ESTA DENTRO DE LA lista_acciones 
          valor_recorrido_total = 0
            #SUMA DE ARISTA POR CADA PAR DE NODOS VECINOS
          for j in range(len(recorrido)-1):
            origen = recorrido[j]
            destino = recorrido[j + 1]
             #ACCESO AL VALOR DE LA ARISTA DE LOS NODOS VECINOS
            valor_recorrido = grafo[origen][destino]['peso']
             #SE SUMAN LOS VALORES
            valor_recorrido_total += valor_recorrido
             #AÑADIR VALOR AL DICCIONARIO
            lista_recorridos[i][str(recorrido)] = valor_recorrido_total
          #ORDENAMIENTO DE LOS VALORES MAS PEQUEÑOS AL INICIO
          lista_recorridos[i] = dict(sorted(lista_recorridos[i].items(), key=lambda item: item[1]))
    time.sleep(1)
  return lista_recorridos
#MOSTRAR RESULTADOS OBTENIDOS
def mostrar_resultados(Lista_ciudades,RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F):
  recorridos = [RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F]
  for x in range(6):
    clave, valor = list(recorridos[x].items())[0] """ACCEDER AL DICCIONARIO CORREPSONDIENTE y al item 0 de este"""
    print(f"Los mejores recorridos para {Lista_ciudades[x]}-{Lista_ciudades[x]} son:")
    for i in range(2):
        clave, valor = list(recorridos[x].items())[i] """ACCEDER AL DICCIONARIO CORREPSONDIENTE y al item 0 de este"""
        print(f"Recorrido: {clave} con un costo de: {valor}")
  for y in range(6):
    print(f"Recorridos de {Lista_ciudades[y]}-{Lista_ciudades[y]}:")
    for recorrido, costo in recorridos[y].items():
        print(f"Recorrido: {recorrido} con un costo de: {costo}")

def execution(grafo,Lista_ciudades,Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F,RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F):
  #Posicionar adecuadamente los vertices
  posiciones= nx.spring_layout(grafo, seed=10)
  #Poner pesos
  pesos= nx.get_edge_attributes(grafo,"peso")
  #Dibujar grafos
  nx.draw(grafo,posiciones,with_labels=True)
  #Dibujar pesos
  nx.draw_networkx_edge_labels(grafo,posiciones,edge_labels=pesos)

  filtro(Lista_ciudades,Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F)
  #INICIALIZAR CONTADOR
  inicio = time.perf_counter()
  #Desempaquetado
  RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F = fuerza_bruta(
    grafo, Lista_ciudades, Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F,
    RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F
  )
  #DETENER CONTADOR
  fin = time.perf_counter()
  #MOSTRAR TIEMPO
  print(f"Tiempo de ejecucion: {fin - inicio} segundos")
  mostrar_resultados(Lista_ciudades,RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F)
  plt.show()

execution(grafo,Lista_ciudades,Lista_A, Lista_B, Lista_C, Lista_D, Lista_E, Lista_F,RECORRIDOS_A, RECORRIDOS_B, RECORRIDOS_C, RECORRIDOS_D, RECORRIDOS_E, RECORRIDOS_F)

