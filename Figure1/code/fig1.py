import networkx as nx
from pylab import *
import matplotlib.pyplot as plt
import seaborn as sns

# %%

# some settings for the plot
matplotlib.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
# matplotlib.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman'})
plt.rcParams['figure.dpi'] = 600
sns.set(context='paper', style='ticks')

TickSize = 16
LabelSize = 26
LegendSize = 26
Labelpad = 5
Linewidth = 4


# %%

def getRobustness(g, sol, method):
    N = nx.number_of_nodes(g)
    Robust = [1]
    norm = N * (N - 1) / 2
    g_copy = g.copy()
    for i in range(len(sol) - 1):
        g_copy.remove_node(sol[i])
        if method == 'ND':
            # Gc = max(nx.connected_component_subgraphs(g_copy), key=len)
            Gc = max((g_copy.subgraph(c).copy() for c in nx.connected_components(g_copy)), key=len)
            max(nx.connected_components(g_copy), key=len)
            robust = nx.number_of_nodes(Gc) / N
        elif method == 'CN':
            # cc = nx.connected_component_subgraphs(g_copy)
            cc = (g_copy.subgraph(c).copy() for c in nx.connected_components(g_copy))
            temp = 0.0
            for c in cc:
                n_c = nx.number_of_nodes(c)
                temp += n_c * (n_c - 1) / 2
                #             robust = 1 - temp / norm
                robust = temp / norm
        Robust.append(robust)
    return Robust


# %%

POS_Krebs = {1: array([-0.13033296,  0.18121866]),
       0: array([-0.09213573,  0.3189762 ]),
       2: array([0.03846213, 0.00168518]),
       3: array([0.06254739, 0.32132908]),
       4: array([0.24347195, 0.56256292]),
       5: array([-0.00161817,  0.69721706]),
       6: array([-0.12589489,  0.66010392]),
       7: array([0.23491005, 0.3008854 ]),
       8: array([0.24254945, 0.04382462]),
       9: array([ 0.42123996, -0.09135411]),
       10: array([0.13099712, 0.61528691]),
       11: array([-0.44778234,  0.50588426]),
       12: array([-0.25473148,  0.54444701]),
       13: array([0.14540399, 0.09482382]),
       16: array([-0.06120889,  0.7       ]),
       17: array([-0.40206669,  0.36398989]),
       19: array([-0.1043576 , -0.01279791]),
       21: array([-0.45764906,  0.25771448]),
       25: array([-0.54850725, -0.21852988]),
       23: array([-0.21280995, -0.51012007]),
       24: array([-0.51502031, -0.34983654]),
       27: array([-0.22379016, -0.2927742 ]),
       28: array([-0.10543277, -0.28840598]),
       29: array([-0.0496048 , -0.60181414]),
       26: array([ 0.04165249, -0.74139791]),
       30: array([ 0.2191024 , -0.11283862]),
       31: array([-0.21195628, -0.10012434]),
       32: array([ 0.18095692, -0.32750248]),
       14: array([ 0.17260745, -0.63642364]),
       15: array([ 0.30459533, -0.60758958]),
       18: array([ 0.40808028, -0.52689824]),
       20: array([ 0.4787308 , -0.42165879]),
       22: array([ 0.51597788, -0.30529592]),
       33: array([ 0.10361376, -0.32458708])}

# %%

method = 'CN'  # 'CN'

data_test = '../data/Karate.txt'
g_test = nx.read_edgelist(data_test)
g = nx.Graph()
for edge in g_test.edges():
    g.add_edge(int(edge[0]), int(edge[1]))

nodes = g.nodes()
NodeNum = nx.number_of_nodes(g)
g_copy = g.copy()
g_DQN = g.copy()

### read sol file

if method == 'CN':
    sol = [0, 33, 32, 2, 1, 23, 5, 24, 3, 6, 31, 4, 30, 29]
elif method == 'ND':
    sol = [0, 33, 32, 2, 1, 23, 5, 24, 3, 6, 31, 4, 30, 29]

sol_all = sol + list(set(nodes) ^ set(sol))
sol = sol_all[:len(sol) + 1]
# sol = sol_all
### draw single png
DQN_Robust = getRobustness(g_DQN, sol, method)

# ######### plot robust curve graph
# fig, ax = plt.subplots(figsize=(8, 6))
# x_DQN_robust = [i / NodeNum for i in range(len(sol))]
# y_DQN_robust = DQN_Robust[:len(sol)]
#
# ax.plot(x_DQN_robust, y_DQN_robust, color='black', marker='o', linestyle='-', label='FINDER')
# ax.set_ylabel('Residual %s Connectivity' % method, labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
# ax.set_xlabel('Fraction of Key-players', fontweight='bold', fontsize=LabelSize)
# ax.set_title('ANC Curve - %s' % method, fontweight='bold', fontsize=28)
#
# ax.set_xlim([-0.05, 0.6])
# ax.set_ylim([-0.05, 1.05])
#
# xmajorLocator = MultipleLocator(0.1)  # 将x主刻度标签设置为0.05的倍数
# xmajorFormatter = FormatStrFormatter('%.1f')  # 设置x轴标签文本的格式
# ax.xaxis.set_major_locator(xmajorLocator)
# ax.xaxis.set_major_formatter(xmajorFormatter)
#
# ymajorLocator = MultipleLocator(0.2)  # 将y轴主刻度标签设置为0.5的倍数
# ymajorFormatter = FormatStrFormatter('%.1f')  # 设置y轴标签文本的格式
# ax.yaxis.set_major_locator(ymajorLocator)
# ax.yaxis.set_major_formatter(ymajorFormatter)
#
# ax.tick_params(axis='x', labelsize=TickSize)
# ax.tick_params(axis='y', labelsize=TickSize)
# # ax.legend(loc='upper right', bbox_to_anchor=(1, 0.88), fontsize=LabelSize)
# plt.close()
# fig.savefig('../result/%s/ANC_%s.png' % (method, method), bbox_inches='tight')
# # fig.savefig('./result/%s/ANC_%s.pdf'%(method, method), bbox_inches='tight')


