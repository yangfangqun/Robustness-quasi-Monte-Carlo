import networkx as nx
import numpy as np
import time
import graph_tools as gt
import igraph as ig
import matplotlib.pyplot as plt
from random import randint, sample

def inde_set(G):
    nlist = G.nodes
    sol = HXA(G, 'HDA')
    return list(set(nlist) ^ set(sol))

def list_to_dict(li_keys, li_values):

    dic = zip(li_keys, li_values)
    return dict(dic)

def ig_betweenness(G):
    g_i = ig.Graph.from_networkx(G)
    bc_v = g_i.betweenness()
    bc_k = list(G.nodes)
    bc = list_to_dict(bc_k, bc_v)
    return bc

### my_method
## 找到当前网络的关键节点

def find_best_node(G):
    g_i = ig.Graph.from_networkx(G)
    values = g_i.betweenness()
    keys = g_i.vs["_nx_name"]
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

## 通过多次随机，找到最优攻击序列(BC_CCW中不适用）
def find_best_sol(G):
    nlist = G.nodes
    N = 1
    best_R = 1
    best_sol = []
    R_sum = 0
    for i in range(N):
        sol = find_sol(G)
        solution = sol + list(set(nlist) ^ set(sol))
        R, x1, y1 = gt.ANC_ND(G,solution)
        R_sum += R
        print('R:      ', R)
        if R <= best_R:
            best_R = R
            best_sol = sol
            # if i % 1 == 0:
            #     print('best_R: ', best_R)
    print('best_R: ', best_R)
    print('R_mean: ', R_sum/N)
    return best_sol

### BC_CCW
def my_method(G):
    nlist = G.nodes
    ## my_method
    print('my_method: ')
    start = time.perf_counter()
    sol = find_best_sol(G)
    total_time = time.perf_counter() - start
    print("time:", total_time * 1000, "ms")
    solution = sol + list(set(nlist) ^ set(sol))
    R, x1, y1 = gt.ANC_ND(G, solution)
    print('My_method: ', R)
    # print('sol: ', solution)
    # print('nodes: ', len(solution))
    # print('dam: ', 1000 * (1 - R) / len(sol))
    return R, x1, y1

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
    # solution_method = solution
    R_HDA, x2, y2 = gt.ANC_ND(G, solution_method)
    print(method + '_ND: ', R_HDA)
    # print('sol: ', sol_method)
    # print('nodes: ', len(sol_method))
    # print('dam: ', 1000 * (1 - R_HDA) / len(sol_method))
    return R_HDA, x2, y2

### FINDER
def FINDER_method(G):
    nlist = G.nodes
    result_file = '../Finder_result/' + filename + '.txt'
    f = open(result_file, encoding='utf-8')
    f_list = f.readlines()
    sol_FINDER = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    # sol_FINDER = [int(i) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    solution_FINDER = sol_FINDER + list(set(nlist) ^ set(sol_FINDER))
    R_F, x4, y4 = gt.ANC_ND(G, solution_FINDER)
    print('FINDER_ND: ', R_F)
    return R_F, x4, y4

def main(data):
    ## 读文件
    global filename, nodes_keys
    filename = data
    ##
    infile = '../data/' + filename + '.gml'
    G0 = nx.read_gml(infile)
    nodes_keys = list(G0.nodes)

    print('开始计算网络：', filename)
    # r1, x1, y1 = my_method(G0)
    r2, x2, y2 = HXA_method(G0, 'HBA')
    print(x2)
    print(y2)
    # r3, x3, y3 = HXA_method(G0, 'HDA')
    # r4, x4, y4 = FINDER_method(G0)


if __name__=="__main__":
    print('BC_CCW')
    data = 'karate'
    main(data)
