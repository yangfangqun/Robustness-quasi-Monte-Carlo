import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import igraph as ig
from tqdm import tqdm

def getRobustness_ND_COST(g, sol):
    # igraph 优化版
    g_i = ig.Graph.from_networkx(g)
    N = g_i.vcount()
    Robust = [0 for i in  range(N+1)]
    Robust[0] = 1
    Robust[N] = 0  # 最后一个节点
    for i in tqdm(range(len(sol)-1)):
        keys = g_i.vs["_nx_name"]
        g_i.delete_vertices(keys.index(sol[i]))
        gcc = max(g_i.connected_components(), key=len)
        robust = len(gcc) / N
        Robust[i+1] = robust
    return Robust

def main(net_name):
    infile = '../../data/' + net_name + '.gml'
    G = nx.read_gml(infile)

    HDA_sol_file = 'sol/' + net_name + '_HDA_sol.txt'
    f = open(HDA_sol_file, encoding='utf-8')
    f_list = f.readlines()
    HDA_sol = [str(int(i)) for i in f_list]
    f.close()
    y_HDA = getRobustness_ND_COST(G, HDA_sol)

    with open(f"res/{net_name}_HDA_y.txt", "w+") as f:
        for y in y_HDA:
            line = str(y) + '\n'
            f.writelines(line)

    HBA_sol_file = 'sol/' + net_name + '_HBA_sol.txt'
    f = open(HBA_sol_file, encoding='utf-8')
    f_list = f.readlines()
    HBA_sol = [str(int(i)) for i in f_list]
    f.close()
    y_HBA = getRobustness_ND_COST(G, HBA_sol)
    with open(f"res/{net_name}_HBA_y.txt", "w+") as f:
        for y in y_HBA:
            line = str(y) + '\n'
            f.writelines(line)

    BCNNS_sol_file = 'sol/' + net_name + '_BCNNS_sol.txt'
    f = open(BCNNS_sol_file, encoding='utf-8')
    f_list = f.readlines()
    BCNNS_sol = [str(int(i)) for i in f_list]
    f.close()
    y_BCNNS = getRobustness_ND_COST(G, BCNNS_sol)
    with open(f"res/{net_name}_BCNNS_y.txt", "w+") as f:
        for y in y_BCNNS:
            line = str(y) + '\n'
            f.writelines(line)

    FINDER_sol_file = 'sol/' + net_name + '_FINDER_sol.txt'
    f = open(FINDER_sol_file, encoding='utf-8')
    f_list = f.readlines()
    FINDER_sol = [str(int(i)) for i in f_list]
    f.close()
    y_FINDER = getRobustness_ND_COST(G, FINDER_sol)
    with open(f"res/{net_name}_FINDER_y.txt", "w+") as f:
        for y in y_FINDER:
            line = str(y) + '\n'
            f.writelines(line)
    



if __name__=="__main__":
    # net_list = ['Karate', 'Krebs', 'Airport', 'Crime', 'Power', 'HEP']
    net_list = ['Oregon1']
    for net in net_list:
        main(net)

