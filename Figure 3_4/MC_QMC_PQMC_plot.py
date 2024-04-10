import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import FuncFormatter

TickSize = 20
LabelSize = 28
Labelpad = 5
LegendSize = 24
line_w = 1.5
mksize = 10
mkevery = (1000, 1000)
mkeverylog = 0.8
def should_mark(x):
    return np.isclose(np.log10(x) % 1, 0)

def comma_format(x, pos):
    return '{:,}'.format(int(x)) if len(str(int(x))) >= 5 else int(x)




def cruve_plot(Inv_mc, Inv_qmc, Inv_pqmc, net_name):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600

    fig, ax = plt.subplots(figsize=(8, 6))
    K = len(Inv_mc)
    x = [i for i in range(K)]

    formatter = FuncFormatter(comma_format)
    ax.xaxis.set_major_formatter(formatter)

    ax.plot(x, Inv_mc, color='#005995', linewidth=line_w, label='MC', marker='v', markersize=mksize, markevery=mkevery)
    ax.plot(x, Inv_qmc, color='#fa625f', linewidth=line_w, label='QMC', marker='o', markersize=mksize, markevery=mkevery)
    ax.plot(x, Inv_pqmc, color='#9dd3a8', linewidth=line_w, label='PRQMC', marker='s', markersize=mksize, markevery=mkevery)



    if net_name == 'Karate':
        Inv_Karate = 46.308057270915725
        plt.axhline(y=Inv_Karate / 100, color='#4E0E2E', linewidth=line_w, linestyle='--', label='$RASR$')
        ax.set_ylim([0.459, 0.469])  # Karate
    else:
        Inv_Krebs = 23.071802215142593
        plt.axhline(y=Inv_Krebs / 100, color='#4E0E2E', linewidth=line_w, linestyle='--', label='$RASR$')
        ax.set_ylim([0.228, 0.235])  # Krebs
    ax.legend(loc='upper right', fontsize=LegendSize)

    ax.set_ylabel('$\widehat R$ of the network', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('Sampling iterations $(K)$', fontweight='bold', fontsize=LabelSize)



    # xline = float(format(Inv_qmc[-1], '.2f'))
    # ax.set_ylim([xline - 0.02, xline + 0.02])
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    # fig.tight_layout()
    plt.close()
    fig.savefig('result_plot/%s.eps' % net_name, bbox_inches='tight')

def err_plot(Inv_mc, Inv_qmc, Inv_pqmc, net_name):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600


    fig, ax = plt.subplots(figsize=(8, 6))
    K = len(Inv_mc)
    x = [i for i in range(K)]
    if net_name == 'Karate':
        Inv_acc = 46.308057270915725   #Karate
    else:
        Inv_acc = 23.071802215142593  #Krebs

    error_mc = [0 for i in range(K)]
    error_qmc = [0 for i in range(K)]
    error_pqmc = [0 for i in range(K)]

    for i in range(K):
        error_mc[i] = abs(Inv_mc[i] - Inv_acc/100)
        error_qmc[i] = abs(Inv_qmc[i] - Inv_acc/100)
        error_pqmc[i] = abs(Inv_pqmc[i] - Inv_acc/100)

    ax.set_ylim([1e-8, 1e+3])
    # ax.set_xlim([1e+0, 1e+4])
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(error_mc, color='#005995', linewidth=line_w, label='MC', marker='v', markersize=mksize, markevery=mkeverylog)
    ax.plot(error_qmc, color='#fa625f', linewidth=line_w, label='QMC', marker='o', markersize=mksize, markevery=mkeverylog)
    ax.plot(error_pqmc, color='#9dd3a8', linewidth=line_w, label='PRQMC', marker='s', markersize=mksize, markevery=mkeverylog)
    ax.legend(loc='upper right', fontsize=LegendSize)



    ax.set_ylabel('Error of $\widehat R$', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('Sampling iterations $(K)$', fontweight='bold', fontsize=LabelSize)

    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    # fig.tight_layout()
    plt.close()
    fig.savefig('result_plot/%s_err.eps' % net_name, bbox_inches='tight')


def main(net_name):
    res_MC = 'res/' + net_name + '_MC_res.txt'
    f = open(res_MC, encoding='utf-8')
    f_list = f.readlines()
    Inv_mc = [float(i) for i in f_list]
    f.close()

    res_QMC = 'res/' + net_name + '_QMC_res.txt'
    f = open(res_QMC, encoding='utf-8')
    f_list = f.readlines()
    Inv_qmc = [float(i) for i in f_list]
    f.close()

    res_PQMC = 'res/' + net_name + '_PRQMC_res.txt'
    f = open(res_PQMC, encoding='utf-8')
    f_list = f.readlines()
    Inv_pqmc = [float(i) for i in f_list]
    f.close()

    pv_file = 'ASR/' + net_name + '_ASR.txt'
    f = open(pv_file, encoding='utf-8')
    f_list = f.readlines()
    p_vi = [float(i) for i in f_list]  # 注意有些gml文件的节点是str，有些是int
    f.close()

    cruve_plot(Inv_mc, Inv_qmc, Inv_pqmc, net_name)
    err_plot(Inv_mc, Inv_qmc, Inv_pqmc, net_name)
    # ASR_plot(p_vi, net_name)


if __name__=="__main__":
    # net_list = ['Karate']
    net_list = ['Karate', 'Krebs']
    for net in net_list:
        main(net)

