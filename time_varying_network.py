import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

N = 10000
m = 2
epsilon = 0.001
eta = 1.
gamma = -2.1

distribution = []

'''
* Active node cannot pick the same target twice
* Active nodes can connect with themselves
* Each active node generates two links
* active nodes should not select active nodes at time t
'''

def power_law(x0, x1, gamma):
    pl = []
    for i in range (N):
        pl.append(((x1**(gamma+1) - x0**(gamma+1))*random.uniform(0,1)  + x0**(gamma+1.0))**(1.0/(gamma + 1.0)))
    return pl

distribution = power_law(epsilon, 1, gamma)

def gen_rand(m):
    return random.sample(range(0,N),m) # return m random numbers, without repetition

def connection_exists(i, chosen_nodes, graph):
    for j in chosen_nodes:
        if (graph.has_edge(i, j)):
            return True
    return False

def connect(graph, active_nodes):
    for ni in active_nodes:
        choose_random = gen_rand(m)
        while (ni in choose_random or connection_exists(ni, choose_random, graph)): # keep generating m random numbers until active node n isn't in the list, so that it doesn't connect to itself
            choose_random = gen_rand(m)
        for nj in choose_random:
            graph.add_edge(ni, nj)
    return graph

def activate_nodes():
    active_nodes = []
    for i in range(N):
        if (random.random() < distribution[i]):
            active_nodes.append(i)
    return active_nodes


def new_graph():
    graph = nx.Graph()
    graph.add_nodes_from(np.arange(0, N))
    return graph

def avg_a():
    return ((1-gamma)/(2-gamma))*((1-(epsilon**(2-gamma)))/(1-(epsilon**(1-gamma))))

k_arr = []
ai_arr = []

for t in range (0, 100):
    graph = new_graph()
    # activate nodes
    active = activate_nodes()
    connected_graph = connect(graph, active)
    # calculate degree of the connected graph
    k = 2 * connected_graph.number_of_edges() / N  # calculate the degree
    k_arr.append(k)

print (eta * np.mean(distribution) * N)

#plt.subplot(211)
plt.plot(k_arr)
plt.axhline(2 * m * eta * np.mean(distribution), color='r', linestyle='--')
plt.xlabel(r'$\tau$')
plt.ylabel(r'$\langle k \rangle_t$')

plt.show()