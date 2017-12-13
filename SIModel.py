import numpy as np
import networkx as nx
import matplotlib.pylab as plt

N = 10000
beta = 0.3

infectedNodes = []
numberOfInfected =[]

inf = 0 # initial number of infected

BAgraph = nx.barabasi_albert_graph(N, 3)

attrs = {'status':'S'}

for n,d in BAgraph.nodes(data=True):
    ''' Set entire population to susceptible'''
    BAgraph.nodes[n].update(attrs)

rand = np.random.randint(1,N)
# infect one random node
BAgraph.nodes[rand].update({'status': 'I'})

# keep track of infected nodes
infectedNodes.append(rand)

''' Get all susceptible neigbours of a node'''
def susceptibleList(node):
    susList = []
    for n in node:
        if (BAgraph.nodes[n]['status'] == 'S'):
            susList.append(n)
    return susList

temp = []

def infect():
    global temp
    temp = []
    for i in infectedNodes:
        neighborList = susceptibleList(list(BAgraph.neighbors(i))) # get all suceptible neighbours of infectious node
        for s in neighborList:
            # Try to infect every susceptible neigbhour
            if (np.random.random() < beta):
                BAgraph.nodes[s].update({'status': 'I'})
                temp.append(s)


''' Get number of infected individuals from the enitre graph '''
def noOfInfected():
    global inf
    inf = 0
    for n, d in BAgraph.nodes(data=True):
        if (BAgraph.nodes[n]['status'] == "I"):
            inf += 1
    return inf

# execute until everyone is infected
while (noOfInfected() < N - 1):
    infect()
    numberOfInfected.append(noOfInfected())
    infectedNodes.extend(temp)

# Threshold
# beta/mu = <k> / <k^2>

'''k = nx.average_degree_connectivity(BAgraph)
k = list(k.values())
k2 = np.array(k)**2

threshold = []

for i in range (0, len(k)):
    threshold.append((k[i] / (k2[i])))'''

plt.subplot(211)
plt.xlabel("t")
plt.ylabel("I")
plt.plot(numberOfInfected)
ax = plt.subplot(212)
plt.hist([1, 2, 3, 4], 4)
fig = plt.gcf()
fig.canvas.set_window_title('SI Model')
#vals = ax.get_yticks()
#ax.set_yticklabels(['{:3.2f}%'.format(x) for x in vals])
plt.show()