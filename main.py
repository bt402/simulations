import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from pprint import pprint as pp

''' 
p - probability of node being occupied
(1 - p) - probability of node being empty
pc - critical value i.e. thershold
PG - probability that node is in the giant cluster 
'''

# TODO 1. Plot p / Pg

M, N = 20, 20
NOT_VISITED = 0

class PercolatedException(Exception): pass

#er_graph = nx.erdos_renyi_graph(N, p)
lattice = nx.grid_2d_graph(N, N)

attrs = {'status': 1} # 1 cell is closed, 0 cell is open

def reset_lattice():
    for n,d in lattice.nodes(data=True):
        ''' Set entire lattice to be open'''
        lattice.nodes[n].update(attrs)

def open_random_nodes(p):
    reset_lattice()
    randomize = [[int(np.random.random() < p) for m in range(M)] for n in range(N)]
    for m in range(len(randomize)):
        for n in range(len(randomize[m])):
            lattice.nodes[(m,n)].update({'status': randomize[m][n]})
    return lattice

def noOfOpenNodes():
    open = 0
    for n, d in lattice.nodes(data=True):
        if (lattice.nodes[n]['status'] == 0):
            open += 1
    return open

'''
#G is the networkx graph
sub_graphs = list(nx.connected_component_subgraphs(lattice))

#n gives the number of sub graphs
n = len(sub_graphs)

# you can now loop through all nodes in each sub graph
for i in range(n):
    print ("Subgraph:", i, "consists of ",sub_graphs[i].nodes())
'''

def check_from_top(cell):
    n, walk_index = 0, 1
    try:
        for m in range(M):
            if cell.nodes[(n,m)]['status'] == NOT_VISITED:
                walk_index += 1
                walk_maze(m, n, cell, walk_index)
    except PercolatedException as ex:
        return ex
    return None

def walk_maze(m, n, cell, indx):
    # fill cell
    cell.nodes[(n, m)].update({'status': indx})
    # down
    if n < N - 1 and cell.nodes[(n + 1,m)]['status'] == NOT_VISITED:
        walk_maze(m, n + 1, cell, indx)
    # THE bottom
    elif n == N - 1:
        raise PercolatedException((m, n + 1))
    # left
    if m and cell.nodes[(n,m - 1)]['status'] == NOT_VISITED:
        walk_maze(m - 1, n, cell, indx)
    # right
    if m < M - 1 and cell.nodes[(n,m + 1)]['status'] == NOT_VISITED:
        walk_maze(m + 1, n, cell, indx)
    # up
    if n and cell.nodes[(n - 1,m)]['status'] == NOT_VISITED:
        walk_maze(m, n - 1, cell, indx)

reset_lattice()
'''
pcount = {}
for p in range (0, 11):
    fraction = int((M*N) * (p/10))
    open_random_nodes(fraction)
    print (noOfOpenNodes() / (M*N))
    fraction_of_open.append(noOfOpenNodes() / (M*N))

    p10 = p / 10.0
    pcount[p10] = 0

    percolated = check_from_top(lattice)
    if percolated:
        pcount[p10] += 1
        print('\nSample percolating %i x %i, p = %5.2f grid\n' % (M, N, p/10))
    reset_lattice()
'''

t = 100

sample_printed = False
pcount = {}
for p10 in range(11):
    p = p10 / 10.0
    pcount[p] = 0
    for tries in range(t):
        cell = open_random_nodes(p)
        percolated = check_from_top(cell)
        if percolated:
            pcount[p] += 1
            #print('\nSample percolating %i x %i, p = %5.2f grid\n' % (M, N, p))


pp({p: c / float(t) for p, c in pcount.items()})

dictlist = []

for key, value in pcount.items():
    temp = [key,value]
    dictlist.append(temp)

#nx.draw(lattice)
col  = [row[1] for row in dictlist]

ticks = []
xs = np.arange(0, 1.1, 0.1)
for x in xs:
    ticks.append(str(x))

plt.xticks(np.arange(0, 11), ticks)
plt.plot(col[::-1])
plt.show()