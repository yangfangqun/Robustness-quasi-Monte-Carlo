import networkx as nx
import numpy as np
import time
import graph_tools as gt
import matplotlib.pyplot as plt
from random import randint, sample
import igraph as ig
from scipy.stats import qmc
from tqdm import tqdm
from scipy.optimize import curve_fit
import multiprocessing as mp

#蒙特卡洛模拟
def m_c(K, G, p_vi, Seq):
    res = []
    sum = 0
    N = len(G.nodes)
    for j in tqdm(range(K)):
        X = []
        r = np.random.rand(N, 1)
        for i in range(N):
            if r[i] > p_vi[i]:
                X.append(0)
            else:
                X.append(1)
        sum += gt.getRobustness_ND_COST_X(G, Seq, X)
        res.append(sum / (j + 1))
    return res
#拟蒙特卡洛模拟
def q_m_c(K, G, p_vi, Seq):
    res = []
    sum = 0
    nlist = G.nodes
    N = len(nlist)
    sobol = qmc.Sobol(N)
    Seq = Seq + list(set(nlist) ^ set(Seq))
    g_i = ig.Graph.from_networkx(G)
    for j in tqdm(range(K)):
        X = []
        r = sobol.random(1)[0]
        for i in range(N):
            if r[i] > p_vi[i]:
                X.append(0)
            else:
                X.append(1)
        sum += gt.getRobustness_ND_COST_X(g_i, Seq, X)
        res.append(sum/(j+1))
    return res


data = 'Karate'
infile = '../../data/' + data + '.gml'
G = nx.read_gml(infile)
N = nx.number_of_nodes(G)
print('N = ', N)

# # Karate
Seq = ['33', '0', '32', '1', '2', '3', '5', '25', '4', '23', '24', '6', '8', '28', '29', '19', '20', '12', '13', '22', '17', '31', '21', '11', '16', '26', '27', '9', '14', '10', '15', '18', '30', '7']
# Krebs
# Seq = ['1', '11', '7', '5', '22', '14', '49', '12', '15', '20', '2', '27', '29', '6', '19', '28', '40', '30', '43', '23', '24', '32', '45', '52', '3', '10', '25', '33', '47', '53', '54', '56', '36', '46', '37', '26', '57', '61', '34', '31', '41', '38', '18', '17', '42', '16', '55', '50', '35', '13', '51', '59', '39', '48', '58', '44', '0', '8', '60', '21', '4', '9']

# # 初始概率
p_vi = [1 for i in range(N)]
# # 重要节点加强
# for i in range(int(N)):
#     p_vi[i] -= 0.5
#随机节点加强
# index_A = [i for i in range(N)]
# S = sample(index_A, int(N*0.2))
# for i in S:
#     p_vi[i] -= 0.1

# 随机节点统一概率
# Karate
# p_vi = [1, 1, 0.8, 1, 1, 1, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 1, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 0.8]
# Krebs
# p_vi = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]# Airport


if __name__=="__main__":

    print(p_vi)

    g = ig.Graph.from_networkx(G)
    X = [0 for i in range(N)]
    # for i in range(N):
    #     if i%2 == 0:
    #         X[i] = 0
    # sol = ['33', '0', '32', '1', '2', '3', '5', '25', '4', '23', '24', '6', '8', '28', '29']
    # n = len(sol)
    for i in range(15):
        X[i] = 1
    anc = gt.getRobustness_ND_COST_X(g, Seq, X)

    print('X: ', X)
    print('anc: ', anc)

    K = 100


    # print("MC")
    # start = time.perf_counter()
    # Inv = m_c(K, G, p_vi, Seq)
    # total_time = time.perf_counter() - start
    # print("time:", total_time * 1000, "ms")
    # print(Inv*100)

    # print("MC")
    # start = time.perf_counter()
    # Inv_mc = m_c(K, G, p_vi, Seq)
    # total_time = time.perf_counter() - start
    # print("time:", total_time * 1000, "ms")

    print("QMC")
    start = time.perf_counter()
    Inv_qmc = q_m_c(K, G, p_vi, Seq)
    total_time = time.perf_counter() - start
    print("time:", total_time * 1000, "ms")
    print(Inv_qmc[-1])


    #
    # plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    # plt.rcParams['figure.dpi'] = 400
    # TickSize = 11
    # LabelSize = 26
    # Labelpad = 5
    # LegendSize = 18
    # # Linewidth = 4
    #
    # fig, ax = plt.subplots()
    #
    # Inv_Karate = 19.003697478991587
    # Inv_Krebs = 28.239039643933246
    # x = [i for i in range(K)]
    #
    # ax.plot(x, Inv_mc, color='#005995',linewidth=0.8,label='MC')
    # ax.plot(x, Inv_qmc, color='#fa625f', linewidth=0.8, label='QMC')
    # # plt.axhline(y=Inv_Karate/100, color='#4E0E2E', linewidth=0.7, linestyle='-', label='Accurate Inv')
    # plt.axhline(y=Inv_Krebs / 100, color='#4E0E2E', linewidth=0.7, linestyle='-', label='Accurate Inv')
    #
    #
    # ax.legend(loc='upper right', fontsize=LegendSize)
    #
    # ax.set_ylabel('Inv of the network', labelpad=Labelpad,fontweight='bold', fontsize=LabelSize)
    # ax.set_xlabel('Sampling iterations $(K)$', fontweight='bold', fontsize=LabelSize)
    # # ax.set_ylim([0.16, 0.22]) #Karate
    # ax.set_ylim([0.26, 0.32]) #Krebs
    # ax.tick_params(axis='x', labelsize=TickSize)
    # ax.tick_params(axis='y', labelsize=TickSize)
    # # fig.tight_layout()
    # plt.close()
    # fig.savefig('%s.png' % data, bbox_inches='tight')
    #
    # fig, ax = plt.subplots()
    # error1 = [0 for i in range(K)]
    # error2 = [0 for i in range(K)]
    #
    # # for i in range(K):
    # #     error1[i] = abs(Inv_mc[i] - Inv_Karate/100)
    # #     error2[i] = abs(Inv_qmc[i] - Inv_Karate/100)
    # for i in range(K):
    #     error1[i] = abs(Inv_mc[i] - Inv_Krebs/100)
    #     error2[i] = abs(Inv_qmc[i] - Inv_Krebs/100)
    #
    # # popt, pcov = curve_fit(fit_line, x, error1)
    # # ax.plot(x, fit_line(x, *popt), color='k', linewidth=0.8)
    # #
    # # popt, pcov = curve_fit(fit_line, x, error2)
    # # ax.plot(x, fit_line(x, *popt), color='r', linewidth=0.8)
    #
    #
    # ax.plot(x, error1, color='#005995', linewidth=0.8, label='MC')
    # ax.plot(x, error2, color='#fa625f', linewidth=0.8, label='QMC')
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    # ax.set_ylim([1e-8, 1e+1])  # Karate
    #
    # ax.legend(loc='upper right', fontsize=LegendSize)
    #
    # ax.set_ylabel('Error of Inv', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    # ax.set_xlabel('Sampling iterations $(K)$', fontweight='bold', fontsize=LabelSize)
    # # ax.tick_params(axis='x', labelsize=TickSize)
    # # ax.tick_params(axis='y', labelsize=TickSize)
    # # fig.tight_layout()
    # plt.close()
    # fig.savefig('%s_Error.png' % data, bbox_inches='tight')
