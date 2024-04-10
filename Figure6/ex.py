import graph_tools as gt
import networkx as nx
import numpy as np
import time
import igraph as ig
from scipy.stats import qmc
from tqdm import tqdm
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor

sobol = qmc.Sobol(d=3, scramble=True)
r1 = sobol.random_base2(m=3)

print(r1)

sobol = qmc.Sobol(d=3, scramble=False)
r1 = sobol.random_base2(m=3)

print(r1)












