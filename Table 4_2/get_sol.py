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

def get_sol(G, file, method):
    sol_file = 'sol/' + file + '_' + method +'_sol.txt'
    f = open(sol_file, encoding='utf-8')
    f_list = f.readlines()
    Seq = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    f.close()

    g_i = ig.Graph.from_networkx(G)
    keys = g_i.vs["_nx_name"]
    dc_i = g_i.degree()
    # dc_i = g_i.betweenness()
    dc = list_to_dict(keys, dc_i)
    dc2 = sorted(dc.items(), key=lambda x: x[1], reverse=True)
    nlist = [item[0] for item in dc2]
    Seq = Seq + [x for x in nlist if x not in Seq]

    # nlist = G.nodes
    # Seq = Seq + list(set(nlist) ^ set(Seq))

    return Seq

def main(file):

    infile = '../data/' + file+ '.gml'
    G = nx.read_gml(infile)

    # method_list = ['HDA', 'HBA', 'FINDER']
    method_list = ['BCNNS']
    for method in method_list:
        sol = get_sol(G, file, method)
        print(sol)
        # with open(f"sol/{file}_{method}_sol.txt", "w+") as f:
        #     for node in sol:
        #         line = node + '\n'
        #         f.writelines(line)

if __name__=="__main__":
    # file_list = ['Karate', 'Krebs', 'Airport', 'Crime', 'Power', 'Oregon1']
    file_list = ['Karate']
    for file in file_list:
        main(file)