######### plot snapshot
NodeScale = 500
MaxNodeSize = 1000
MinNodeSize = 200
Nodesize_all = dict(nx.degree(g_copy))
for node in Nodesize_all.keys():
    temp = np.log10(Nodesize_all[node]) * NodeScale
    if temp < MinNodeSize:
        temp = MinNodeSize
    Nodesize_all[node] = temp
Nodesize_all_list = [Nodesize_all[item] for item in g_copy.nodes()]
##########注意在这里修改不同的情况哈
# X = [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0]
X = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Sol = []
fail = []
Nodesize_fail = []

# flagx = True
for i in range(len(sol) - 1):
# for i in range(1):
    #     print ('Iter:%d'%i)
    fig, ax = plt.subplots(figsize=(8, 6))
    G = g.copy()
    Pos = POS_Krebs.copy()
    Node_size = Nodesize_all.copy()

    G1 = g.copy()
    Pos1 = POS_Krebs.copy()
    Node_size1 = Nodesize_all.copy()


    # if flagx == True:
    #     NodeSize_list = [Node_size[item] for item in G.nodes()]
    #     nx.draw_networkx(G1, pos=Pos, with_labels=False, node_color='#2E94B9', node_size=NodeSize_list,
    #                      nodelist=list(G1.nodes()), edgelist=list(G1.edges()), width=2)
    #     plt.xticks([])
    #     plt.yticks([])
    #     plt.close()
    #     # fig.savefig('../result/%s/%d.png' % (method, i), bbox_inches='tight')
    #     method = 'ND'
    #     # fig.savefig('../result/%s/%d.eps' % (method, i), bbox_inches='tight')
    #     fig.savefig('../result/%s/%d.png' % (method, 0), bbox_inches='tight')
    #     flagx = False

    attack = sol[:i+1]
    for node in attack:
        G1.remove_node(node)
        del Pos1[node]
        del Node_size1[node]
    NodeSize_list1 = [Node_size1[item] for item in G1.nodes()]
    Nodesize_Sol_list1 = [Nodesize_all[item] for item in attack]
    if X[i] == 1:
        Sol.append(sol[i])
    else:
        fail.append(sol[i])
        Nodesize_fail.append((Nodesize_all[sol[i]]))
    for node in Sol:
        G.remove_node(node)
        del Pos[node]
        del Node_size[node]
    NodeSize_list = [Node_size[item] for item in G.nodes()]
    Nodesize_Sol_list = [Nodesize_all[item] for item in Sol]

    #攻击成功的节点
    nx.draw_networkx(g, pos=POS_Krebs, with_labels=False, node_color='silver', node_size=Nodesize_Sol_list,
                     nodelist=Sol, edgelist=list(g.edges()), width=1, edge_color='silver', style='dashed')
    #剩余的节点
    nx.draw_networkx(G1, pos=Pos, with_labels=False, node_color='#2E94B9', node_size=NodeSize_list1,
                         nodelist=list(G1.nodes()), edgelist=list(G1.edges()), width=2)
    #攻击失败的节点
    nx.draw_networkx(G, pos=Pos, with_labels=False, node_color='#9dd3a8',node_size=Nodesize_fail,
                             nodelist=fail, width=2)


    # ax.set_title('Network with 34 nodes', pad=Labelpad, fontsize=LabelSize)
    # ax.set_title('Network with 34 nodes', fontweight='bold', fontsize=LabelSize)
    # ax.set_title('%.1f%% of the nodes are attacked' % (100*(i+1)/34),fontweight='bold', fontsize=LabelSize)
    # ax.set_title('%.1f%% of the nodes are attacked' % (100*(i+1)/34),pad=Labelpad, fontweight='bold', fontsize=LabelSize)
    # fig.tight_layout()
    # ax.text(0.98, 0.98, "ASR: 60%",
    #         transform=ax.transAxes,
    #         horizontalalignment='right',
    #         verticalalignment='top',
    #         fontweight='bold', fontsize=28)
    plt.xticks([])
    plt.yticks([])
    plt.close()
    # fig.savefig('../result/%s/%d.png' % (method, i), bbox_inches='tight')
    method = 'ND'
    # fig.savefig('../result/%s/%d.eps' % (method, i), bbox_inches='tight')
    fig.savefig('../result/%s/%d.png' % (method, i+1), bbox_inches='tight')

print('Closed!')