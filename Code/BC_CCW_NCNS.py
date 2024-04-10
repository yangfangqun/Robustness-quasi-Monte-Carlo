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

# def low_degree_nodes_old(G):
#     dc = dict(nx.degree(G))
#     dc_m = np.quantile(np.array(list(dc.values())),0.6)
#     low_dc_nodes = []
#     for u in dc.items():
#         if u[1] <= int(dc_m):
#             low_dc_nodes.append(u[0])
#     return low_dc_nodes

def low_degree_nodes(G):
    dc = nx.degree_centrality(G)
    dc = sorted(dc.items(), key=lambda x:x[1])
    low_dc_nodes = []
    N = int(len(dc) * 0.8)
    if(len(dc) <= 10):
        N = int(len(dc) * 0.8)
    # print(len(dc),N)  # 打印采样节点数量
    for i in range(N):
        low_dc_nodes.append(dc[i][0])
    return low_dc_nodes

# def inde_set(G):
#     nlist = G.nodes
#     sol = HXA(G, 'HDA')
#     return list(set(nlist) ^ set(sol))
#
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
# def find_best_node_old(G, sub_inde_set):
#
#     bc = ig_betweenness(G)
#     keys = list(bc.keys())
#     values = list(bc.values())
#     maxTag = np.argmax(values)
#     node = keys[maxTag]
#     return node

# def find_best_node(G):
#     low_set = low_degree_nodes(G)
#     # print(len(low_set)/len(G.nodes))  # 打印采样比例
#     S = sample(low_set, int(len(low_set)*0.5))
#     T = list(set(low_set) ^ set(S))
#     bc = nx.betweenness_centrality_subset(G, S, T, normalized=False,weight=None)
#     keys = list(bc.keys())
#     values = list(bc.values())
#     maxTag = np.argmax(values)
#     node = keys[maxTag]
#     return node

def find_best_node(G):
    g_i = ig.Graph.from_networkx(G)
    keys = g_i.vs["_nx_name"]
    low_set = low_degree_nodes(G)
        # print(len(low_set)/len(G.nodes))  # 打印采样比例
    S = sample(low_set, int(len(low_set)*0.5))
    T = list(set(low_set) ^ set(S))
    s = list(map(keys.index, S))
    t = list(map(keys.index, T))
    values = g_i.betweenness(sources=s, targets=t)
    # print(values)
    # values = g_i.betweenness()
    maxTag = np.argmax(values)
    node = keys[maxTag]
    return node

# def find_best_node(G):
#     g_i = ig.Graph.from_networkx(G)
#     keys = g_i.vs["_nx_name"]
#     low_set = low_degree_nodes(G)
#     S = random.sample(low_set, len(low_set)//2)
#     T = list(set(low_set) - set(S))
#     s = [keys.index(node) for node in S]
#     t = [keys.index(node) for node in T]
#     values = g_i.betweenness(sources=s, targets=t)
#     maxTag = np.argmax(values)
#     node = keys[maxTag]
#     return node


# ## 找到网络的攻击序列
def find_sol(G):
    g = G.copy()

    sol = []
    N = G.number_of_nodes()
    for i in tqdm(range(N)):
        gcc = max(nx.connected_components(g), key=len)
        if len(gcc) <= 1:
            break
        g_s = g.subgraph(gcc)
        u = find_best_node(g_s)
        g.remove_node(u)  # 删除节点会破坏原始网络，注意这种情况下使用deepcopy，networkx的G.copy()是深拷贝
        sol.append(u)
    return sol





## 通过多次随机，找到最优攻击序列
def find_best_sol(G):

    nlist = G.nodes

    N = 1

    best_R = 1
    best_sol = []
    R_sum = 0
    count = 0
    for i in range(N):

        sol = find_sol(G)
        solution = sol + list(set(nlist) ^ set(sol))
        R, x1, y1 = gt.ANC_ND_COST(G,solution)
        R_sum += R
        # print('R:      ', R)
        if R < best_R:
            best_R = R
            best_sol = sol
            print('best_R: ', best_R)
        else:
            count += 1
        if count >= 5:
            break
    print('best_R: ', best_R)
    # print('R_mean: ', R_sum/N)
    return best_sol

