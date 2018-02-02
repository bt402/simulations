import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

''' 
p - probability of node being occupied
(1 - p) - probability of node being empty
pc - critical value i.e. thershold
PG - probability that node is in the giant cluster 
'''

# TODO 1. Plot p / Pg

M, N = 10, 10
NOT_VISITED = 0

class PercolatedException(Exception): pass

#er_graph = nx.erdos_renyi_graph(N, p)
lattice = nx.grid_2d_graph(N, N)

attrs = {'status': 1} # 1 cell is closed

def reset_lattice():
    for n,d in lattice.nodes(data=True):
        ''' Set entire lattice to be open'''
        lattice.nodes[n].update(attrs)

def open_random_nodes(fraction):
    for i in range(0, fraction):
        node_pos = (np.random.randint(0, M), np.random.randint(0, N))
        # infect one random node
        lattice.nodes[node_pos].update({'status': 0}) # 0 cell is open

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

for p in range (0, 100, 10):
    fraction = int((M*N) * (p/100))
    open_random_nodes(fraction)
    print (noOfOpenNodes() / (M*N))

    percolated = check_from_top(lattice)
    if percolated:
        print('\nSample percolating %i x %i, p = %5.2f grid\n' % (M, N, p))
    reset_lattice()

#nx.draw(lattice)
plt.show()