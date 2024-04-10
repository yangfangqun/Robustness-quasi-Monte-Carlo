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



# # Karate
# data = 'Karate'
# Seq = ['33', '0', '32', '1', '2', '3', '5', '25', '4', '23', '24', '6', '8', '28', '29', '19', '20', '12', '13', '22', '17', '31', '21', '11', '16', '26', '27', '9', '14', '10', '15', '18', '30', '7']
# N = 34

# Krebs
data = 'Krebs'
Seq = ['1', '11', '7', '5', '22', '14', '49', '12', '15', '20', '2', '27', '29', '6', '19', '28', '40', '30', '43', '23', '24', '32', '45', '52', '3', '10', '25', '33', '47', '53', '54', '56', '36', '46', '37', '26', '57', '61', '34', '31', '41', '38', '18', '17', '42', '16', '55', '50', '35', '13', '51', '59', '39', '48', '58', '44', '0', '8', '60', '21', '4', '9']
N = 62


#初始概率
p_vi = [1 for i in range(N)]
#重要节点加强
for i in range(int(N*0.2)):
    p_vi[i] -= 0.2
# 随机节点加强
# index_A = [i for i in range(N)]
# S = sample(index_A, int(N*0.2))
# for i in S:
#     p_vi[i] -= 0.1

# 随机节点统一概率
# Karate
# p_vi = [1, 1, 0.8, 1, 1, 1, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 1, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 0.8]
# # Krebs
# p_vi = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

def P_sum(X):
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

    infile = '../data/' + data + '.gml'
    G = nx.read_gml(infile)
    print(p_vi)
    ind = []
    for index, value in enumerate(p_vi):
        if value != 1:
            ind.append(index)
    anc = 0
    X_full = [1 for i in range(N)]
    for X in tqdm(generate_vectors(int(N*0.2))):
        for i in range(len(X)):
            X_full[ind[i]] = X[i]
        P_X = P_sum(X_full)
        anc += gt.getRobustness_ND_COST_X(G, Seq, X_full)*P_X
    print(anc*100)
