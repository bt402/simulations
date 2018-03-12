import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

N = 10000
m = 2
epsilon = 0.001
eta = 1.
gamma = -2.1

activity = []

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

activity = power_law(epsilon, 1, gamma)

def connect(graph, active_nodes):
    for i in active_nodes:
        count = 0
        while count < m:
            target = random.randint(0, N)
            if target != i and target not in graph.neighbors(i):
                graph.add_edge(i, target)
                count += 1
    return graph

def activate_nodes():
    active_nodes = []
    for i in range(N):
        if (random.random() < activity[i]):
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

print (eta * np.mean(activity) * N)

#plt.subplot(211)
plt.plot(k_arr)
plt.axhline(2 * m * eta * np.mean(activity), color='r', linestyle='--')
plt.xlabel(r'$\tau$')
plt.ylabel(r'$\langle k \rangle_t$')

plt.show()