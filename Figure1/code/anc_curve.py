import networkx as nx
from pylab import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
plt.rcParams['figure.dpi'] = 600
# sns.set(context='paper', style='ticks')

TickSize = 20
LabelSize = 28
Labelpad = 5
LegendSize = 24
line_w = 2
mksize = 10
mkevery = 50

def sigma_ND(G):
    if len(G.nodes()) == 0:
        return 0
    sigma = len(max(nx.connected_components(G), key=len))
    return sigma

def getRobustness_ND_COST_X(g, sol,X):
    nlist = g.nodes
    sol = sol + list(set(nlist) ^ set(sol))
    N = nx.number_of_nodes(g)
    Robust = [0 / N for i in range(N + 1)]
    Robust[0] = 1
    Robust[N] = 0  # 最后一个节点
    g_copy = g.copy()
    for i in range(len(sol)):
        #考虑到生存率的情况，要攻击到最后一个节点
        if X[i] == 1:
            g_copy.remove_node(sol[i])
        sigma = sigma_ND(g_copy)
        if sigma <= 1:
            sigma = 0
            break
        robust = sigma / N
        Robust[i+1] = robust
    return sum(Robust)/(N+1)

data_test = '../data/Karate.txt'
g_test = nx.read_edgelist(data_test)
g = nx.Graph()
for edge in g_test.edges():
    g.add_edge(int(edge[0]), int(edge[1]))

def getRobustness_ND_COST_X(g, sol,X):
    nlist = g.nodes
    sol = sol + list(set(nlist) ^ set(sol))
    N = nx.number_of_nodes(g)
    Robust = [0 / N for i in range(N + 1)]
    Robust[0] = 1
    Robust[N] = 0  # 最后一个节点
    g_copy = g.copy()
    for i in range(len(sol)):
        #考虑到生存率的情况，要攻击到最后一个节点
        if X[i] == 1:
            g_copy.remove_node(sol[i])
        sigma = sigma_ND(g_copy)
        if sigma <= 1:
            sigma = 0
            break
        robust = sigma / N
        Robust[i+1] = robust
    return Robust
sol = [0, 33, 32, 2, 1, 23, 5, 24, 3, 6, 31, 4, 30, 29]
##########注意在这里修改不同的情况哈
X = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# X = [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0]
x = [0, 0.029411764705882353, 0.058823529411764705, 0.08823529411764706, 0.11764705882352941, 0.14705882352941177, 0.17647058823529413, 0.20588235294117646, 0.23529411764705882, 0.2647058823529412, 0.29411764705882354, 0.3235294117647059, 0.35294117647058826, 0.38235294117647056, 0.4117647058823529, 0.4411764705882353, 0.47058823529411764, 0.5, 0.5294117647058824, 0.5588235294117647, 0.5882352941176471, 0.6176470588235294, 0.6470588235294118, 0.6764705882352942, 0.7058823529411765, 0.7352941176470589, 0.7647058823529411, 0.7941176470588235, 0.8235294117647058, 0.8529411764705882, 0.8823529411764706, 0.9117647058823529, 0.9411764705882353, 0.9705882352941176, 1.0]
y = getRobustness_ND_COST_X(g,sol, X)



fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x,y,color='k', marker='o', linestyle='-', label='FINDER')
# ax.set_ylabel('GCC size of residual network',labelpad = Labelpad, fontweight='bold', fontsize=LabelSize)
ax.set_ylabel('GCC size of residual network',labelpad = Labelpad, fontweight='bold', fontsize=LabelSize-2)
ax.set_xlabel('Fraction of attacked nodes', fontweight='bold', fontsize=LabelSize)
# ax.set_title('ANC Curve', fontweight='bold',fontsize=LabelSize)
# ax.text(0.95, 0.95, "ASR: 100%",
#             transform=ax.transAxes,
#             horizontalalignment='right',
#             verticalalignment='top',
#             fontweight='bold', fontsize=28)
ax.set_xlim([-0.05,1.05])
ax.set_ylim([-0.05,1.05])

xmajorLocator = MultipleLocator(0.1) #将x主刻度标签设置为0.05的倍数
xmajorFormatter = FormatStrFormatter('%.1f') #设置x轴标签文本的格式
ax.xaxis.set_major_locator(xmajorLocator)
ax.xaxis.set_major_formatter(xmajorFormatter)

ymajorLocator = MultipleLocator(0.2) #将y轴主刻度标签设置为0.5的倍数
ymajorFormatter = FormatStrFormatter('%.1f') #设置y轴标签文本的格式
ax.yaxis.set_major_locator(ymajorLocator)
ax.yaxis.set_major_formatter(ymajorFormatter)

ax.tick_params(axis='x', labelsize=TickSize)
ax.tick_params(axis='y', labelsize=TickSize)
# fig.tight_layout()
plt.close()
fig.savefig('../result/ANC_Curve.png' , bbox_inches='tight')
# fig.savefig('../result/ANC_Curve.png')

