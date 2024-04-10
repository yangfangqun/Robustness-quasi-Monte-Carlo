import graph_tools as gt
import networkx as nx
import numpy as np
import time
import igraph as ig
from scipy.stats import qmc
from tqdm import tqdm
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor



#蒙特卡洛模拟
def m_c(K, G, p_vi, Seq):
    res = []
    sum = 0
    nlist = G.nodes
    N = len(nlist)
    Seq = Seq + list(set(nlist) ^ set(Seq))
    g_i = ig.Graph.from_networkx(G)
    for j in tqdm(range(K)):
        X = []
        r = np.random.rand(N, 1)
        for i in range(N):
            if r[i] > p_vi[i]:
                X.append(0)
            else:
                X.append(1)
        sum += gt.getRobustness_ND_COST_X(g_i, Seq, X)
        # sum += gt.getRobustness_ND_COST(g_i, Seq)

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
        res.append(sum / (j + 1))
    return res


def run_mc(K, G, p_vi, Seq, file):
    print(f"MC for {file}")
    start = time.perf_counter()
    Inv_mc = m_c(K, G, p_vi, Seq)
    total_time = time.perf_counter() - start
    print(f"Time for MC of {file}: {total_time * 1000}ms")
    with open(f"res/{file}_MC_res.txt", "w+") as f:
        for i in Inv_mc:
            line = str(i) + "\n"
            f.writelines(line)
    # with open(f"res/time/{file}_MC_time.txt", "w+") as f:
    #     times = "time:" + str(total_time * 1000) + "ms"
    #     f.writelines(times)

def run_qmc(K, G, p_vi, Seq, file):
    print(f"QMC for {file}")
    start = time.perf_counter()
    Inv_qmc = q_m_c(K, G, p_vi, Seq)
    total_time = time.perf_counter() - start
    print(100*Inv_qmc[-1])
    print(f"Time for QMC of {file}: {total_time * 1000}ms")
    # with open(f"res/{file}_QMC_res.txt", "w+") as f:
    #     for i in Inv_qmc:
    #         line = str(i) + "\n"
    #         f.writelines(line)
    # with open(f"res/time/{file}_QMC_time.txt", "w+") as f:
    #     times = "time:" + str(total_time * 1000) + "ms"
    #     f.writelines(times)

#main
def main(file, K):

    infile = '../../data/' + file+ '.gml'
    G = nx.read_gml(infile)

    sol_file = 'sol/' + file + '_HDA_sol.txt'
    f = open(sol_file, encoding='utf-8')
    f_list = f.readlines()
    Seq = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    f.close()

    pv_file = 'ASR/' + file + '_ASR.txt'
    f = open(pv_file, encoding='utf-8')
    f_list = f.readlines()
    p_vi = [float(i) for i in f_list]  # 注意有些gml文件的节点是str，有些是int

    run_qmc(K, G, p_vi, Seq, file)
    # with ThreadPoolExecutor() as executor:
    #     executor.submit(run_mc, K, G, p_vi, Seq, file)
    #     executor.submit(run_qmc, K, G, p_vi, Seq, file)


def process_mp(file, K):
    main(file, K)

if __name__=="__main__":
    K = 100000
    # file_list = ['Karate']
    file_list = ['Krebs']
    process_mp('Karate', K)
    # with mp.Pool(processes=len(file_list)) as pool:
    #     pool.starmap(process_mp, [(file, K) for file in file_list])










