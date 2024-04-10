import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import qmc

sobol = qmc.Sobol(1)
X =[]
LDS = sobol.random(10)
for i in LDS:
    X.append(float(i))
print(X)
