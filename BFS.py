import random as rd
import networkx as nx
import matplotlib.pyplot as plt

G = nx.barabasi_albert_graph(200, 3)

def bfs(graph, start, N, path=[]):
  queue = [start]
  while (queue and len(path) < N):
   vertex = queue.pop(0)
   if vertex not in path:
    path.append(vertex)
    queue.extend(set(graph[vertex]) - set(path))

  return path

def bfsLimite(G, N):
  return bfs(G, rd.randint(0, len(G)), N)

nn=50
nb = bfsLimite(G, nn)
sG = nx.subgraph(G, nb)



# plt.subplot(121)
#Plot graph
options = {
    'node_color': 'royalblue',
    'edge_color': 'black',
    'font_color': 'white',
    'font_weight': 'bold',
    'node_size': 400,
    'width': 2,
    }
# nx.draw(G, with_labels = True, **options)

# plt.subplot(122)

# nx.draw(sG, with_labels = True, **options)
# plt.show()

print nn, len(nb)