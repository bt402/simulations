import networkx as nx
import numpy as np
import matplotlib.pylab as plt

N = 10000
m = 3

ba_graph = nx.barabasi_albert_graph(N, m)

# pc = <k> / <k2><k>

Gcc = sorted(nx.connected_component_subgraphs(ba_graph), key=len, reverse=True)
G0 = Gcc[0]

print (nx.number_of_nodes(G0)) # the size of the giant component

# just use double_edge_swap for time being
# size of a giant cluster against the occupation probability pc

# P(k|k') = kP(k)/<k>
# pc = <k> / <k2> - <k>'
# where <k>' is the average degree after shuffle

def k2(graph, ba):
    k = 0
    k2 = []
    for n in range (0, N):
        if (n in graph):
            k += ba.degree(n)
            k2.append(k**2)
    return np.mean(k2)

def avg_k(graph, ba):
    k = 0
    for n in range (0, N):
        if (n in graph):
            k += ba.degree(n)
    return k/N

# phi_c = avg_k(ba_graph.nodes(), ba_graph) / (k2(ba_graph.nodes(), ba_graph) - avg_k(ba_graph.nodes(), ba_graph)) # critical thershold

giant_component = []
probability = []
for p10 in range (0, 11):
    ba_graph = nx.barabasi_albert_graph(N, m)
    nx.double_edge_swap(ba_graph)
    for n in range (0, N):
        p = p10/10 # probability a node can be occupied
        if (np.random.binomial(1, p) < 1):
            ba_graph.remove_node(n)
    if (p > 0):
        Gcc = sorted(nx.connected_component_subgraphs(ba_graph), key=len, reverse=True)
        G0 = Gcc[0]

        print("Giant component size: " + str(nx.number_of_nodes(G0)) + "(" + str(nx.number_of_nodes(G0)/N) + ") when probability=" + str(p))  # the size of the giant component
        giant_component.append(nx.number_of_nodes(G0)/N)
        probability.append(p)
       # print (avg_k(ba_graph.nodes(), ba_graph) / (k2(ba_graph.nodes(), ba_graph) - avg_k(ba_graph.nodes(), ba_graph))) # criticlal occupation probability

plt.plot(probability, giant_component)
plt.show()

