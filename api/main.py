from flask import Flask, request, jsonify
import networkx as nx
import socket

app = Flask(__name__)

Lista_ciudades = ["A","B","C","D","E","F"]
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

@app.route('/')
def inicio():
    return "Servidor TSP en funcionamiento"


@app.route('/calcular_distancia', methods=['POST'])
def calcular_distancia():
    data= request.get_json()
    
    if 'path' not in data:
        return jsonify({"error": "No se encuentra 'path'"}), 400

    path = data["path"]
    total = 0

    for i in range(len(path) - 1):
        origen = path[i]
        destino = path[i + 1]
        total += grafo[origen][destino]["peso"]

    print("Atendiendo desde:", socket.gethostname())
    return jsonify({"distancia_total": total})


if __name__ == '__main__':
    app.run(debug=True)