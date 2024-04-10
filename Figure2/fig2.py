import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt

import matplotlib.ticker as mtick


def f(x):
    return np.sin(x) + np.cos(2*x)
def mc_integral_plot():
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600
    TickSize = 20
    LabelSize = 28
    Labelpad = 5
    LegendSize = 18

    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.linspace(0, 1, 100)
    y = f(x)
    ax.plot(x, y, color='#13334c', linewidth=5)
    ax.set_xlim([0, 1])
    ax.set_ylim(ymin=0)
    ax.fill_between(x, 0, y, facecolor='#9dd3a8')

    ax.set_ylabel('$f(X)$', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('$X$', fontweight='bold', fontsize=LabelSize)
    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    fig.tight_layout()
    plt.grid(True)
    # plt.show()
    plt.close()
    fig.savefig('fig2a.png', bbox_inches='tight')

def mc_plot(K, X):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600
    TickSize = 20
    LabelSize = 28
    Labelpad = 5
    LegendSize = 18

    fig, ax = plt.subplots(figsize=(8, 6))

    x = np.linspace(0, 1, 100)
    y = f(x)
    ax.plot(x, y, color='#13334c', linewidth=5)

    ax.set_xlim([0, 1])
    ax.set_ylim(ymin=0)

    print(len(X))
    for xi in X:
        yi = f(xi)
        ax.bar(xi, yi, width=1/K,  color='#9dd3a8', edgecolor='black')
        ax.vlines(xi, ymin=0, ymax=yi, color='black', linestyle='dashed', linewidth=1.0)

    ax.set_ylabel('$f(X)$', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
    ax.set_xlabel('$X$', fontweight='bold', fontsize=LabelSize)
    ax.tick_params(axis='x', labelsize=TickSize)
    ax.tick_params(axis='y', labelsize=TickSize)
    # ax.text(0.8, 0.88, r"$f(X_i),X_i=0.6$",
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
    fig.savefig('fig2b.png', bbox_inches='tight')

def mc_sample_plot(K, X):
    plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
    plt.rcParams['figure.dpi'] = 600
    TickSize = 20
    LabelSize = 28
    Labelpad = 5
    LegendSize = 18

    fig, ax = plt.subplots(figsize=(8, 6))

    x = np.linspace(0, 1, 100)
    y = f(x)
    ax.plot(x, y, color='#13334c', linewidth=5)

    ax.set_xlim([0, 1])
    ax.set_ylim(ymin=0)

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
    fig.savefig('fig2c.png', bbox_inches='tight')


def main():
    mc_integral_plot()
    K = 30
    X = [0.6, 0.28282902449878544, 0.775650065172436, 0.2767712210313754, 0.7691304386149064, 0.7547701629368181, 0.4929472076530782, 0.5467652932369932, 0.44359209230404284, 0.523976589449887, 0.8525846325883573, 0.3778385331112425, 0.16701246776367573, 0.411471472522432, 0.4809327832539496, 0.6769026676143763, 0.8151971913129066, 0.11937859926122307, 0.3110105033745125, 0.5207422046957589, 0.6793062124527502, 0.00088036226986965, 0.1363089076822157, 0.9882428150135429, 0.0843012334463088, 0.888652941494068, 0.5335354900257131, 0.41875283941884733, 0.7691685276694834, 0.10207917740823469]
    # X = list(np.random.rand(K))
    mc_plot(K,X)
    mc_sample_plot(K,X)


if __name__=="__main__":
    main()

