import networkx as nx
import operator, random, numpy
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import igraph as ig
from copy import copy, deepcopy


def ig_copy(g_i):
    # 只能复制连通图，注意使用场景，效率很快
    return g_i.subgraph(g_i.connected_components()[0])

def sigma_ND(g_i):
    # igraph 优化版
    if g_i.vcount() == 0:
        return 0
    sigma = len(max(g_i.connected_components(), key=len))
    return sigma

# def getRobustness_ND_COST(g, sol):
#     # igraph 优化版
#     g_i = ig.Graph.from_networkx(g)
#     N = g_i.vcount()
#     Robust = [0 for i in  range(N+1)]
#     Robust[0] = 1
#     Robust[N] = 0  # 最后一个节点
#     for i in tqdm(range(len(sol)-1)):
#         keys = g_i.vs["_nx_name"]
#         g_i.delete_vertices(keys.index(sol[i]))
#         gcc = max(g_i.connected_components(), key=len)
#         robust = len(gcc) / N
#         Robust[i+1] = robust
#     return sum(Robust)/(N+1)

def getRobustness_ND_COST(G, sol):
    # igraph 优化版   GA用
    g = G.copy()
    g_i = ig.Graph.from_networkx(g)
    N = g_i.vcount()
    Robust = [0 for i in  range(N+1)]
    Robust[0] = 1
    Robust[N] = 0  # 最后一个节点
    for i in range(len(sol)):
        keys = g_i.vs["_nx_name"]
        g_i.delete_vertices(keys.index(sol[i]))
        sigma = sigma_ND(g_i)
        if sigma <= 1:
            sigma = 0
            break
        robust = sigma / N
        Robust[i + 1] = robust
    return sum(Robust)/(N+1)

def getRobustness_ND_COST_X(g, sol,X):
    # igraph 优化版
    # 调用时传入完整的sol，以便加速
    g_i = g.copy()
    N = g_i.vcount()
    Robust = [0 / N for i in range(N + 1)]
    Robust[0] = 1
    Robust[N] = 0  # 最后一个节点
    sigma = sigma_ND(g_i)
    for i in range(len(sol)):
        #考虑到生存率的情况，要攻击到最后一个节点
        keys = g_i.vs["_nx_name"]
        if X[i] == 1:
            g_i.delete_vertices(keys.index(sol[i]))
            sigma = sigma_ND(g_i)
        if sigma <= 1:
            sigma = 0
            break
        robust = sigma / N
        Robust[i+1] = robust
    return sum(Robust)/(N+1)



def getRobustness_ND(g, sol):
    #sol是攻击到Gcc为1的时候
    N = nx.number_of_nodes(g)
    Robust = [1/N for i in  range(N+1)]
    Robust[0] = 1
    Robust[N] = 0 #最后一个节点
    g_copy = g.copy()
    for i in range(len(sol)):
        g_copy.remove_node(sol[i])
        Gcc = max(nx.connected_components(g_copy), key = len)
        robust = len(Gcc) / N
        Robust[i+1] = robust
    return Robust

# def getRobustness_ND_COST(g, sol):
#     N = nx.number_of_nodes(g)
#     Robust = [0 for i in  range(N+1)]
#     Robust[0] = 1
#     Robust[N] = 0  # 最后一个节点
#     g_copy = g.copy()
#     for i in range(len(sol)-1):
#         g_copy.remove_node(sol[i])
#         Gcc = max(nx.connected_components(g_copy), key = len)
#         robust = len(Gcc) / N
#         Robust[i+1] = robust
#     return Robust
def getRobustness_ND_X(g, sol,X):
    nlist = g.nodes
    sol = sol + list(set(nlist) ^ set(sol))
    N = nx.number_of_nodes(g)
    Robust = [1 / N for i in range(N + 1)]
    Robust[0] = 1
    Robust[N] = 0  # 最后一个节点
    g_copy = g.copy()
    for i in range(len(sol)):
        #考虑到生存率的情况，要攻击到最后一个节点
        if X[i] == 1:
            g_copy.remove_node(sol[i])
        sigma = sigma_ND(g_copy)
        robust = sigma / N
        Robust[i+1] = robust
    return sum(Robust)/(N+1)

def ANC_ND(G, seq):

    g = deepcopy(G)
    Seq =deepcopy(seq)
    n = len(g.nodes())
    N = n  # 横坐标比例
    sigma_G = sigma_ND(g)
    #赋初值
    x = []
    y = []
    R = 1
    x.append(0)
    y.append(1)
    for i in range(1, n+1):
        attack = Seq.pop(0)
        g.remove_node(attack)
        sigma = sigma_ND(g)
        R += sigma * 1. / sigma_G
        x.append(i * 1. / N)
        y.append(sigma * 1. / sigma_G)
    return (R/(n+1)), x, y

def ANC_ND_COST(G, seq):

    g = deepcopy(G)
    Seq =deepcopy(seq)
    n = len(g.nodes())
    N = n  # 横坐标比例
    sigma_G = sigma_ND(g)
    #赋初值
    x = []
    y = []
    R = 1
    x.append(0)
    y.append(1)
    for i in range(1, n+1):
        attack = Seq.pop(0)
        g.remove_node(attack)
        sigma = sigma_ND(g)
        if sigma <= 1:
            sigma = 0
        R += sigma * 1. / sigma_G
        x.append(i * 1. / N)
        y.append(sigma * 1. / sigma_G)
    return (R/(n+1)), x, y

def ANC_ND_X(G, seq, X):

    g = deepcopy(G)
    Seq =deepcopy(seq)
    n = len(g.nodes())
    N = 1  # 横坐标比例
    sigma_G = sigma_ND(g)
    #赋初值
    x = []
    y = []
    R = 1.0
    x.append(0)
    y.append(1)
    for i in range(1, n+1):
        attack = Seq.pop(0)
        if X[i-1] == 1:
            g.remove_node(attack)
        sigma = sigma_ND(g)
        R += sigma * 1. / sigma_G
        x.append(i * 1. / N)
        y.append(sigma * 1. / sigma_G)
    return (R/(n+1))


def ANC_ND_COST_X(G, seq, X):

    g = deepcopy(G)
    Seq =deepcopy(seq)
    n = len(g.nodes())
    N = 1 # 横坐标比例
    sigma_G = sigma_ND(g)
    #赋初值
    x = []
    y = []
    R = 1
    x.append(0)
    y.append(1)
    for i in range(1, n+1):
        attack = Seq.pop(0)
        if X[i-1] == 1:
            g.remove_node(attack)
        sigma = sigma_ND(g)
        if sigma <= 1:
            sigma = 0
        R += sigma * 1. / sigma_G
        x.append(i * 1. / N)
        y.append(sigma * 1. / sigma_G)
    return (R/(n+1))
