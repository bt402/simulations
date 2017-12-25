import numpy as np
import networkx as nx
import matplotlib.pylab as plt

N = 10000
beta = 0.3
mu = 0.1

infectedNodes = []
numberOfInfected =[]

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
                inftemp.append(s)

def recover():
    global rectemp
    rectemp = []
    for i in infectedNodes:
        if (np.random.random() < mu):
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
        if (BAgraph.nodes[n]['status'] == "S"):
            rec += 1
    return rec

def updateNodes(infectedNodes):
    for n in infectedNodes:
        BAgraph.nodes[n].update({'status': 'I'})

def updateRecovered(recoveredNodes):
    for n in recoveredNodes:
        BAgraph.nodes[n].update({'status': 'S'})


# execute until everyone is infected
for t in range (0, 100):
    infect()
    recover()
    print (str(t) + "%")
    numberOfInfected.append(noOfInfected())
    infectedNodes.extend(inftemp)
    infectedNodes = list(set(infectedNodes).difference(set(rectemp)))
    updateNodes(inftemp)
    updateRecovered(rectemp)

S = N - 1
I = 1
beta = 0.05
mu = 0.5

threshold = []
infected = []

while (beta <= 2):

    simulations = 200
    time = 100

    for n in range (0, simulations):
        i = []
        s = []
        for t in range (0, time):
            if I > 0:
                p = (I / N) * beta
                S = S - (beta * S * I / N) + np.random.binomial(I, mu)
                I = I + (beta * S * I / N) - np.random.binomial(I, mu)
                i.append(I)
        S = N - 1
        I = 1
    infected.append(np.mean(i))
    threshold.append(beta/mu)
    beta += 0.05

x = 0

prev = 0

for t in range (0, len(threshold)):
    current = infected[t]
    if (abs(current - prev) >= 50):
        x = threshold[t]
        break

plt.subplot(211)
plt.xlabel("t")
plt.ylabel("I")
plt.plot(numberOfInfected)
ax = plt.subplot(212)
plt.plot(threshold, infected, "o-")
plt.axvline(x, color='r', linestyle='--')
plt.ylabel("I")
plt.xlabel("β/μ")
fig = plt.gcf()
fig.canvas.set_window_title('SIS Model')
#vals = ax.get_yticks()
#ax.set_yticklabels(['{:3.2f}%'.format(x) for x in vals])
plt.show()