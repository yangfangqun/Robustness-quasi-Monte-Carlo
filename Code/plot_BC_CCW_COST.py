import networkx as nx
import numpy as np
import time
import graph_tools as gt
import igraph as ig
import operator, pylab, random
import matplotlib.pyplot as plt
from random import randint, sample
import seaborn as sns
import pandas as pd
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

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
        R, x, y = gt.ANC_ND_COST(G,solution)
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
    R1, x1, y1 = gt.ANC_ND_COST(G, solution)
    print('My_method: ', R1)
    # print('sol: ', solution)
    # print('nodes: ', len(solution))
    # print('dam: ', 1000 * (1 - R) / len(sol))
    return R1, x1, y1

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
    R_HDA, x2, y2 = gt.ANC_ND_COST(G, solution_method)
    print(method + '_ND: ', R_HDA)
    # print('sol: ', sol_method)
    # print('nodes: ', len(sol_method))
    # print('dam: ', 1000 * (1 - R_HDA) / len(sol_method))
    return R_HDA, x2, y2

### FINDER
def FINDER_method(G):
    nlist = G.nodes
    result_file = '../result/' + filename + '.txt'
    f = open(result_file, encoding='utf-8')
    f_list = f.readlines()
    sol_FINDER = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    # sol_FINDER = [int(i) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    solution_FINDER = sol_FINDER + list(set(nlist) ^ set(sol_FINDER))
    R_F, x4, y4 = gt.ANC_ND_COST(G, solution_FINDER)
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
    r1, x1, y1 = my_method(G0)
    r2, x2, y2 = HXA_method(G0, 'HBA')
    r3, x3, y3 = HXA_method(G0, 'HDA')
    r4, x4, y4 = FINDER_method(G0)

    #画图

    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 500
    TickSize = 11
    LabelSize = 18
    Labelpad = 5
    LegendSize = 18
    # Linewidth = 4

    fig, ax = plt.subplots()

    ax.plot(x1, y1, color='r', linestyle='-', alpha=0.8, linewidth=0.8, ms=2, label='$B{{C}_{GCCW}}$')
    ax.plot(x2, y2, color='b', linestyle='-',  alpha=0.8, linewidth=0.8, ms=2, label='HBA')
    ax.plot(x4, y3, color='g', linestyle='-',  alpha=0.8, linewidth=0.8, ms=2,label='HDA')
    ax.plot(x4, y4, color='k', linestyle='-',  alpha=0.8, linewidth=0.8, ms=2,label='FINDER')
    ax.set_ylabel('GCC size of residual network', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('Fraction of removed nodes', fontweight='bold', fontsize=LabelSize)
    ax.set_title(filename, fontweight='bold', fontsize=LabelSize)
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    xmajorLocator = MultipleLocator(0.1)  # 将x主刻度标签设置为0.05的倍数
    xmajorFormatter = FormatStrFormatter('%.1f')  # 设置x轴标签文本的格式
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)

    ymajorLocator = MultipleLocator(0.2)  # 将y轴主刻度标签设置为0.5的倍数
    ymajorFormatter = FormatStrFormatter('%.1f')  # 设置y轴标签文本的格式
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)
    # legend_properties = {'weight': 'bold'}
    ax.legend(loc='upper right', fontsize=LegendSize)

    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    fig.tight_layout()
    plt.show()



    # pylab.figure(1, dpi=500)
    # pylab.title(filename)
    # # pylab.title('Karate')
    # pylab.xlabel(r"Fraction of removed nodes")
    # pylab.ylabel(r"GCC size of residual network")
    # pylab.ylim(-0.05,1.1)
    # #pylab.xlim(0,1.1)
    # pylab.plot(x1, y1, "r-", alpha=0.8, linewidth=0.8, ms=2)
    # pylab.plot(x2, y2, "b-", alpha=0.8, linewidth=0.8, ms=2)
    # pylab.plot(x3, y3, "g-", alpha=0.8, linewidth=0.8, ms=2)
    # pylab.plot(x4, y4, "k-", alpha=0.8, linewidth=0.8, ms=2)
    #
    # #画图时的标签
    # pylab.legend((r"$B{{C}_{GCCW}}$",
    #                   "HBA",
    #               "HDA",
    #               "FINDER"
    #               ),
    #                  loc = "upper right", shadow = False)
    # pylab.show()
    # pylab.close(1)


if __name__=="__main__":
    print('BC_CCW')
    data = 'Karate'
    main(data)
