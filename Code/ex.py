import networkx as nx
import numpy as np
import time
import graph_tools as gt
import matplotlib.pyplot as plt
from random import randint, sample
import igraph as ig
from scipy.stats import qmc
from tqdm import tqdm
import multiprocessing as mp


n=782
num_processes = 6
part_count = [n // num_processes] * num_processes
for i in range(n % num_processes):
    part_count[i] += 1
print(part_count)


for i in V:
   Gcc = max(nx.connected_components(), key = len)