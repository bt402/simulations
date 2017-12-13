import numpy as np
import networkx as nx
import matplotlib.pylab as plt

N = 100
beta = 0.3
mu = 0.1

infectedNodes = []
numberOfInfected =[]

# TODO infect after time t+1 -- create a temp array for that
# TODO try to work out the thershold
# TODO store data in lists

inf = 0 # initial number of infected
rec = 0 # initial number of recovered

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

inftemp = []
rectemp = []

def infect():
    global inftemp
    inftemp = []
    for i in infectedNodes:
        neighborList = susceptibleList(list(BAgraph.neighbors(i))) # get all suceptible neighbours of infectious node
        for s in neighborList:
            # Try to infect every susceptible neigbhour
            if (np.random.random() < beta):
                BAgraph.nodes[s].update({'status': 'I'})
                inftemp.append(s)

def recover():
    global rectemp
    rectemp = []
    for i in infectedNodes:
        if (np.random.random() < mu):
            BAgraph.nodes[i].update({'status' : 'R'})
            rectemp.append(i)

''' Get number of infected individuals from the enitre graph '''
def noOfInfected():
    global inf
    inf = 0
    for n, d in BAgraph.nodes(data=True):
        if (BAgraph.nodes[n]['status'] == "I"):
            inf += 1
    return inf

def noOfRecovered():
    global rec
    rec = 0
    for n, d in BAgraph.nodes(data=True):
        if (BAgraph.nodes[n]['status'] == "R"):
            rec += 1
    return rec

# execute until everyone is recovered
while (noOfRecovered() < N - 1):
    infect()
    recover()
    numberOfInfected.append(noOfInfected())
    infectedNodes.extend(inftemp)

#for n,d in BAgraph.nodes(data=True):
#    print ("node#" + str(n) + " " + str(BAgraph.nodes[n]['status']))


# Threshold
# beta/mu = <k> / <k^2> - <k>
d = dict(nx.degree(BAgraph))
'''k = nx.average_degree_connectivity(BAgraph)
k = list(k.values())
k2 = np.array(k)**2

threshold = []

for i in range (0, len(k)):
    threshold.append((k[i] / (k2[i] - k[i])))

print (len(d))'''

# TODO use binning to work out the degree distribution of k

plt.subplot(211)
plt.xlabel("t")
plt.ylabel("I")
plt.plot(numberOfInfected)
ax = plt.subplot(212)
plt.bar(np.arange(0, len(d)), d.values())
fig = plt.gcf()
fig.canvas.set_window_title('SIR Model')
#vals = ax.get_yticks()
#ax.set_yticklabels(['{:3.2f}%'.format(x) for x in vals])
plt.show()