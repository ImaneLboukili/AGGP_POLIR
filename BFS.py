import random as rd
import networkx as nx

G = nx.barabasi_albert_graph(1000, 500)

def bfsLimite(G, N):
    d = {}
    for node in G.nodes:
	d[node] = []

    for edge in G.edges:
	d[edge[0]].append(edge[1])
	d[edge[1]].append(edge[0])


    def bfs(graph, start, N, path=[]):
	queue = [start]
	while (queue and len(path) < N):
	    vertex = queue.pop(0)
	    if vertex not in path:
		path.append(vertex)
		queue.extend(set(graph[vertex]) - set(path))
		
	return path

    return bfs(d, rd.randint(0, len(d)), N)

print bfsLimite(G, 200)
