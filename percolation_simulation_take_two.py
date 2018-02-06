import networkx as nx
import numpy as np
import matplotlib.pylab as plt
from scipy.ndimage import measurements
from collections import Counter
import itertools
import random

M, N = 50, 50 # size of a lattce
NOT_VISITED = 0

lattice = nx.grid_2d_graph(M, N)

attrs = {'status': 1} # 1 cell is closed, 0 cell is open

class PercolatedException(Exception): pass

def setup_lattice():
    for n,d in lattice.nodes(data=True):
        ''' Set entire lattice to be open'''
        lattice.nodes[n].update(attrs)

def open_entire_lattice():
    attrs = {'status' : 0}
    for n,d in lattice.nodes(data=True):
        lattice.nodes[n].update(attrs)

def open_random_nodes(number_of_seeds):
    possible_coordinates = [(x, y) for x in range(M) for y in range(1, N)]
    if (number_of_seeds == (M*N)):
        # open entire lattice
        open_entire_lattice()
    else :
        random_coordinates = random.sample(possible_coordinates, number_of_seeds)
        for s in range(0, len(random_coordinates)):
            #print ("(" + str(random_coordinates[s][0]) + ", " + str(random_coordinates[s][1]) + ")")
            lattice.nodes[random_coordinates[s]].update({'status': 0})
    return lattice

def noOfOpenNodes():
    open = 0
    for n, d in lattice.nodes(data=True):
        if (lattice.nodes[n]['status'] == 0):
            open += 1
    return open

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

def cluster_sizes_number(z2, p):
    lw, num = measurements.label(z2)
    totals = Counter(i for i in list(itertools.chain.from_iterable(lw.tolist())))

    cluster_sizes = []
    to_sum = []

    for i in range(2, (M * N)):
        if (totals[i]) > 0:
            cluster_sizes.append(totals[i])

    # check if cluster scales with the number of nodes

    for i in range(0, (M * N)):
        count = cluster_sizes.count(i)
        if count > 0:
            # exclude giant component from the summation
            if (((M*N) % count) == 0):
                if (count < int(((M*N)*p))):
                    n_s = count / (M * N)
                    #print("there is " + str(count) + " clusters of size: " + str(i) + ", n_s(p)=" + str(n_s) + ", sn_s=" + str(i * n_s))
                    to_sum.append(i * n_s)

    sum = 0
    for i in range (0, len(to_sum)):
        sum += to_sum[i]
    PG = -sum + p
    #print ("PG=" + str(PG))
    return PG

def degree_s(z2):
    lw, num = measurements.label(z2)
    totals = Counter(i for i in list(itertools.chain.from_iterable(lw.tolist())))

    cluster_sizes = []
    to_sum = []
    to_sum_squared = []

    for i in range(2, (M * N)):
        if (totals[i]) > 0:
            cluster_sizes.append(totals[i])

    for i in range(0, (M * N)):
        count = cluster_sizes.count(i)
        if count > 0:
            n_s = count / (M * N)
            # print("there is " + str(count) + " clusters of size: " + str(i) + ", n_s(p)=" + str(n_s) + ", sn_s=" + str(i * n_s))
            to_sum.append(i * n_s)
            to_sum_squared.append((i**2) * n_s)

    sum = 0
    sum_squared = 0

    for i in range(0, len(to_sum)):
        sum += to_sum[i]

    for i in range (0, len(to_sum_squared)):
        sum_squared += to_sum_squared[i]

    if sum_squared > 0:
        return sum/sum_squared
    else:
        return 0

# make sure to setup lattice first time
setup_lattice()

def print_lattice(lattice):
    cells = np.zeros(shape=(M,N))
    for n, d in lattice.nodes(data=True):
        cells[n[0]][n[1]] = lattice.nodes[n]['status']
    return (cells)

t = 100
pg_array = []
pg_array_average = []

ns_array = []
ns_array_average = []

sample_printed = False
pcount = {}
for p10 in range(0, 11):
    p = p10 / 10.0
    pcount[p] = 0
    for tries in range(t):
        cell = open_random_nodes(int((M*N)*p))
        percolated = check_from_top(cell)
        if percolated:
            pcount[p] += 1
            # find culster size here
        pg_array.append(cluster_sizes_number(print_lattice(lattice),p))
        ns_array.append(degree_s(print_lattice(lattice)))
    pg_array_average.append(np.mean(np.asarray(pg_array)))
    ns_array_average.append(np.mean(np.asarray(ns_array)))
    pg_array = []
    ns_array = []

ticks = []
xs = np.arange(0, 1.1, 0.1)
for x in xs:
    ticks.append(str(round(x, 2)))

plt.xticks(np.arange(0, 11), ticks)

plt.subplot(211)
plt.xlabel(r'$p$')
plt.ylabel(r'$P_{G}$')
plt.xticks(np.arange(0, 11), ticks)
plt.grid(True)
plt.plot(pg_array_average)
plt.title("A", loc='left')

plt.subplot(212)
plt.xticks(np.arange(0, 11), ticks)
plt.ylabel(r'$\left \langle s \right \rangle$')
plt.xlabel(r'$p_{c}$')
plt.plot(ns_array_average)
plt.title("B", loc='left')
plt.show()

