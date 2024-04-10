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


def FINDER_method(G):
    result_file = 'Finder_result/' + filename + '_FINDER_sol.txt'
    f = open(result_file, encoding='utf-8')
    f_list = f.readlines()
    sol = [str(int(i)) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    return sol

def main(data):
    ## 读文件
    global filename, nodes_keys
    filename = data
    ##

    infile = '../../data/' + filename + '.gml'
    G0 = nx.read_gml(infile)
    nodes_keys = list(G0.nodes)
    print(filename)
    sol_FINGER = FINDER_method(G0)
    print(gt.getRobustness_ND_COST(G0, sol_FINGER))
    print(len(sol_FINGER))


if __name__=="__main__":
    print('Finder')
    # netlist = ['Karate', 'Krebs', 'Airport', 'Crime', 'Power']
    netlist = ['Oregon1']
    for net in netlist:
        data = net
        main(data)
