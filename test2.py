import networkx as nx
import matplotlib.pylab as plt
import numpy as np
from numpy.random import choice
from matplotlib.animation import FuncAnimation

# Build plot
fig, ax = plt.subplots(figsize=(7,6))

def isInfected(n):
    if (BAgraph.nodes[n]['status'] == 'S'):
        return False
    else:
        return True

def susceptibleList(nodes):
    susList = []
    for n in nodes:
        if (BAgraph.nodes[n]['status'] == 'S'):
            susList.append(n)
    return susList

N = 100
S = N - 1
I = 1
beta = 0.3

BAgraph = nx.barabasi_albert_graph(N, 3)
colors = []

attrs = {'status':'S'}

''' Create the initial graph'''
for n,d in BAgraph.nodes(data=True):
    #BAgraph[n] = 0
    l = list(BAgraph.neighbors(n))

    ''' Set entire population to susceptible'''
    BAgraph.nodes[n].update(attrs)

    if (isInfected(n)):
        colors.append("darkred")
    else:
        colors.append("green")

rand = np.random.randint(1,N)
# infect one random node
BAgraph.nodes[rand].update({'status': 'I'})
colors[rand] = "darkred"

neighborList = list(BAgraph.neighbors(rand)) # get neighbors of the infected node


#nx.draw(BAgraph, node_color = colors, with_labels=True)

pos = nx.spring_layout(BAgraph)
labels = {}
for node in BAgraph.nodes():
        labels[node] = node


nx.draw_networkx_edges(BAgraph, pos=pos, ax=ax, edge_color="black")
nx.draw_networkx_nodes(BAgraph, pos=pos, node_color=colors)
nx.draw_networkx_labels(BAgraph, pos=pos, labels=labels, font_color="white", ax=ax)
ax.legend(labels=["{}".format(0)])

''' THIS IS WHERE I HAVE TO FIGURE OUT WHAT TODO'''

#print (len(neighborList))

length = len(neighborList)

probArray = np.full(length, (1/length))

draw = None

infectedNodes = []

infectedNodes.append(rand) # add first random infected node

def infect(draw):
    for toInfect in range(0, len(draw)):
        BAgraph.nodes[draw[toInfect]].update({'status': 'I'})

        colors[draw[toInfect]] = 'darkred'

        # add new infected nodes
        infectedNodes.append(draw[toInfect])

 # TODO (1) Get the neibours of infected nodes, and infect them
# TODO (2) animate the graph

oldI = I

def update(i):
    global S, I, N, oldI
    if (i > 1):
        ax.clear()
        p = (I / N) * beta
        I = I + np.random.binomial(S, p)
        S = N - I
        diff = I - oldI;
        #print (str(I) + " diff: " + str(diff))
        if (diff > 0):
            for n in range(0, len(infectedNodes)):
                neighborList.extend(BAgraph.neighbors(infectedNodes[n]))
                #neighborList = list(BAgraph.neighbors(infectedNodes[n]))  # get neighbors of the infected node
            test = list(set(neighborList))
            test = susceptibleList(test)
            draw = choice(test, diff, p=np.full(len(test), (1/len(test))), replace=False) # infect a neighbor
            #if draw not in infectedNodes:
            infect(draw)
            #print (str("How many: ") + str(len(draw)) + str(draw))

        # infect just after the iteration, time t+1, use temp array to store it
        # probabiltiy is a random number and if it's grater than 1 infect the person

        neighborList.clear()
        oldI = I

        nx.draw_networkx_edges(BAgraph, pos=pos, ax=ax, edge_color="black")
        nx.draw_networkx_nodes(BAgraph, pos=pos, node_color=colors)
        nx.draw_networkx_labels(BAgraph, pos=pos, labels=labels, font_color="white", ax=ax)
        ax.legend(labels=["{}".format(i)])
        #print (BAgraph.nodes[toInfect]['status'])

ani = FuncAnimation(fig, update, frames=100, interval=50, repeat=False)

plt.show()
