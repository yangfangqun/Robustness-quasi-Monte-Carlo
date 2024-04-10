import graph_tools as gt
import networkx as nx
import time
import numpy as np
import igraph as ig
from tqdm import tqdm
import concurrent.futures
import random

if __name__=="__main__":
    K = 5000
    file_list = ['Karate', 'Krebs', 'Airport', 'Crime', 'Power', 'Oregon1']
    # file_list = ['Karate', 'Krebs', 'Airport', 'Crime']
    # file_list = ['Power']
    # file_list = ['Power', 'Oregon1']
    method_list = ['BCNNS', 'FINDER', 'HBA', 'HDA']
    # ASR_list = ['ASR11', 'ASR12', 'ASR13', 'ASR14', 'ASR15']
    ASR_list = ['ASR2', 'ASR3', 'ASR4', 'ASR5', 'ASR6', 'ASR7', 'ASR8', 'ASR11', 'ASR12', 'ASR13', 'ASR14', 'ASR15', 'ASR10A', 'ASR11A']
    for file in file_list:
        for ASR in ASR_list:
            for method in method_list:
                res_file = f"res_x_{ASR}/{file}_{ASR}_{method}_PRQMC_X_res.txt"
                f = open(res_file, encoding='utf-8')
                res = f.readline()

                # with open(f"res_x_{ASR}/1{ASR}.txt", "w+") as f:
                #     line = ''
                #     f.writelines(line)

                with open(f"res_x_{ASR}/1{ASR}.txt", "a+") as f:
                    line = str(res)
                    f.writelines(line)













