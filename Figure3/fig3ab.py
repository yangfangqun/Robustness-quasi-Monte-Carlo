import numpy as np
from scipy.stats import qmc
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import *
#

# some settings for the plot
matplotlib.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
# matplotlib.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman'})
plt.rcParams['figure.dpi'] = 600
sns.set(context='paper', style='ticks')

TickSize = 20
LabelSize = 28
Labelpad = 5
Linewidth = 4


# # 生成Sobol点列
num_points = 2048
dim = 2
sobol = qmc.Sobol(dim)
sobol_points = sobol.random(num_points)


# 绘制散点图  2维
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(sobol_points[:,0], sobol_points[:,1], c='#35A9D4', marker='o')
# ax.set_title("Low-discrepancy Sequences", fontweight='bold', fontsize=LabelSize)
ax.set_xlim(-0.01, 1.01)
ax.set_ylim(-0.01, 1.01)
ax.set_xlabel("${{y}_{1}}$",fontweight='bold', fontsize=LabelSize)
ax.set_ylabel("${{y}_{2}}$",fontweight='bold', fontsize=LabelSize,rotation=0)
ax.tick_params(axis='x', labelsize=TickSize)
ax.tick_params(axis='y', labelsize=TickSize)
fig.savefig('fig3b.png',bbox_inches='tight')
#
#
#
#均匀分布
random_points = np.random.rand(num_points, dim)  # 生成1000个随机均匀分布的点
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(random_points[:,0], random_points[:,1], c='#9dd3a8', marker='o')
# ax.set_title("Pseudo-random Sequences", fontweight='bold', fontsize=LabelSize)
ax.set_xlim(-0.01, 1.01)
ax.set_ylim(-0.01, 1.01)
ax.set_xlabel("${{x}_{1}}$",fontweight='bold', fontsize=LabelSize)
ax.set_ylabel("${{x}_{2}}$",fontweight='bold', fontsize=LabelSize,rotation=0)
ax.tick_params(axis='x', labelsize=TickSize)
ax.tick_params(axis='y', labelsize=TickSize)
fig.savefig('fig3a.png',bbox_inches='tight')