def my_method(G):
    nlist = G.nodes
    ## my_method
    print('my_method: ')
    start = time.perf_counter()
    sol = find_best_sol(G)
    total_time = time.perf_counter() - start
    print("time:", total_time * 1000, "ms")
    solution = sol + list(set(nlist) ^ set(sol))
    R, x1, y1 = gt.ANC_ND_COST(G, solution)
    print('My_method: ', R)
    # print('sol: ', solution)
    # print('nodes: ', len(sol))
    # print('dam: ', 1000 * (1 - R) / len(sol))


### HXA
def HXA(G, method):
    # 'HDA', 'HBA', 'HPRA', ''
    sol = []
    g = G.copy()
    while (nx.number_of_edges(g)>0):  #当边为0时，只剩下孤立节点，不计入sol
        if method == 'HDA':
            dc = nx.degree_centrality(g)
        elif method == 'HBA':
            dc = ig_betweenness(g)    # best method
            # dc = nx.betweenness_centrality(g)
        elif method == 'HCA':
            dc = nx.closeness_centrality(g)
        elif method == 'HPRA':
            dc = nx.pagerank(g)
        keys = list(dc.keys())
        values = list(dc.values())
        maxTag = np.argmax(values)
        node = keys[maxTag]
        sol.append(node)
        g.remove_node(node)
    return sol

def HXA_method(G, method):
    nlist = G.nodes
    print(method + ': ')
    start = time.perf_counter()
    sol_method = HXA(G, method)
    total_time = time.perf_counter() - start
    print("time:", total_time * 1000, "ms")
    solution_method = sol_method + list(set(nlist) ^ set(sol_method))
    print(solution_method)
    # solution_method = solution
    # R_HDA, x2, y2 = gt.ANC_ND(G, solution_method)
    R_HDA = gt.getRobustness_ND_COST(G,sol_method)
    # print(sum(r) / len(r))
    print(method + '_ND: ', R_HDA)
    # print('sol: ', sol_method)
    # print('nodes: ', len(sol_method))
    # print('dam: ', 1000 * (1 - R_HDA) / len(sol_method))



def FINDER_method(G):
    nlist = G.nodes
    result_file = '../Finder_result/' + filename + '.txt'
    f = open(result_file, encoding='utf-8')
    f_list = f.readlines()
    sol_FINDER = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    # sol_FINDER = [int(i) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    solution_FINDER = sol_FINDER + list(set(nlist) ^ set(sol_FINDER))
    start = time.perf_counter()
    R_F, x4, y4 = gt.ANC_ND_COST(G, solution_FINDER)
    total_time = time.perf_counter() - start
    print("ANC_time:", total_time * 1000, "ms")
    start = time.perf_counter()
    r = gt.getRobustness_ND_COST(G,sol_FINDER)
    total_time = time.perf_counter() - start
    print("Roubust_time:", total_time * 1000, "ms")
    print('FINDER_ND: ', R_F)
    print(sum(r)/len(r))
    print(sum(y4)/len(y4))
    # print(r)
    # print(y4)


def main(data):
    ## 读文件
    global filename, nodes_keys
    filename = data
    ##

    infile = '../data/' + filename + '.gml'
    G0 = nx.read_gml(infile)
    nodes_keys = list(G0.nodes)

    print('开始计算网络：', filename)
    # my_method(G0)
    #
    # HXA_method(G0, 'HBA')
    HXA_method(G0, 'HDA')
    # FINDER_method(G0)


if __name__=="__main__":
    print('BC_GCCW_NCNS')
    #Celegansneural
    data = 'Krebs'
    main(data)
