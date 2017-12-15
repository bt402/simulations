import numpy as np
import networkx as nx
import matplotlib.pylab as plt

N = 10000
beta = 0.01

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
                temp.append(s)


''' Get number of infected individuals from the enitre graph '''
def noOfInfected():
    global inf
    inf = 0
    for n, d in BAgraph.nodes(data=True):
        if (BAgraph.nodes[n]['status'] == "I"):
            inf += 1
    return inf

def updateNodes(infectedNodes):
    for n in infectedNodes:
        BAgraph.nodes[n].update({'status': 'I'})

# execute until everyone is infected
while (noOfInfected() < N - 1):
    infect()
    numberOfInfected.append(noOfInfected())
    infectedNodes.extend(temp)
    updateNodes(temp)

S = N - 1
I = 1

threshold = []
infected = []

while (beta <= 0.5):
    simulations = 200
    time = 100

    dIdt = np.zeros((simulations, time)) # array with #simulations (20) rows and #time (100) columns

    for n in range (0, simulations):
        i = []
        for t in range (0, time):
            if I > 0:
                p = (I / N) * beta
                I = I + np.random.binomial(S, p)
                S = N - I
                #print (I)
                i.append(I)
                dIdt[n][t] = I
        #plt.plot(i)
        S = N - 1
        I = 1
    infected.append(np.mean(i))
    threshold.append(beta)
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
fig.canvas.set_window_title('SI Model')
#vals = ax.get_yticks()
#ax.set_yticklabels(['{:3.2f}%'.format(x) for x in vals])
plt.show()