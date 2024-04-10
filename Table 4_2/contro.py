# Example: rand node-removal on Random Graph networks

import timeit
import numpy as np
import random
import networkx as nx
import igraph as ig



N = 1000    # nodes
M = 5*N     # edges
G = nx.gnm_random_graph(N, M, directed=True)
g_i = ig.Graph.from_networkx(G)

start = timeit.default_timer()
adj_matrix = g_i.get_adjacency().data
adj_matrix = np.array(adj_matrix)
stop = timeit.default_timer()
print('Time: ', (stop - start)*1000)
cv = []     # controllability curve

start = timeit.default_timer()
A = nx.adjacency_matrix(G).todense()
#print(np.linalg.matrix_rank(A))
stop = timeit.default_timer()
print('Time: ', (stop - start)*1000)

start = timeit.default_timer()
cv.append(max(N-np.linalg.matrix_rank(A), 1)/N)
stop = timeit.default_timer()
print('Time: ', stop - start)

for i in range(N-1):
    nid = random.choice(list(G))

    start = timeit.default_timer()
    G.remove_node(nid)
    stop = timeit.default_timer()
    print('Time: ', (stop - start) * 1000)

    A = nx.adjacency_matrix(G).todense()
    #print(np.linalg.matrix_rank(A))
    # cv.append(max(G.number_of_nodes()-np.linalg.matrix_rank(A), 1) / G.number_of_nodes())

print(sum(cv))



#
# average run time = 162.68s
# Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz 2.59GHz
# Installed memory (RAM): 16.0GB (15.8 usable)
# Windows 10 Home 64-bit Operating System

