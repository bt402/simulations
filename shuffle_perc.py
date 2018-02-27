import networkx as nx
import numpy as np
import matplotlib.pylab as plt
import random
from random import randint

N = 10000
m = 3

ba_graph = nx.barabasi_albert_graph(N, m)

# pc = <k> / <k2><k>

'''
# the size of the giant component
Gcc = sorted(nx.connected_component_subgraphs(ba_graph), key=len, reverse=True)
G0 = Gcc[0]

print (nx.number_of_nodes(G0)) 
'''

# P(k|k') = kP(k)/<k>
# pc = <k> / <k2> - <k>

def k2(graph, ba):
    k = 0
    k2 = []
    for n in range (0, N):
        if (n in graph):
            k = ba.degree(n)
            k2.append(k**2)
    return np.mean(k2)

def avg_k(graph, ba):
    k = 0
    km = []
    for n in range (0, N):
        if (n in graph):
            k = ba.degree(n)
            km.append(k)
    return np.mean(km)


for shuffle in range (0, 1000): # shuffle 10^3 times
    nx.double_edge_swap(ba_graph)


'''
    (\_/)
    (^.^)
   (")_(")
'''

giant_component = []
probability = []

gc_avg = []
prob_avg = []

#for n in range(0, N):
 #   if ((randint(1, 999) / 10e8) < (phi_c)):
 #       if (n in ba_graph.nodes()):
  #          ba_graph.remove_node(n)

shuffled_graph = ba_graph


# this doesn't change
phi_c = avg_k(shuffled_graph.nodes(), shuffled_graph) / (k2(shuffled_graph.nodes(), shuffled_graph) - avg_k(shuffled_graph.nodes(), shuffled_graph)) # critical thershold
print (phi_c)
giant_component = []
probability = []
for p10 in range (0, 41):
    ba = shuffled_graph.copy()
    for n in range (0, N):
        p = p10/100 # probability a node can be occupied
        if (np.random.binomial(1, p) < 1):
            ba.remove_node(n)
    if (p > 0):
        Gcc = sorted(nx.connected_component_subgraphs(ba), key=len, reverse=True)
        G0 = Gcc[0]

        #print("Giant component size: " + str(nx.number_of_nodes(G0)) + "(" + str(nx.number_of_nodes(G0)/N) + ") when probability=" + str(p))  # the size of the giant component
        giant_component.append(nx.number_of_nodes(G0)/N)
        probability.append(p)
       # print (avg_k(ba_graph.nodes(), ba_graph) / (k2(ba_graph.nodes(), ba_graph) - avg_k(ba_graph.nodes(), ba_graph))) # criticlal occupation probability


'''
shuffle it number of times first, and then use the theoretical thershold to find the giant cluster,
the k stays the same, it's a constant, so the occupation probability doesn't change, even if p changes,
thus degree remains the same. Focus on smaller area between 0 and 0.4.

epsilon is x0, a-active node (x1), gamma is n (it stays positive) on wolfram alpha.
using different groups, lambdaA, lambdaB, lambdaC, is the different level of gullability, using undirected
graph, find the average degree over time of that. delta t is 1, m is the number of connections that a new
node will establish.
'''

plt.plot(probability, giant_component)
plt.axvline(phi_c, color="red", linestyle='--')
plt.ylabel("Size of giant cluser")
plt.xlabel(r'$\phi$')
plt.show()

