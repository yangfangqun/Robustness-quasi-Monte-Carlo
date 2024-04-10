#并行抽样

import graph_tools as gt
import networkx as nx
import time
from scipy.stats import qmc
from tqdm import tqdm
import multiprocessing as mp
import igraph as ig


def q_m_c(K):
    res = []

    for j in tqdm(range(K)):
        r = sobol.random(1)[0]
        X = []
        for i in range(N):
            if r[i] > p_vi[i]:
                X.append(0)
            else:
                X.append(1)
        res.append(gt.getRobustness_ND_COST_X(g_i, Seq, X))
    return res


def estimate_p(n, num_processes=5):
    print("num_processes=", num_processes)
    part_count = [n // num_processes] * num_processes
    for i in range(n % num_processes):
        part_count[i] += 1
    pool = mp.Pool(processes=num_processes)
    count_li = pool.map(q_m_c, part_count)
    pool.close()
    res = []
    total_list = []
    for li in count_li:
        total_list += li
    sum = 0
    for j in range(len(total_list)):
        sum += total_list[j]
        res.append(sum/(j+1))
    return res, num_processes



# ['Karate', 'Krebs', 'Airport', 'Crime', 'Power', 'Oregon1']
file = 'Karate'
print(file)
infile = '../../data/' + file + '.gml'
G = nx.read_gml(infile)
N = nx.number_of_nodes(G)
g_i = ig.Graph.from_networkx(G)
sol_file = 'sol/' + file + '_HDA_sol.txt'
f = open(sol_file, encoding='utf-8')
f_list = f.readlines()
Seq = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
nlist = G.nodes
Seq = Seq + list(set(nlist) ^ set(Seq))
f.close()

pv_file = 'ASR3/' + file + '_ASR.txt'
f = open(pv_file, encoding='utf-8')
f_list = f.readlines()
p_vi = [float(i) for i in f_list] # 注意有些gml文件的节点是str，有些是int
f.close()

sobol = qmc.Sobol(N)

if __name__=="__main__":
    K = 5000
    print("PQMC")
    start = time.perf_counter()
    Inv_pqmc, num = estimate_p(K)
    total_time = time.perf_counter() - start
    print("time:", total_time * 1000, "ms")
    print(sum(Inv_pqmc)/len(Inv_pqmc))
    # f = open('res/' + file + '_PQMC_res.txt', 'w+')
    # for i in Inv_pqmc:
    #     line = str(i) + '\n'
    #     f.writelines(line)
    # f.close()
    # #time
    # f = open('res/time/' + file + '_PQMC_time.txt', 'w+')
    # num_of_p = 'num_of_p: ' + str(num) + '\n'
    # times ='time:' + str(total_time*1000) + 'ms'
    # f.writelines(num_of_p)
    # f.writelines(times)
    # f.close()



