import numpy as np
import networkx as nx
import matplotlib.pylab as plt

N = 1000
n = int(0.01 * N)

m = 0.1 * N
S = N - 1
I = 1
beta = 0.3

infectedNodes = []
susceptibleNodes = []

BAgraph = nx.barabasi_albert_graph(N, n)

attrs = {'status':'S'}

for n,d in BAgraph.nodes(data=True):
    ''' Set entire population to susceptible'''
    BAgraph.nodes[n].update(attrs)

rand = np.random.randint(1,N)
# infect one random node
BAgraph.nodes[rand].update({'status': 'I'})

infectedNodes.append(rand) # keep track of infected nodes

susceptibleNodes = np.arange(0, N) # all susceptible nodes
index = np.argwhere(susceptibleNodes==rand) # get index of node to remove
susceptibleNodes = np.delete(susceptibleNodes, index) # remove the infected node

numberOfInfected = []

def are_susceptible(neighbours):
    return (any(x in susceptibleNodes for x in neighbours))


def infect():
    global susceptibleNodes
    for i in infectedNodes:
        neigbours = list(BAgraph.neighbors(i)) # get all neighbours of infected node
        if are_susceptible(neigbours): # check if neighbours are susceptible
            for s in neigbours:
                if (np.random.random() < beta):
                    BAgraph.nodes[s].update({'status': 'I'})
                    infectedNodes.append(s)
                    index = np.argwhere(susceptibleNodes == s)  # get index of node to remove
                    susceptibleNodes = np.delete(susceptibleNodes, index)  # remove the infected node

for t in range (0, 100):
    numberOfInfected.append(len(infectedNodes))
    infect()



plt.plot(infectedNodes)
plt.show()