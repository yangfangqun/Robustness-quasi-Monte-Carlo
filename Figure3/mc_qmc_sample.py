import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.stats import qmc
import math

import matplotlib.ticker as mtick


def f(x):
    # if x < 0.4:
    #     return 1.2
    # else:
    #     return 0.7
    return  math.sin(x*2*math.pi)+1.2

linew = 5
ylim = 2.5


def mc_plot(K):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600
    TickSize = 20
    LabelSize = 28
    Labelpad = 5
    LegendSize = 18

    fig, ax = plt.subplots(figsize=(8, 6))

    x = np.linspace(0, 1, 1000)
    y = [f(xi) for xi in x]
    ax.plot(x, y, color='#13334c', linewidth=linew)

    ax.set_xlim([0, 1])
    ax.set_ylim([0,ylim])

    # X = np.random.rand(K)
    # print(list(X))
    X = [0.8549579863383322, 0.2640597329680492, 0.026114309863991658, 0.7144648667382216, 0.7973363674797649, 0.9309054351102595, 0.21157021764963246, 0.6582736986522908, 0.07059938812565048, 0.03591307114501374, 0.6251305927960652, 0.03638507493848098, 0.5074904590045506, 0.22419232135863287, 0.7182183956514077, 0.10372358850421703, 0.6089097253503591, 0.46216179509191346, 0.3814376674397305, 0.7468675235265505, 0.7507210926806857, 0.10424340173843871, 0.17600811811193529, 0.6731691128812382, 0.2666341533090587, 0.43799316864051496, 0.25209227078542973, 0.4965742387256459, 0.1291903477569457, 0.29354718132961866]

    for xi in X:
        yi = f(xi)
        ax.bar(xi, yi, width=1/K, color='#9dd3a8', edgecolor='black')
        ax.vlines(xi, ymin=0, ymax=yi, color='black', linestyle='dashed', linewidth=1.0)

    ax.set_ylabel('$f(X)$', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('$X$', fontweight='bold', fontsize=LabelSize)
    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    # ax.bar(0.6, f(0.6), width=1 / K, alpha=1, color='#369cbf', edgecolor='black')
    # ax.text(0.82, 0.88, r"$f(X_i),X_i=0.6$",
    #         transform=ax.transAxes,
    #         horizontalalignment='right',
    #         verticalalignment='top',
    #         fontweight='bold', fontsize=14)
    ax.text(0.95, 0.95, "$K=30$",
            transform=ax.transAxes,
            horizontalalignment='right',
            verticalalignment='top',
            fontweight='bold', fontsize=30)
    # ax.text(0.61, -0.08, r'$\frac{1}{K}$',
    #         transform=ax.transAxes,
    #         horizontalalignment='right',
    #         verticalalignment='top',
    #         fontweight='bold', fontsize=16)
    fig.tight_layout()
    plt.grid(True)
    plt.close()
    fig.savefig('fig3c.png', bbox_inches='tight')

def mc_sample_plot(K):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600
    TickSize = 20
    LabelSize = 28
    Labelpad = 5
    LegendSize = 18

    fig, ax = plt.subplots(figsize=(8, 6))

    x = np.linspace(0, 1, 1000)
    y = [f(xi) for xi in x]
    ax.plot(x, y, color='#13334c', linewidth=linew)

    ax.set_xlim([0, 1])
    ax.set_ylim([0, ylim])

    X = [0.8549579863383322, 0.2640597329680492, 0.026114309863991658, 0.7144648667382216, 0.7973363674797649,
         0.9309054351102595, 0.21157021764963246, 0.6582736986522908, 0.07059938812565048, 0.03591307114501374,
         0.6251305927960652, 0.03638507493848098, 0.5074904590045506, 0.22419232135863287, 0.7182183956514077,
         0.10372358850421703, 0.6089097253503591, 0.46216179509191346, 0.3814376674397305, 0.7468675235265505,
         0.7507210926806857, 0.10424340173843871, 0.17600811811193529, 0.6731691128812382, 0.2666341533090587,
         0.43799316864051496, 0.25209227078542973, 0.4965742387256459, 0.1291903477569457, 0.29354718132961866]

    Y = []
    X.sort()
    for xi in X:
        Y.append(f(xi))
    xi = 0.5 * (1/K)
    for yi in Y:
        ax.bar(xi, yi, width=1 / K, color='#9dd3a8', edgecolor='black')
        ax.vlines(xi, ymin=0, ymax=yi, color='black', linestyle='dashed', linewidth=1.0)
        xi += 1/K

    ax.set_ylabel('$f(X)$', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('$X$', fontweight='bold', fontsize=LabelSize)
    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    # ax.bar(0.6, f(0.6), width=1 / K, alpha=1, color='#369cbf', edgecolor='black')
    # ax.text(0.82, 0.88, r"$f(X_i),X_i=0.6$",
    #         transform=ax.transAxes,
    #         horizontalalignment='right',
    #         verticalalignment='top',
    #         fontweight='bold', fontsize=14)
    ax.text(0.95, 0.95, "$K=30$",
            transform=ax.transAxes,
            horizontalalignment='right',
            verticalalignment='top',
            fontweight='bold', fontsize=30)
    # ax.text(0.61, -0.08, r'$\frac{1}{K}$',
    #         transform=ax.transAxes,
    #         horizontalalignment='right',
    #         verticalalignment='top',
    #         fontweight='bold', fontsize=16)
    fig.tight_layout()
    plt.grid(True)
    plt.close()
    fig.savefig('fig3e.png', bbox_inches='tight')



def qmc_plot(K):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600
    TickSize = 20
    LabelSize = 28
    Labelpad = 5
    LegendSize = 18

    fig, ax = plt.subplots(figsize=(8, 6))

    x = np.linspace(0, 1, 1000)
    y = [f(xi) for xi in x]
    ax.plot(x, y, color='#13334c', linewidth=linew)

    ax.set_xlim([0, 1])
    ax.set_ylim([0,ylim])
    # sobol = qmc.Sobol(1)
    #
    # LDS = sobol.random(K)

    LDS = [0.7165478020906448, 0.15495370235294104, 0.3481292789801955, 0.7885078713297844, 0.9483366087079048, 0.3828520094975829, 0.11216148640960455, 0.5486180484294891, 0.5909736538305879, 0.029520651325583458, 0.47355091385543346, 0.914032400585711, 0.8237849334254861, 0.2584108840674162, 0.23662165366113186, 0.6732117170467973, 0.6356747383251786, 0.1972533818334341, 0.29997594468295574, 0.8596134046092629, 0.9026189455762506, 0.4681196194142103, 0.036661406978964806, 0.6001893663778901, 0.5102265775203705, 0.0716945817694068, 0.42551570292562246, 0.9850195720791817, 0.7781930491328239, 0.3435524767264724]

    X = []
    # Y = []
    for i in LDS:
        X.append(i)
        # Y.append(float(i))
    # print(Y)

    for xi in X:
        yi = f(xi)
        ax.bar(xi, yi, width=1/K, color='#35A9D4', edgecolor='black')
        ax.vlines(xi, ymin=0, ymax=yi, color='black', linestyle='dashed', linewidth=1.0)

    ax.set_ylabel('$f(Y)$', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('$Y$', fontweight='bold', fontsize=LabelSize)
    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    # ax.bar(0.6, f(0.6), width=1 / K, alpha=1, color='#369cbf', edgecolor='black')
    # ax.text(0.82, 0.88, r"$f(X_i),X_i=0.6$",
    #         transform=ax.transAxes,
    #         horizontalalignment='right',
    #         verticalalignment='top',
    #         fontweight='bold', fontsize=14)
    ax.text(0.95, 0.95, "$K=30$",
            transform=ax.transAxes,
            horizontalalignment='right',
            verticalalignment='top',
            fontweight='bold', fontsize=30)
    # ax.text(0.61, -0.08, r'$\frac{1}{K}$',
    #         transform=ax.transAxes,
    #         horizontalalignment='right',
    #         verticalalignment='top',
    #         fontweight='bold', fontsize=16)
    fig.tight_layout()
    plt.grid(True)
    plt.close()
    fig.savefig('fig3d.png', bbox_inches='tight')

def qmc_sample_plot(K):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600
    TickSize = 20
    LabelSize = 28
    Labelpad = 5
    LegendSize = 18

    fig, ax = plt.subplots(figsize=(8, 6))

    x = np.linspace(0, 1, 1000)
    y = [f(xi) for xi in x]
    ax.plot(x, y, color='#13334c', linewidth=linew)

    ax.set_xlim([0, 1])
    ax.set_ylim([0, ylim])
    # sobol = qmc.Sobol(1)
    #
    # LDS = sobol.random(K)

    X = [0.7165478020906448, 0.15495370235294104, 0.3481292789801955, 0.7885078713297844, 0.9483366087079048,
           0.3828520094975829, 0.11216148640960455, 0.5486180484294891, 0.5909736538305879, 0.029520651325583458,
           0.47355091385543346, 0.914032400585711, 0.8237849334254861, 0.2584108840674162, 0.23662165366113186,
           0.6732117170467973, 0.6356747383251786, 0.1972533818334341, 0.29997594468295574, 0.8596134046092629,
           0.9026189455762506, 0.4681196194142103, 0.036661406978964806, 0.6001893663778901, 0.5102265775203705,
           0.0716945817694068, 0.42551570292562246, 0.9850195720791817, 0.7781930491328239, 0.3435524767264724]


    Y = []
    X.sort()
    for xi in X:
        Y.append(f(xi))
    xi = 0.5 * (1/K)
    for yi in Y:
        ax.bar(xi, yi, width=1 / K, color='#35A9D4', edgecolor='black')
        ax.vlines(xi, ymin=0, ymax=yi, color='black', linestyle='dashed', linewidth=1.0)
        xi += 1/K

    ax.set_ylabel('$f(Y)$', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('$Y$', fontweight='bold', fontsize=LabelSize)
    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    # ax.bar(0.6, f(0.6), width=1 / K, alpha=1, color='#369cbf', edgecolor='black')
    # ax.text(0.82, 0.88, r"$f(X_i),X_i=0.6$",
    #         transform=ax.transAxes,
    #         horizontalalignment='right',
    #         verticalalignment='top',
    #         fontweight='bold', fontsize=14)
    ax.text(0.95, 0.95, "$K=30$",
            transform=ax.transAxes,
            horizontalalignment='right',
            verticalalignment='top',
            fontweight='bold', fontsize=30)
    # ax.text(0.61, -0.08, r'$\frac{1}{K}$',
    #         transform=ax.transAxes,
    #         horizontalalignment='right',
    #         verticalalignment='top',
    #         fontweight='bold', fontsize=16)
    fig.tight_layout()
    plt.grid(True)
    plt.close()
    fig.savefig('fig3f.png', bbox_inches='tight')

def main():
    K = 30

    mc_plot(K)
    qmc_plot(K)
    mc_sample_plot(K)
    qmc_sample_plot(K)

if __name__=="__main__":
    main()

