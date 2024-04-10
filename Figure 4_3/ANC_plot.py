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

    fig, ax = plt.subplots(figsize=(8, 6))
    K = len(HDA_y)
    x = [i / (1 + K) for i in range(K)]
    if net_name == 'Karate':
        mkevery = 1
        ax.set_xlim([-0.005, 0.55])  # 设置x轴范围
        ax.set_ylim([-0.05, 1.15])  # 设置y轴范围
    elif net_name == 'Krebs':
        mkevery = 2
        ax.set_xlim([-0.005, 0.55])  # 设置x轴范围
        ax.set_ylim([-0.05, 1.15])  # 设置y轴范围
    elif net_name == 'Airport':
        mkevery = 10
        ax.set_xlim([-0.005, 0.55])  # 设置x轴范围
        ax.set_ylim([-0.05, 1.15])  # 设置y轴范围
    elif net_name == 'Crime':
        mkevery = 20
        ax.set_xlim([-0.005, 0.44])  # 设置x轴范围
        ax.set_ylim([-0.05, 1.15])  # 设置y轴范围
    elif net_name == 'Power':
        mkevery = 60
        ax.set_xlim([-0.005, 0.33])  # 设置x轴范围
        ax.set_ylim([-0.05, 1.15])  # 设置y轴范围
    elif net_name == 'Oregon1':
        mkevery = 80
        ax.set_xlim([-0.005, 0.18])  # 设置x轴范围
        ax.set_ylim([-0.05, 1.15])  # 设置y轴范围
    ax.plot(x, HDA_y, color='#4E0E2E', marker='*', markersize=mksize, markevery=mkevery, linewidth=line_w, label='HDA')
    ax.plot(x, HBA_y, color='#005995', marker='v', markersize=mksize, markevery=mkevery, linewidth=line_w, label='HBA')
    ax.plot(x, FINDER_y, color='#fa625f', marker='o', markersize=mksize, markevery=mkevery, linewidth=line_w, label='FINDER')
    ax.plot(x, BCNNS_y, color='#9dd3a8', marker='s', markersize=mksize, markevery=mkevery, linewidth=line_w, label='$\mathrm{HB_{nns}AGP}$')
    ax.plot(x, RF_y, color='#FFCC00', marker='^', markersize=mksize, markevery=mkevery, linewidth=line_w,
            label='RF')


    # # 创建第二个子图
    # ax2 = ax.inset_axes([0.4, 0.15, 0.5, 0.35])
    # # ax2 = ax.inset_axes([0.55, 0.15, 0.4, 0.35])  #Oregon1
    # # 在第二个子图中绘制所需的数据
    # ax2.plot(x, HDA_y, color='#005995', linewidth=line_w1)
    # ax2.plot(x, HBA_y, color='#fa625f', linewidth=line_w1)
    # ax2.plot(x, FINDER_y, color='#3d3d3b', linewidth=line_w1)
    # ax2.plot(x, BCNNS_y, color='#8bc24c',  linewidth=line_w1)
    # ax2.set_xlim([0.0, 1.01])  # 设置x轴范围
    #
    # ax2.tick_params(axis='x', labelsize=TickSize-5)
    # ax2.tick_params(axis='y', labelsize=TickSize-5)
    #
    # ax2.set_ylim([-0.005, 0.05])  # 设置y轴范围 Airport Crime
    # # ax2.set_ylim([-0.001, 0.01])  # 设置y轴范围 Power
    # # ax2.set_ylim([-0.0005, 0.0025])  # 设置y轴范围 Oregon1
    # ax2.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
    # # 将第二个子图添加到主图中
    # ax.indicate_inset_zoom(ax2)

    # # 创建第三个子图
    # # ax3 = ax.inset_axes([0.4, 0.2, 0.5, 0.35])
    # ax3 = ax.inset_axes([0.16, 0.4, 0.2, 0.55])  # Oregon1
    # # 在第二个子图中绘制所需的数据
    # ax3.plot(x, HDA_y, color='#005995', linewidth=line_w1)
    # ax3.plot(x, HBA_y, color='#fa625f', linewidth=line_w1)
    # ax3.plot(x, FINDER_y, color='#3d3d3b', linewidth=line_w1)
    # ax3.plot(x, BCNNS_y, color='#8bc24c', linewidth=line_w1)
    # ax3.set_xlim([0.01, 0.04])  # 设置x轴范围
    #
    # ax3.tick_params(axis='x', labelsize=TickSize - 5)
    # ax3.tick_params(axis='y', labelsize=TickSize - 5)
    #
    # # ax3.set_ylim([-0.005, 0.05])  # 设置y轴范围 Airport Crime
    # # ax3.set_ylim([-0.001, 0.01])  # 设置y轴范围 Power
    # ax3.set_ylim([-0.0005, 0.3])  # 设置y轴范围 Oregon1
    # ax3.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
    # # 将第二个子图添加到主图中
    # ax.indicate_inset_zoom(ax3)

    ax.legend(loc='upper right', fontsize=LegendSize)

    ax.set_ylabel('GCC size of residual network', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize - 2)
    ax.set_xlabel('Fraction of attacked nodes', fontweight='bold', fontsize=LabelSize)

    # xline = float(format(Inv_qmc[-1], '.2f'))
    # ax.set_ylim([xline - 0.02, xline + 0.02])
    # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    # fig.tight_layout()
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
        
    # if net_name == 'Karate':
    #     fig.savefig('anc_plot/fig8a.eps', bbox_inches='tight')
    # elif net_name == 'Krebs':
    #     fig.savefig('anc_plot/fig8b.eps', bbox_inches='tight')
    # elif net_name == 'Airport':
    #     fig.savefig('anc_plot/fig8c.eps', bbox_inches='tight')
    # elif net_name == 'Crime':
    #     fig.savefig('anc_plot/fig8d.eps', bbox_inches='tight')
    # elif net_name == 'Power':
    #     fig.savefig('anc_plot/fig8e.eps', bbox_inches='tight')
    # elif net_name == 'Oregon1':
    #     fig.savefig('anc_plot/fig8f.eps', bbox_inches='tight')

    # fig.savefig('anc_plot/%s.png' % net_name, bbox_inches='tight')


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
    # net_list = ['Karate']
    # net_list = ['Karate', 'Krebs']
    # net_list = ['Airport']
    # net_list = ['Crime']
    # net_list = ['Power']
    net_list = ['Karate', 'Krebs', 'Airport', 'Power', 'Crime', 'Oregon1']
    for net in net_list:
        main(net)

