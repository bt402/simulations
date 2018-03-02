import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

N = 5000
m = 2
epsilon = 0.001
eta = 10
gamma = 2.8

def generate_links(graph, active_nodes):
    a = np.ndarray.tolist(np.arange(0, N))  # create a list of all nodes
    indices = []
    for n in active_nodes:
        a.remove(n)  # remomve active nodes from the list, prevents self connections
    # loop through all nodes
    for an in range (0, len(active_nodes)):
        if (len(a) > 2):
            indices = random.sample(a, 2) # pick two non-repetitive random numbers, so that the node doesn't select same target twice
        for i in range(0, len(indices)):
            # add edge between node n, and two other random nodes picked
            graph.add_edge(active_nodes[an], indices[i])
    return graph

def activate_nodes(ai):
    active_nodes = []
    for n in range(0, N):
        if (np.random.random() < ai):
            # vertex becomes active and generates m link
            active_nodes.append(n)
    return active_nodes

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
ai_arr = []

def power_law(x0, x1, y, gamma):
    return ((x1**(-gamma+1) - x0**(-gamma+1))*y  + x0**(-gamma+1.0))**1.0/(-gamma + 1.0)

for t in range (0, 100):
    graph = new_graph()
    x =  power_law(epsilon, 1, random.uniform(0,1), gamma)
    ai = eta * x
    #print ("ai" + str(ai))
    # activate nodes
    active = activate_nodes(ai)
    #print (active)
    connected_graph = generate_links(graph, active)
    # calculate degree of the connected graph
    ai_arr.append(ai)
    k = (2 * connected_graph.number_of_edges()) / N # calculate the degree
    k_arr.append(k)

plt.subplot(211)
plt.plot(k_arr)
plt.xlabel(r'$\tau$')
plt.ylabel(r'$\langle k \rangle_t$')

plt.subplot(212)
plt.ylabel(r"Probability $a_i$")
plt.plot(ai_arr)

plt.show()