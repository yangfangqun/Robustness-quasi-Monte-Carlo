import graph_tools as gt
import networkx as nx
import numpy as np
import time
import igraph as ig
from scipy.stats import qmc
from tqdm import tqdm
import os
import concurrent.futures
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor



def Inv(G, X_list, Seq):
    res = []
    g_i = ig.Graph.from_networkx(G)
    K = len(X_list)
    for j in tqdm(range(K)):
        X = [int(i) for i in X_list[j][0:-1]]
        anc = gt.getRobustness_ND_COST_X(g_i, Seq, X)
        res.append(anc)
    return res

def Inv_parallel(K, G, X_list, Seq, num_threads):
    chunk_size = len(X_list) // num_threads
    X_list_chunks = [X_list[i:i + chunk_size] for i in range(0, len(X_list), chunk_size)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(Inv, G, X_list_chunk, Seq) for X_list_chunk in X_list_chunks]
        res = []
        for future in concurrent.futures.as_completed(futures):
            res.extend(future.result())

    return res

def run_Inv(K, G, Seq, file, method):
    # X_file = 'gen_x/' + file + '_QMC_X.txt'
    X_file = f"gen_x/{file}_{method}_X.txt"
    f = open(X_file, encoding='utf-8')
    f_list = f.readlines()
    X_list = [i for i in f_list]  # 注意有些gml文件的节点是str，有些是int

    print(f"{method}_X for {file}")
    num_threads = 10
    start = time.perf_counter()
    total_list = Inv_parallel(K, G, X_list, Seq, num_threads)
    total_time = time.perf_counter() - start
    res = []
    sum = 0
    for j in range(len(total_list)):
        sum += total_list[j]
        res.append(sum / (j + 1))

    print(f"Time for {method} of {file}: {total_time * 1000}ms")
    if not os.path.exists("res_x"):
        os.makedirs("res_x")
    with open(f"res_x/{file}_{method}_X_res.txt", "w+") as f:
        for i in res:
            line = str(i) + "\n"
            f.writelines(line)

    if not os.path.exists("res_x/time"):
        os.makedirs("res_x/time")
    with open(f"res_x/time/{file}_{method}_X_time.txt", "w+") as f:
        times = "time:" + str(total_time * 1000) + "ms"
        f.writelines(times)

#main
def main(file, K):

    infile = '../data/' + file+ '.gml'
    G = nx.read_gml(infile)

    sol_file = 'sol/' + file + '_HDA_sol.txt'
    f = open(sol_file, encoding='utf-8')
    f_list = f.readlines()
    Seq = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    f.close()

    # run_Inv(K, G, Seq, file, 'MC')
    run_Inv(K, G, Seq, file, 'QMC')
    # run_Inv(K, G, Seq, file, 'RQMC')


def process_mp(file, K):
    main(file, K)

if __name__=="__main__":
    K = 5000
    file_list = ['Crime']
    # file_list = ['Power', 'Oregon1']
    for file in file_list:
        process_mp(file, K)





