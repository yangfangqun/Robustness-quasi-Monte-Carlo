import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

TickSize = 20
LabelSize = 28
Labelpad = 5
LegendSize = 18
line_w = 2
mksize = 10
mkevery = 50
def anc_plot(net_name, HDA_y, HBA_y, BCNNS_y, FINDER_y, RF_y):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600

    K = 16
    HDA_y = HDA_y[0:K]
    HBA_y = HBA_y[0:K]
    FINDER_y = FINDER_y[0:K]
    BCNNS_y = BCNNS_y[0:K]
    RF_y = RF_y[0:K]
    fig, ax = plt.subplots(figsize=(8, 6))
    K = len(HDA_y)
    x = [i for i in range(K)]
    mkevery = 1

    ax.xaxis.set_major_locator(mtick.MaxNLocator(integer=True))

    if net_name == 'Karate':
        ax.set_ylim([-0.3, 1.02])  # 设置y轴范围
    elif net_name == 'Krebs':
        ax.set_ylim([0.00, 1.02])  # 设置y轴范围
    elif net_name == 'Airport':
        ax.set_ylim([0.63, 1.015])  # 设置y轴范围
    elif net_name == 'Crime':
        ax.set_ylim([0.94, 1.01])  # 设置y轴范围
    elif net_name == 'Power':
        ax.set_ylim([0.7, 1.02])  # 设置y轴范围
    elif net_name == 'Oregon1':
        ax.set_ylim([0.66, 1.02])  # 设置y轴范围

    ax.plot(x, HDA_y, color='#4E0E2E', marker='*', markersize=mksize, markevery=mkevery, linewidth=line_w, label='HDA')
    ax.plot(x, HBA_y, color='#005995', marker='v', markersize=mksize, markevery=mkevery, linewidth=line_w, label='HBA')
    ax.plot(x, FINDER_y, color='#fa625f', marker='o', markersize=mksize, markevery=mkevery, linewidth=line_w, label='FINDER')
    ax.plot(x, BCNNS_y, color='#9dd3a8', marker='s', markersize=mksize, markevery=mkevery, linewidth=line_w, label='$\mathrm{HB_{nns}AGP}$')
    ax.plot(x, RF_y, color='#FFCC00', marker='^', markersize=mksize, markevery=mkevery, linewidth=line_w,
            label='RF')


    ax.legend(loc='lower left', fontsize=LegendSize)
    ax.set_ylabel('GCC size of residual network', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize - 2)
    ax.set_xlabel('Number of attacked nodes', fontweight='bold', fontsize=LabelSize)

    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)

    plt.close()
    if net_name == 'Karate':
        fig.savefig('anc_plot/fig8a.png', bbox_inches='tight')
    elif net_name == 'Krebs':
        fig.savefig('anc_plot/fig8b.png', bbox_inches='tight')
    elif net_name == 'Airport':
        fig.savefig('anc_plot/fig8c.png', bbox_inches='tight')
    elif net_name == 'Crime':
        fig.savefig('anc_plot/fig8d.png', bbox_inches='tight')
    elif net_name == 'Power':
        fig.savefig('anc_plot/fig8e.png', bbox_inches='tight')
    elif net_name == 'Oregon1':
        fig.savefig('anc_plot/fig8f.png', bbox_inches='tight')



def main(net_name):
    res_HDA = 'res/' + net_name + '_HDA_y.txt'
    f = open(res_HDA, encoding='utf-8')
    f_list = f.readlines()
    HDA_y = [float(i) for i in f_list]
    f.close()

    res_HBA = 'res/' + net_name + '_HBA_y.txt'
    f = open(res_HBA, encoding='utf-8')
    f_list = f.readlines()
    HBA_y = [float(i) for i in f_list]
    f.close()

    res_BCNNS = 'res/' + net_name + '_BCNNS_y.txt'
    f = open(res_BCNNS, encoding='utf-8')
    f_list = f.readlines()
    BCNNS_y = [float(i) for i in f_list]
    f.close()

    res_FINDER = 'res/' + net_name + '_FINDER_y.txt'
    f = open(res_FINDER, encoding='utf-8')
    f_list = f.readlines()
    FINDER_y = [float(i) for i in f_list]
    f.close()

    res_RF = 'res/' + net_name + '_RF_y.txt'
    f = open(res_RF, encoding='utf-8')
    f_list = f.readlines()
    RF_y = [float(i) for i in f_list]
    f.close()

    anc_plot(net_name, HDA_y, HBA_y, BCNNS_y, FINDER_y, RF_y)


if __name__ == "__main__":
    net_list = ['Karate', 'Krebs', 'Airport', 'Power', 'Crime', 'Oregon1']
    for net in net_list:
        main(net)

