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

def BC_NNS(g_i):
    keys = g_i.vs["_nx_name"]
    dc_i = g_i.degree()
    dc = list_to_dict(keys, dc_i)
    low_dc_nodes2 = []
    dc2 = sorted(dc.items(), key=lambda x: x[1], reverse=False)
    # dc2 = sorted(dc.items(), key=lambda x: x[1], reverse=True)
    global n1
    global n2
    N1 = n1
    N2 = n2

    # dc2 = list(dc.items())
    # dc2 = random.sample(dc2, len(dc2))

    if (len(dc2) <= N1):
        N1 = int(len(dc2) * 0.85)
    for i in range(N1):
        low_dc_nodes2.append(dc2[i][0])
    low_odd = low_dc_nodes2[0::2]
    low_even = low_dc_nodes2[1::2]

    len_min = min(len(low_odd), len(low_even))

    if (len_min <= N2):
        N2 = int(len_min)
    S = random.sample(low_odd, N2)
    T = random.sample(low_even, N2)

    # S = low_odd
    # T = low_even
    s = list(map(keys.index, S))
    t = list(map(keys.index, T))
    bc_nns2 = np.array(g_i.betweenness(sources=s, targets=t))

    bc_nns =  bc_nns2

    return bc_nns

def find_best_node(g_i):
    keys = g_i.vs["_nx_name"]
    values = BC_NNS(g_i)
    maxTag = np.argmax(values)
    node = keys[maxTag]
    return node

# ## 找到网络的攻击序列

def find_sol(g_i):

    sol = []
    total_edges = g_i.ecount()
    while (g_i.ecount()>0):

        gcc = max(g_i.connected_components(), key=len)
        g_s = g_i.subgraph(gcc)
        node = find_best_node(g_s)
        keys = g_i.vs["_nx_name"]
        g_i.delete_vertices(keys.index(node))
        sol.append(node)
        processed_edges = total_edges - g_i.ecount()
        print(f"\rProcessed edges: {processed_edges}/{total_edges} ({processed_edges / total_edges:.2%})", end='')
    return sol

def main(data):
    ## 读文件
    file = data
    ##
    infile = '../../data/' + file + '.gml'
    G0 = nx.read_gml(infile)

    g_i = ig.Graph.from_networkx(G0)
    N = g_i.vcount()
    print('开始计算网络：', file)
    start = time.perf_counter()
    sol= find_sol(g_i)
    total_time = time.perf_counter() - start
    print("\nBCNNS_time:", total_time * 1000, "ms")
    print(len(sol))
    # with open(f"sol/{file}_BCNNS_sol.txt", "w+") as f:
    #     for node in sol:
    #         line = node + '\n'
    #         f.writelines(line)

    start = time.perf_counter()
    ANC = gt.getRobustness_ND_COST(G0, sol)
    total_time1 = time.perf_counter() - start
    print('ANC: ', ANC)
    print("ANC_time:", total_time1 * 1000, "ms")
    global n1
    global n2
    # with open(f"sol/{file}_BCNNS_inf.txt", "w+") as f:
    #     sampling_num = "N1: " + str(n1) + ",   N2: " + str(n2) + "\n"
    #     filename = "network: " + file + '\n'
    #     times = "time: " + str(total_time * 1000) + "ms"+ '\n'
    #     len_sol = "len_sol: " + str(len(sol))+ '\n'
    #     num_nodes = "Num of nodes: "+ str(N) + '\n'
    #     anc = "ANC: " + str(ANC)+ '\n'
    #     f.writelines("BCNNS:\n")
    #     f.writelines(filename)
    #     f.writelines(times)
    #     f.writelines(sampling_num)
    #     f.writelines(len_sol)
    #     f.writelines(num_nodes)
    #     f.writelines(anc)

n1 = 2300
n2 = 80

if __name__=="__main__":
    print('BC_NNS_plus')
    #Celegansneural
    data = 'Oregon1'
    # data = 'Crime'
    # data = 'Airport'
    # data = 'Karate'
    # data = 'Power'
    main(data)

