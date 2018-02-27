import networkx as nx
import  numpy as np
import random
import matplotlib.pyplot as plt

N = 5000
m = 2
eta = 1
gamma = 2.8
epsilon = 0.001

def generate_links(n):
    for l in range(0, m):
        graph.add_edge(n, random.randint(0, N))

def activate_nodes(ai):
    for n in range (0, N):
        if (np.random.random() < ai):
            # vertex becomes active and generates m link
            generate_links(n)

def new_graph():
    graph = nx.Graph()
    graph.add_nodes_from(np.arange(0, N))
    return graph

def avg_k(graph):
    km = []
    for n in range (0, N):
        km.append(graph.degree(n))
    return np.mean(km)

k_arr = []

for t in range (0, 100):
    graph = new_graph()
    x = random.uniform(epsilon,1)
    ai = eta * x
    activate_nodes(ai)
    k = 2 * m * eta * avg_k(graph)
    k_arr.append(k)

plt.plot(k_arr)
plt.xlabel(r'$\tau$')
plt.ylabel(r'$\langle k \rangle_t$')

plt.show()
