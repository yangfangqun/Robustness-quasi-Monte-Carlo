import graph_tools as gt
import networkx as nx
import time
import numpy as np
import igraph as ig
from tqdm import tqdm
import concurrent.futures
import random


def list_to_dict(li_keys, li_values):
    dic = zip(li_keys, li_values)
    return dict(dic)


def q_m_c(g_i, X_list, Seq):
    res = []
    K = len(X_list)
    for j in tqdm(range(K)):
        X = [int(i) for i in X_list[j][0:-1]]
        anc = gt.getRobustness_ND_COST_X(g_i, Seq, X)
        res.append(anc)
    return res

def q_m_c_parallel(K, g_i, X_list, Seq, num_threads):
    chunk_size = len(X_list) // num_threads
    X_list_chunks = [X_list[i:i + chunk_size] for i in range(0, len(X_list), chunk_size)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(q_m_c, g_i, X_list_chunk, Seq) for X_list_chunk in X_list_chunks]
        res = []
        for future in concurrent.futures.as_completed(futures):
            res.extend(future.result())

    return res

def run_qmc(K, G, method, ASR, file):

    sol_file = 'sol/' + file + '_' + method +'_sol.txt'
    f = open(sol_file, encoding='utf-8')
    f_list = f.readlines()
    Seq = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    f.close()

    g_i = ig.Graph.from_networkx(G)

    X_file = 'gen_x_' + ASR + '/' + file + '_' + method + '_PRQMC_X.txt'
    f = open(X_file, encoding='utf-8')
    f_list = f.readlines()
    X_list = [i for i in f_list]  # 注意有些gml文件的节点是str，有些是int

    print(f"QMC_X for {file}")
#####################  进程数  #####################
    num_threads = 150
    start = time.perf_counter()
    total_list = q_m_c_parallel(K, g_i, X_list, Seq, num_threads)
    total_time = time.perf_counter() - start
    res = []
    sum = 0
    for j in range(len(total_list)):
        sum += total_list[j]
        res.append(sum / (j + 1))

    run_time = f"Time for MC of {file}: {total_time * 1000}ms\n"
    print(run_time)


    with open(f"res_x_{ASR}/{file}_{ASR}_{method}_PRQMC_X_res.txt", "w+") as f:
        inv = res[-1]*100
        line = file + '_' + ASR + '_' + method +':' + str(inv) + "\n"
        print( line)
        f.writelines(line)
        f.writelines(run_time)

#main
def main(file, K):

    infile = '../data/' + file+ '.gml'
    G = nx.read_gml(infile)

    method_list = ['HDA', 'HBA', 'FINDER', 'BCNNS', 'RF']
    ASR_list = ['ASR5020', 'ASR5010']
    for ASR in ASR_list:
        for method in method_list:
            run_qmc(K, G, method, ASR, file)


def process_mp(file, K):
    main(file, K)

if __name__=="__main__":
    K = 5000
    file_list = ['Karate', 'Krebs', 'Airport', 'Crime', 'Power', 'Oregon1']
    # file_list = ['Karate', 'Krebs', 'Airport']
    for file in file_list:
        main(file, K)