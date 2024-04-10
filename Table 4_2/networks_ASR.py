
import networkx as nx
import numpy as np
import random


file_list = ['Karate', 'Krebs', 'Airport', 'Crime', 'Power', 'Oregon1']
# file_list = ['Karate']
# file_list = ['Krebs']
# file_list = ['Airport']
# file_list = ['Crime']
# file_list = ['Power']
# file_list = ['Oregon1']
for file in file_list:
    filename = data = file
    infile = '../data/' + data + '.gml'
    G = nx.read_gml(infile)
    N = nx.number_of_nodes(G)
    nlist = G.nodes

#     # 初始概率100%
#     p_vi = [1 for i in range(N)]
#     f = open('ASR1/' + filename + '_ASR.txt', 'w+')
#     for p in p_vi:
#         line = str(p) + '\n'
#         f.writelines(line)
#     f.close()
#### ASR=90%  ASR2
    p_vi = [0.9 for i in range(N)]
    f = open('ASR90/' + filename + '_ASR.txt', 'w+')
    for p in p_vi:
        line = str(p) + '\n'
        f.writelines(line)
    f.close()

#### ASR=80%  ASR2
    p_vi = [0.8 for i in range(N)]
    f = open('ASR80/' + filename + '_ASR.txt', 'w+')
    for p in p_vi:
        line = str(p) + '\n'
        f.writelines(line)
    f.close()

# #### ASR=70%  ASR2
#     p_vi = [0.7 for i in range(N)]
#     f = open('ASR2/' + filename + '_ASR.txt', 'w+')
#     for p in p_vi:
#         line = str(p) + '\n'
#         f.writelines(line)
#     f.close()

#### ASR=60%  ASR2
    p_vi = [0.6 for i in range(N)]
    f = open('ASR60/' + filename + '_ASR.txt', 'w+')
    for p in p_vi:
        line = str(p) + '\n'
        f.writelines(line)
    f.close()

# #### ASR=70%  ASR2
#     p_vi = [0.7 for i in range(N)]
#     f = open('ASR2/' + filename + '_ASR.txt', 'w+')
#     for p in p_vi:
#         line = str(p) + '\n'
#         f.writelines(line)
#     f.close()
#
# #### ASR=50%  ASR3
#     p_vi = [0.5 for i in range(N)]
#     f = open('ASR3/' + filename + '_ASR.txt', 'w+')
#     for p in p_vi:
#         line = str(p) + '\n'
#         f.writelines(line)
#     f.close()

# #### ASR=random 100%-50%  ASR4-5-6-7-8
#     # ASR_list = ['ASR4', 'ASR5', 'ASR6', 'ASR7', 'ASR8']
#     ASR_list = ['ASR11', 'ASR12', 'ASR13', 'ASR14', 'ASR15']
#     for ASR in ASR_list:
#         p_vi = [random.uniform(0.5, 1) for i in range(N)]
#         f = open(f"{ASR}/{filename}_ASR.txt", 'w+')
#         for p in p_vi:
#             line = str(p) + '\n'
#             f.writelines(line)
#         f.close()

# #### ASR=random 30%增强0.5
#     ASR_list = ['ASR11A']
#     a = 0.3
#     p_vi = [1 for i in range(N)]
#     for ASR in ASR_list:
#         for i in range(int(N*a)):
#             p_vi[i] = 0.7
#         f = open(f"{ASR}/{filename}_ASR.txt", 'w+')
#         for p in p_vi:
#             line = str(p) + '\n'
#             f.writelines(line)
#         f.close()
