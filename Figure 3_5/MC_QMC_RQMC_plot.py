import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

TickSize = 20
LabelSize = 28
Labelpad = 5
LegendSize = 24
line_w = 1.5
mksize = 10
mkevery = (500, 500)
def cruve_plot(Inv_mc, Inv_qmc, Inv_pqmc, net_name):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600

    fig, ax = plt.subplots(figsize=(8, 6))
    K = len(Inv_mc)
    x = [i for i in range(K)]

    ax.plot(x, Inv_mc, color='#005995', linewidth=line_w, label='MC', marker='v', markersize=mksize, markevery=mkevery)
    ax.plot(x, Inv_qmc, color='#fa625f', linewidth=line_w, label='QMC', marker='o', markersize=mksize, markevery=mkevery)
    ax.plot(x, Inv_pqmc, color='#9dd3a8', linewidth=line_w, label='PRQMC', marker='s', markersize=mksize, markevery=mkevery)
    ax.legend(loc='upper right', fontsize=LegendSize)

    ax.set_ylabel('$\widehat R$ of the network', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('Sampling iterations $(K)$', fontweight='bold', fontsize=LabelSize)

    if net_name == 'Airport':
        ax.set_ylim([0.395, 0.405])
    elif net_name == 'Crime':
        ax.set_ylim([0.310, 0.330])
    elif net_name == 'Power':
        ax.set_ylim([0.085, 0.091])
    elif net_name == 'Oregon1':
        ax.set_ylim([0.260, 0.280])
    # ax.set_ylim([0.18, 0.195]) #Power
    # ax.set_ylim([0.34, 0.365]) #Oregon1
    # xline = float(format(Inv_qmc[-1], '.2f'))
    # ax.set_ylim([xline - 0.02, xline + 0.02])
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    # fig.tight_layout()
    plt.close()
    if net_name == 'Airport':
        fig.savefig('result_plot/fig6a.png', bbox_inches='tight')
    elif net_name == 'Crime':
        fig.savefig('result_plot/fig6b.png', bbox_inches='tight')
    elif net_name == 'Power':
        fig.savefig('result_plot/fig6c.png', bbox_inches='tight')
    elif net_name == 'Oregon1':
        fig.savefig('result_plot/fig6d.png', bbox_inches='tight')
    # fig.savefig('result_plot/%s.png' % net_name, bbox_inches='tight')

def std_plot(Inv_mc, Inv_qmc, Inv_pqmc, net_name):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600


    fig, ax = plt.subplots(figsize=(8, 6))

    std_mc = [np.std(Inv_mc[:i+1]) for i in range(1, len(Inv_mc))]
    std_qmc = [np.std(Inv_qmc[:i+1]) for i in range(1, len(Inv_qmc))]
    std_pqmc = [np.std(Inv_pqmc[:i+1]) for i in range(1,len(Inv_pqmc))]

    ax.plot(std_mc[1:], color='#005995', linewidth=line_w, label='MC', marker='v', markersize=mksize, markevery=mkevery)
    ax.plot(std_qmc[1:], color='#fa625f', linewidth=line_w, label='QMC', marker='o', markersize=mksize, markevery=mkevery)
    ax.plot(std_pqmc[1:], color='#9dd3a8', linewidth=line_w, label='PRQMC', marker='s', markersize=mksize, markevery=mkevery)
    ax.legend(loc='upper right', fontsize=LegendSize)
    if net_name == 'Airport':
        ax.set_ylim([0, 0.01])
    elif net_name == 'Crime':
        ax.set_ylim([0, 0.01])
    elif net_name == 'Power':
        ax.set_ylim([0, 0.002])
    elif net_name == 'Oregon1':
        ax.set_ylim([0, 0.02])
    # ax.set_ylim([-0.0001, 0.01])  # Oregon1
    # ax.set_xscale('log')
    # ax.set_yscale('log')

    ax.set_ylabel('Standard deviation', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('Sampling iterations $(K)$', fontweight='bold', fontsize=LabelSize)

    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    # fig.tight_layout()
    plt.close()
    if net_name == 'Airport':
        fig.savefig('result_plot/fig6e.png', bbox_inches='tight')
    elif net_name == 'Crime':
        fig.savefig('result_plot/fig6f.png', bbox_inches='tight')
    elif net_name == 'Power':
        fig.savefig('result_plot/fig6g.png', bbox_inches='tight')
    elif net_name == 'Oregon1':
        fig.savefig('result_plot/fig6h.png', bbox_inches='tight')
    # fig.savefig('result_plot/%s_std.png' % net_name, bbox_inches='tight')

def main(net_name):
    res_MC = 'res_x/' + net_name + '_MC_X_res.txt'
    f = open(res_MC, encoding='utf-8')
    f_list = f.readlines()
    Inv_mc = [float(i) for i in f_list]
    f.close()

    res_QMC = 'res_x/' + net_name + '_QMC_X_res.txt'
    f = open(res_QMC, encoding='utf-8')
    f_list = f.readlines()
    Inv_qmc = [float(i) for i in f_list]
    f.close()

    res_RQMC = 'res_x/' + net_name + '_RQMC_X_res.txt'
    f = open(res_RQMC, encoding='utf-8')
    f_list = f.readlines()
    Inv_rqmc = [float(i) for i in f_list]
    f.close()

    cruve_plot(Inv_mc, Inv_qmc, Inv_rqmc, net_name)
    std_plot(Inv_mc, Inv_qmc, Inv_rqmc, net_name)


if __name__=="__main__":
    net_list = [ 'Airport', 'Crime', 'Power', 'Oregon1']
    # net_list = ['Airport']
    # net_list = ['Crime']
    # net_list = ['Power']
    # net_list = ['Oregon1']
    for net in net_list:
        main(net)

