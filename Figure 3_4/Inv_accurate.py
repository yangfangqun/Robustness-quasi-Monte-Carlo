import networkx as nx
import itertools
import numpy as np
import time
import graph_tools as gt
from random import randint, sample
import igraph as ig
from scipy.stats import qmc
from tqdm import tqdm
import multiprocessing as mp

def P_sum(X, p_vi, N):
    """
    计算攻击序列状态为X时的概率
    """
    p = 1
    for i in range(N):
        if X[i] == 1:
            p *= p_vi[i]
        else:
            p *= 1-p_vi[i]
        if p == 0:
            break
    return p

def generate_vectors(n):
    """
    生成n维的01向量，并覆盖所有情况
    """
    # 创建一个包含n个0和1的元组
    items = itertools.product([0, 1], repeat=n)

    # 将元组转换为列表并返回结果
    return [list(item) for item in items]

if __name__=="__main__":

    # file = 'Karate'
    file = 'Krebs'
    infile = '../../data/' + file + '.gml'
    G = nx.read_gml(infile)
    N = G.number_of_nodes()
    g_i = ig.Graph.from_networkx(G)

    sol_file = 'sol/' + file + '_HDA_sol.txt'
    f = open(sol_file, encoding='utf-8')
    f_list = f.readlines()
    Seq = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    f.close()

    pv_file = 'ASR/' + file + '_ASR.txt'
    f = open(pv_file, encoding='utf-8')
    f_list = f.readlines()
    p_vi = [float(i) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    print(p_vi)

    ind = []  #ASR不为1的节点下标
    for index, value in enumerate(p_vi):
        if value != 1:
            ind.append(index)
    anc = 0
    X_full = [1 for i in range(N)]
    for X in tqdm(generate_vectors(len(ind))):
        for i in range(len(X)):
            X_full[ind[i]] = X[i]
        P_X = P_sum(X_full, p_vi, N)
        anc += gt.getRobustness_ND_COST_X(g_i, Seq, X_full)*P_X
    print(anc*100)
