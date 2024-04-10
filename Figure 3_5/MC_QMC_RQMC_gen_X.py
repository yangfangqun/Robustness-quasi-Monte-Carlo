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
    N = len(p_vi)
    for j in tqdm(range(K)):
        X = ''
        r = np.random.rand(N, 1)
        for i in range(N):
            if r[i] > p_vi[i]:
                X +='0'
            else:
                X +='1'
        res.append(X)
    return res
#拟蒙特卡洛模拟
def q_m_c(K, G, p_vi, Seq):
    res = []
    N = len(p_vi)
    sobol = qmc.Sobol(d=N, scramble=False)
    R = sobol.random_base2(m=16)
    for j in tqdm(range(K)):
        X = ''
        r = R[j]
        for i in range(N):
            if r[i] > p_vi[i]:
                X += '0'
            else:
                X += '1'
        res.append(X)
    return res

#R拟蒙特卡洛模拟
def r_q_m_c(K, G, p_vi, Seq):
    res = []
    N = len(p_vi)
    sobol = qmc.Sobol(d=N, scramble=True)
    R = sobol.random_base2(m=16)
    for j in tqdm(range(K)):
        X = ''
        r = R[j]
        for i in range(N):
            if r[i] > p_vi[i]:
                X +='0'
            else:
                X +='1'
        res.append(X)
    return res

def run_mc(K, G, p_vi, Seq, file):
    print(f"MC for {file}")
    start = time.perf_counter()
    X_mc = m_c(K, G, p_vi, Seq)
    total_time = time.perf_counter() - start
    print(f"Time for MC of {file}: {total_time * 1000}ms")
    with open(f"gen_x/{file}_MC_X.txt", "w+") as f:
        for i in X_mc:
            line = str(i) + "\n"
            f.writelines(line)


def run_qmc(K, G, p_vi, Seq, file):
    print(f"QMC for {file}")
    start = time.perf_counter()
    X_qmc = q_m_c(K, G, p_vi, Seq)
    total_time = time.perf_counter() - start
    print(f"Time for QMC of {file}: {total_time * 1000}ms")
    with open(f"gen_x/{file}_QMC_X.txt", "w+") as f:
        for i in X_qmc:
            line = str(i) + "\n"
            f.writelines(line)

def run_rqmc(K, G, p_vi, Seq, file):
    print(f"QMC for {file}")
    start = time.perf_counter()
    X_rqmc = r_q_m_c(K, G, p_vi, Seq)
    total_time = time.perf_counter() - start
    print(f"Time for RQMC of {file}: {total_time * 1000}ms")
    with open(f"gen_x/{file}_RQMC_X.txt", "w+") as f:
        for i in X_rqmc:
            line = str(i) + "\n"
            f.writelines(line)

#main
def main(file, K):

    infile = '../data/' + file+ '.gml'
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

    # run_mc(K, G, p_vi, Seq, file)
    run_qmc(K, G, p_vi, Seq, file)
    # run_rqmc(K, G, p_vi, Seq, file)



def process_mp(file, K):
    main(file, K)

if __name__=="__main__":
    K = 5000
    # file_list = ['Airport', 'Crime', 'Power', 'Oregon1']
    file_list = ['Crime']
    # file_list = ['Power', 'Oregon1']
    with mp.Pool(processes=len(file_list)) as pool:
        pool.starmap(process_mp, [(file, K) for file in file_list])










