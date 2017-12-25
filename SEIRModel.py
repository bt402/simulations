import numpy as np
import networkx as nx
import matplotlib.pylab as plt

N = 10000
beta = 0.05
mu = 0.5
k = 0.4 # progression rate from exposed (latent) to infected

infectedNodes = []
numberOfInfected =[]
exposedNodes = []

inf = 0 # initial number of infected
rec = 0 # initial number of recovered
exp = 0 # initial number of exposed

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
        if (BAgraph.nodes[n]['status'] == 'E'):
            susList.append(n)
    return susList

infected_temp = []
recovered_temp = []
exposed_temp = []

def infect():
    global infected_temp
    infected_temp = []
    for i in infectedNodes:
        neighborList = susceptibleList(list(BAgraph.neighbors(i))) # get all suceptible neighbours of infectious node
        for s in neighborList:
            # Try to infect every susceptible neigbhour
            if (np.random.random() < beta):
                #BAgraph.nodes[s].update({'status': 'I'})
                infected_temp.append(s)

def recover():
    global recovered_temp
    recovered_temp = []
    for i in infectedNodes:
        if (np.random.random() < mu):
            recovered_temp.append(i)

def expose():
    global exposed_temp
    exposed_temp = []
    susceptible = []
    for i in infectedNodes:
        susceptible = BAgraph.neighbors(i)
    for s in susceptible:
        exposed_temp.append(s)

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

def noOfExposed():
    global exp
    exp = 0
    for n, d in BAgraph.nodes(data=True):
        if (BAgraph.nodes[n]['status'] == "E"):
            exp += 1
    return exp

def updateNodes(infectedNodes):
    for n in infectedNodes:
        BAgraph.nodes[n].update({'status': 'I'})

def updateRecovered(recoveredNodes):
    for n in recoveredNodes:
        BAgraph.nodes[n].update({'status': 'R'})

def updateExposed(exposedNodes):
    for n in exposedNodes:
        BAgraph.nodes[n].update({'status' : 'E'})

# execute until everyone is recovered
for t in range (0, 100):
    #print (str((noOfRecovered() / N) * 100) + "%")
    print (t)
    expose()
    infect()
    recover()
    numberOfInfected.append(noOfInfected())
    infectedNodes.extend(infected_temp)
    updateNodes(infected_temp)
    updateExposed(exposed_temp)
    updateRecovered(recovered_temp)

for n,d in BAgraph.nodes(data=True):
    print ("node#" + str(n) + " " + str(BAgraph.nodes[n]['status']))

S = N - 1
E = 0
I = 1
R = 0
beta = 0.05

threshold = []
infected = []

while (beta <= 3):

    simulations = 100
    time = 1000

    for n in range (0, simulations):
        i = []
        r = []
        for t in range (0, time):
            if I > 0:
                S = S - (beta * S * I / N)
                E = E + (beta * S * I / N) - k * E
                I = I + k * E - np.random.binomial(I, mu)
                R = R + np.random.binomial(I, mu)
                i.append(I)
                r.append(R)
        S = N - 1
        I = 1
        R = 0
    infected.append(np.mean(i))
    threshold.append(beta/mu)
    beta += 0.05
'''
x = 0

prev = 0

for t in range (0, len(threshold)):
    current = infected[t]
    if (abs(current - prev) >= 50):
        x = threshold[t]
        break
'''

np.savetxt('seir.out', numberOfInfected, delimiter=',')
np.savetxt('seirThershold.out', (threshold, infected))

plt.subplot(211)
plt.xlabel("t")
plt.ylabel("I")
plt.plot(numberOfInfected)
ax = plt.subplot(212)
plt.plot(threshold, infected, "o-")
#plt.axvline(x, color='r', linestyle='--')
plt.ylabel("I")
plt.xlabel("β/μ")
fig = plt.gcf()
fig.canvas.set_window_title('SEIR Model')
#vals = ax.get_yticks()
#ax.set_yticklabels(['{:3.2f}%'.format(x) for x in vals])
plt.show()