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

def low_degree_nodes(G):
    dc = nx.degree_centrality(G)
    # dc = sorted(dc.items(), key=lambda x:x[1], reverse=True)
    dc = sorted(dc.items(), key=lambda x:x[1])
    low_dc_nodes = []
    N = int(len(dc) * 0.05) #低度节点比例
    if(len(dc) <= 10):
        N = int(len(dc) * 0.8)
    for i in range(N):
        low_dc_nodes.append(dc[i][0])
    return low_dc_nodes

def list_to_dict(li_keys, li_values):
    dic = zip(li_keys, li_values)
    return dict(dic)

### my_method
## 找到当前网络的关键节点

def ig_betweenness(G):
    g_i = ig.Graph.from_networkx(G)
    bc_v = g_i.betweenness()
    bc_k = list(G.nodes)
    bc = list_to_dict(bc_k, bc_v)
    return bc

def find_best_node(G):
    g_i = ig.Graph.from_networkx(G)
    keys = g_i.vs["_nx_name"]
    low_set = low_degree_nodes(G)
    S = sample(low_set, int(len(low_set)*0.5))
    T = list(set(low_set) ^ set(S))
    s = list(map(keys.index, S))
    t = list(map(keys.index, T))
    # values1 = np.array(g_i.betweenness(sources=s, targets=t))

    low = list(map(keys.index, low_set))
    values1 = np.array(g_i.betweenness(sources=low, targets=low))

    values2 = np.array(g_i.betweenness())
    v1_max = np.max(values1)
    v1_min = np.min(values1)
    v2_max = np.max(values2)
    v2_min = np.min(values2)
    n_values1 = (values1 -v1_min)/(v1_max - v1_min + 0.00001)
    n_values2 = (values2 - v2_min) / (v2_max - v2_min + 0.00001)
    a = 0.4
    values = n_values1*a + n_values2*(1-a)
    maxTag = np.argmax(values)
    node = keys[maxTag]
    return node



## 找到网络的攻击序列
def find_sol(G):
    g = G.copy()
    sol = []
    N = G.number_of_nodes()
    for i in range(N):
        gcc = max(nx.connected_components(g), key=len)
        if len(gcc) <= 1:
            break
        g_s = g.subgraph(gcc)
        u = find_best_node(g_s)
        g.remove_node(u)  # 删除节点会破坏原始网络，注意这种情况下使用deepcopy，networkx的G.copy()是深拷贝
        sol.append(u)
    return sol


def main(data):
    ## 读文件
    global filename, nodes_keys
    filename = data
    ##
    infile = '../../data/' + filename + '.gml'
    G0 = nx.read_gml(infile)
    print('开始计算网络：', filename)
    start = time.perf_counter()
    sol = find_sol(G0)
    print(sol)
    total_time = time.perf_counter() - start
    print("time:", total_time * 1000, "ms")
    print(gt.getRobustness_ND_COST(G0, sol))

if __name__=="__main__":
    print('BC_NNS')
    #Celegansneural
    data = 'Power'
    main(data)
