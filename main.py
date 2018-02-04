import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from pprint import pprint as pp
from pylab import *
from scipy.ndimage import measurements
from collections import Counter
import itertools
from scipy.signal import _savitzky_golay

''' 
p - probability of node being occupied
(1 - p) - probability of node being empty
pc - critical value i.e. thershold
PG - probability that node is in the giant cluster 
'''

# clusters can be of size 1 (isolates) to N

# Done write a function that finds clusters of size s
# TODO Plot p / Pg, not really done...

M, N = 30, 30
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

cells = np.zeros(shape=(M,N))

def print_lattice(cell):
    for n, d in lattice.nodes(data=True):
        cells[n[0]][n[1]] = cell.nodes[n]['status']
    return (cells)

PG_array = []

def cluster_sizes_number(z2, p):
    lw, num = measurements.label(z2)
    totals = Counter(i for i in list(itertools.chain.from_iterable(lw.tolist())))

    cluster_sizes = []
    to_sum = []

    for i in range(2, (M * N)):
        if (totals[i]) > 0:
            cluster_sizes.append(totals[i])

    for i in range(0, (M * N)):
        count = cluster_sizes.count(i)
        if count > 0:
            n_s = count / (M * N)
            #print("there is " + str(count) + " clusters of size: " + str(i) + ", n_s(p)=" + str(n_s) + ", sn_s=" + str(i * n_s))
            to_sum.append(i * n_s)

    sum = 0

    for i in range (0, len(to_sum)):
        sum += to_sum[i]
    PG = -sum + p
    #print ("PG=" + str(PG))
    PG_array.append(PG)
    return PG

degree_s_array = []

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
        degree_s_array.append((sum/sum_squared))
        return sum/sum_squared
    else:
        degree_s_array.append(0)
        return 0

reset_lattice()

t = 100
avera_arr = []
deg = []
test = []
test2 = []

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
            # find culster size here
        avera_arr.append(cluster_sizes_number(print_lattice(lattice),p))
        deg.append(degree_s(print_lattice(lattice)))
    test.append(np.mean(np.asarray(avera_arr)))
    test2.append(np.mean(np.asarray(deg)))
    avera_arr = []
    deg = []
            #print('\nSample percolating %i x %i, p = %5.2f grid\n' % (M, N, p))


pp({p: c / float(t) for p, c in pcount.items()})

dictlist = []

for key, value in pcount.items():
    temp = [key,value]
    dictlist.append(temp)

col = [row[1] for row in dictlist]

ticks = []
xs = np.arange(0, 1.1, 0.1)
for x in xs:
    ticks.append(str(x))

plt.xticks(np.arange(0, 11), ticks)

yhat = _savitzky_golay.savgol_filter(test, 9, 3) # window size 73, polynomial order 2

plt.subplot(211)
plt.xlabel(r'$p$')
plt.ylabel(r'$P_{G}$')
plt.xticks(np.arange(0, 11), ticks)
plt.grid(True)
plt.plot(yhat, "r-")
plt.title("A", loc='left')

pos = np.where(np.asarray(test2) <= 0.5)

pos = np.array(pos).ravel().tolist()


for i in pos:
    if (i > 0 and i <8):
        test2[i] = np.nan

print (test2)

plt.subplot(212)
plt.xticks(np.arange(0, 11), ticks)
plt.ylabel(r'$\left \langle s \right \rangle$')
plt.xlabel(r'$p_{c}$')
plt.plot(test2)
plt.title("B", loc='left')
plt.show()