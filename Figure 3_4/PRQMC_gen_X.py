import graph_tools as gt
import networkx as nx
import numpy as np
import time
import igraph as ig
from scipy.stats import qmc
from tqdm import tqdm
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor

#拟蒙特卡洛模拟
def q_m_c(K, G, p_vi, Seq):
    res = []
    N = len(p_vi)
    sobol = qmc.Sobol(N)
    for j in tqdm(range(K)):
        X = ''
        r = sobol.random(1)[0]
        for i in range(N):
            if r[i] > p_vi[i]:
                X +='0'
            else:
                X +='1'
        res.append(X)
    return res

def run_qmc(method, K, G, p_vi, Seq, file, ASR):
    print(f"QMC for {file}")
    start = time.perf_counter()
    X_qmc = q_m_c(K, G, p_vi, Seq)
    total_time = time.perf_counter() - start
    print(f"Time for QMC of {file}: {total_time * 1000}ms")
    with open(f"gen_x_{ASR}/{file}_{method}_PRQMC_X.txt", "w+") as f:
        for i in X_qmc:
            line = str(i) + "\n"
            f.writelines(line)


#main
def main(file, K):

    infile = '../data/' + file+ '.gml'
    G = nx.read_gml(infile)



    method_list = ['HDA']
    ASR_list = ['ASR']
    for ASR in ASR_list:
        pv_file = ASR + '/' + file + '_ASR.txt'
        f = open(pv_file, encoding='utf-8')
        f_list = f.readlines()
        p_vi = [float(i) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
        for method in method_list:
            sol_file = 'sol/' + file + '_' + method + '_sol.txt'
            f = open(sol_file, encoding='utf-8')
            f_list = f.readlines()
            Seq = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
            f.close()
            nlist = G.nodes
            # Seq = Seq + list(set(nlist) ^ set(Seq))
            run_qmc(method, K, G, p_vi, Seq, file, ASR)

def process_mp(file, K):
    main(file, K)

if __name__=="__main__":
    K = 10000
    # file_list = ['Karate', 'Krebs', 'Airport', 'Crime', 'Power', 'Oregon1']
    file_list = ['Krebs']
    # file_list = ['Karate']

    with mp.Pool(processes=len(file_list)) as pool:
        pool.starmap(process_mp, [(file, K) for file in file_list])










