import networkx as nx
import numpy as np
import time
import graph_tools as gt
import igraph as ig
from tqdm import tqdm
import random
import matplotlib.pyplot as plt
from random import randint, sample
import os

def HXA(g, method):
    sol = []
    g_i = ig.Graph.from_networkx(g)
    while (g_i.ecount()>0):  #当边为0时，只剩下孤立节点，不计入sol
        keys = g_i.vs["_nx_name"]
        if method == 'HDA':
            values = g_i.degree()
        elif method == 'HBA':
            values = g_i.betweenness() # best method
        elif method == 'HCA':
            values = g_i.closeness()
        maxTag = np.argmax(values)
        node = keys[maxTag]
        sol.append(node)
        g_i.delete_vertices(maxTag)
    return sol
def HXA_method(G, method):
    print(method + ': ')
    sol = HXA(G, method)
    return sol

def HBA(g_i):
    print('HBA:')
    sol = []
    total_edges = g_i.ecount()
    while (g_i.ecount()>0):  #当边为0时，只剩下孤立节点，不计入sol
        keys = g_i.vs["_nx_name"]
        values = g_i.betweenness()
        maxTag = np.argmax(values)
        node = keys[maxTag]
        sol.append(node)
        g_i.delete_vertices(maxTag)
        processed_edges = total_edges - g_i.ecount()
        print(f"\rProcessed edges: {processed_edges}/{total_edges} ({processed_edges / total_edges:.2%})", end='')
    return sol

def HDA(g_i):
    print('HDA:')
    sol = []

    total_edges = g_i.ecount()
    while (g_i.ecount()>0):  #当边为0时，只剩下孤立节点，不计入sol
        keys = g_i.vs["_nx_name"]
        values = g_i.degree()
        maxTag = np.argmax(values)
        node = keys[maxTag]
        sol.append(node)
        g_i.delete_vertices(maxTag)
        processed_edges = total_edges - g_i.ecount()
        print(f"\rProcessed edges: {processed_edges}/{total_edges} ({processed_edges / total_edges:.2%})", end='')
    return sol


def run_HBA(G, file):
    g_i = ig.Graph.from_networkx(G)
    N = g_i.vcount()
    start = time.perf_counter()
    sol = HBA(g_i)
    total_time = time.perf_counter() - start
    print("HBA_time:", total_time * 1000, "ms")
    print('len_HBA_sol: ', len(sol))
    with open(f"sol/{file}_HBA_sol.txt", "w+") as f:
        for node in sol:
            line = node + '\n'
            f.writelines(line)

    start = time.perf_counter()
    ANC = gt.getRobustness_ND_COST(G, sol)
    total_time1 = time.perf_counter() - start
    print("ANC_HBA_time:", total_time1 * 1000, "ms")
    print(ANC)
    with open(f"sol/{file}_HBA_inf.txt", "w+") as f:
        filename = "network: " + file + '\n'
        times = "time: " + str(total_time * 1000) + "ms"+ '\n'
        len_sol = "len_sol: " + str(len(sol))+ '\n'
        num_nodes = "Num of nodes: " + str(N) + '\n'
        anc = "ANC: " + str(ANC)+ '\n'
        f.writelines("HBA:\n")
        f.writelines(filename)
        f.writelines(times)
        f.writelines(len_sol)
        f.writelines(num_nodes)
        f.writelines(anc)

def run_HDA(G, file):
    g_i = ig.Graph.from_networkx(G)
    N = g_i.vcount()
    start = time.perf_counter()
    sol = HDA(g_i)
    total_time = time.perf_counter() - start
    print("HDA_time:", total_time * 1000, "ms")
    print('len_HDA_sol: ', len(sol))
    # with open(f"sol/{file}_HDA_sol.txt", "w+") as f:
    #     for node in sol:
    #         line = node + '\n'
    #         f.writelines(line)

    start = time.perf_counter()
    ANC = gt.getRobustness_ND_COST(G, sol)
    total_time1 = time.perf_counter() - start
    print("ANC_HDA_time:", total_time1 * 1000, "ms")
    print(ANC)
    # with open(f"sol/{file}_HDA_inf.txt", "w+") as f:
    #     filename = "network: " + file + '\n'
    #     times = "time: " + str(total_time * 1000) + "ms"+ '\n'
    #     len_sol = "len_sol: " + str(len(sol))+ '\n'
    #     num_nodes = "Num of nodes: "+ str(N) + '\n'
    #     anc = "ANC: " + str(ANC)+ '\n'
    #     f.writelines("HDA:\n")
    #     f.writelines(filename)
    #     f.writelines(times)
    #     f.writelines(len_sol)
    #     f.writelines(num_nodes)
    #     f.writelines(anc)

def main(data):
    ## 读文件
    global filename, nodes_keys
    filename = data
    ##
    infile = '../../data/' + filename + '.gml'
    G0 = nx.read_gml(infile)
    print(filename)
    run_HDA(G0, filename)
    run_HBA(G0, filename)






if __name__=="__main__":
    print('HXA')
    # netlist = ['Karate', 'Krebs', 'Airport', 'Crime', 'Power', 'HEP']
    # netlist = ['Karate', 'Krebs']
    netlist = ['Oregon1']
    for net in netlist:
        data = net
        main(data)
