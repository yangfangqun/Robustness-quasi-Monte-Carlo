import networkx as nx
import numpy as np
import time
import graph_tools as gt
import igraph as ig
from tqdm import tqdm
import random
import matplotlib.pyplot as plt
from random import randint, sample
import os

def list_to_dict(li_keys, li_values):
    dic = zip(li_keys, li_values)
    return dict(dic)

### my_method
## 找到当前网络的关键节点

# def low_degree_nodes(g_i):
#     keys = g_i.vs["_nx_name"]
#     dc_i = g_i.degree()
#     dc = list_to_dict(keys, dc_i)
#     dc = sorted(dc.items(), key=lambda x:x[1])
#     low_dc_nodes = []
#     # N = int(len(dc) * 0.4) #低度节点比例
#     N = 2000
#     if(len(dc) <= 2000):
#         N = int(len(dc) * 0.8)
#     for i in range(N):
#         low_dc_nodes.append(dc[i][0])
#     return low_dc_nodes

def BC_NNS(g_i):
    keys = g_i.vs["_nx_name"]
    dc_i = g_i.degree()
    dc = list_to_dict(keys, dc_i)
    dc = sorted(dc.items(), key=lambda x: x[1])


    N1 = 200
    low_dc_nodes1 = []
    if (len(dc) <= N1):
        N1 = int(len(dc) * 0.9)
    for i in range(N1):
        low_dc_nodes1.append(dc[i][0])

    low_odd = low_dc_nodes1[0::2]
    low_even = low_dc_nodes1[1::2]
    S = low_odd
    T = low_even
    s = list(map(keys.index, S))
    t = list(map(keys.index, T))
    bc_nns = np.array(g_i.betweenness(sources=s, targets=t))

    return bc_nns

# def BC_NNS(g_i):
#     keys = g_i.vs["_nx_name"]
#     dc_i = g_i.degree()
#     dc = list_to_dict(keys, dc_i)
#     dc = sorted(dc.items(), key=lambda x: x[1])
#
#     N1 = 200
#     low_dc_nodes1 = []
#     if (len(dc) <= N1):
#         N1 = int(len(dc) * 1)
#     for i in range(N1):
#         low_dc_nodes1.append(dc[i][0])
#
#     low_odd = low_dc_nodes1[0::2]
#     low_even = low_dc_nodes1[1::2]
#
#     num_nodes = min(len(low_odd), len(low_even))
#     if num_nodes > 50:
#         K = int(num_nodes * 0.8)
#         K = K + int(K < 50)*(50-K)
#     else:
#         K = int(num_nodes * 0.8)
#
#     bc_nns = np.zeros_like(keys, dtype=np.float64)
#     if K > 10:
#         for i in range(1):
#             S = sample(low_odd, K)
#             T = sample(low_even, K)
#             s = list(map(keys.index, S))
#             t = list(map(keys.index, T))
#             values1 = np.array(g_i.betweenness(sources=s, targets=t))
#             v1_max = np.max(values1)
#             v1_min = np.min(values1)
#             bc_nns += (values1 -v1_min)/(v1_max - v1_min + 0.00001)
#     else:
#         S = low_odd
#         T = low_even
#         s = list(map(keys.index, S))
#         t = list(map(keys.index, T))
#         values1 = np.array(g_i.betweenness(sources=s, targets=t))
#         v1_max = np.max(values1)
#         v1_min = np.min(values1)
#         bc_nns += (values1 - v1_min) / (v1_max - v1_min + 0.00001)
#
#     return bc_nns


# def BC_NNS(g_i):
#     keys = g_i.vs["_nx_name"]
#     dc_i = g_i.degree()
#     dc = list_to_dict(keys, dc_i)
#     dc = sorted(dc.items(), key=lambda x: x[1])
#
#     N1 = 400
#     low_dc_nodes1 = []
#     if (len(dc) <= N1):
#         N1 = int(len(dc) * 1)
#     for i in range(N1):
#         low_dc_nodes1.append(dc[i][0])
#     # S = sample(low_dc_nodes1, int(len(low_dc_nodes1) * 0.5))
#     # T = list(set(low_dc_nodes1) ^ set(S))
#     # s = list(map(keys.index, S))
#     # t = list(map(keys.index, T))
#     # values1 = np.array(g_i.betweenness(sources=s, targets=t))
#
#     li = list(map(keys.index, low_dc_nodes1))
#     # k = int(len(li)/2)
#     s = li[0::2]
#     t = li[1::2]
#     # s = t = li
#     values1 = np.array(g_i.betweenness(sources=s, targets=t))
#
#     # s = t = list(map(keys.index, low_dc_nodes1))
#     # values1 = np.array(g_i.betweenness(sources=s, targets=t))
#
#     N2 = 100
#     low_dc_nodes2 = []
#     if (len(dc) <= N2):
#         N2 = int(len(dc) * 0.1)
#     for i in range(N2):
#         low_dc_nodes2.append(dc[i][0])
#     li1 = list(map(keys.index, low_dc_nodes2))
#     s = li1[0::2]
#     t = li1[1::2]
#     values2 = np.array(g_i.betweenness(sources=s, targets=t))
#     v1_max = np.max(values1)
#     v1_min = np.min(values1)
#     v2_max = np.max(values2)
#     v2_min = np.min(values2)
#     n_values1 = (values1 -v1_min)/(v1_max - v1_min + 0.00001)
#     n_values2 = (values2 - v2_min) / (v2_max - v2_min + 0.00001)
#     a = 1
#     bc_nns = n_values1*a + n_values2*(1-a)
#     return bc_nns


def find_best_node(g_i):
    keys = g_i.vs["_nx_name"]
    values = BC_NNS(g_i)
    maxTag = np.argmax(values)
    node = keys[maxTag]
    return node

# ## 找到网络的攻击序列

def find_sol(G):
    g_i = ig.Graph.from_networkx(G)
    sol = []
    total_edges = g_i.ecount()
    print_time = 0
    while (g_i.ecount()>0):

        gcc = max(g_i.connected_components(), key=len)
        g_s = g_i.subgraph(gcc)
        node = find_best_node(g_s)
        keys = g_i.vs["_nx_name"]
        g_i.delete_vertices(keys.index(node))
        sol.append(node)
        start = time.perf_counter()
        processed_edges = total_edges - g_i.ecount()
        print(f"\rProcessed edges: {processed_edges}/{total_edges} ({processed_edges / total_edges:.2%})", end='')
        total_time = time.perf_counter() - start
        print_time += total_time
    return sol, print_time

def main(data):
    ## 读文件
    global filename, nodes_keys
    filename = data
    ##
    infile = '../../data/' + filename + '.gml'
    G0 = nx.read_gml(infile)
    print('开始计算网络：', filename)
    start = time.perf_counter()
    sol, pt = find_sol(G0)
    total_time = time.perf_counter() - start - pt
    print("\nattack_time:", total_time * 1000, "ms")
    print(len(sol))

    start = time.perf_counter()
    ANC = gt.getRobustness_ND_COST(G0, sol)
    total_time = time.perf_counter() - start
    print('ANC: ', ANC)
    print("ANC_time:", total_time * 1000, "ms")

if __name__=="__main__":
    print('BC_NNS_plus')
    #Celegansneural
    # data = 'Collaboration'
    data = 'Airport'
    main(data)
