import numpy as np
from scipy.stats import qmc
import matplotlib.pyplot as plt
#

# 生成Sobol点列
num_points = 1
dim = 2
sobol = qmc.Sobol(5)
for i in range(1):
    sobol_points = sobol.random(1)[0]
    print(sobol_points)


# 绘制散点图  2维
fig, ax = plt.subplots(figsize=(15,15),dpi=400)
ax.scatter(sobol_points[:,0], sobol_points[:,1], c='b', marker='o')
ax.set_title("Sobol Points Example")
ax.set_xlabel("X")
ax.set_ylabel("Y")
fig.savefig('./fig/sobol.png')
#
#
#
#均匀分布
random_points = np.random.rand(num_points, 2)  # 生成1000个随机均匀分布的点
fig, ax = plt.subplots(figsize=(15,15),dpi=400)
ax.scatter(random_points[:,0], random_points[:,1], c='r', marker='o')
ax.set_title("uni Points Example")
ax.set_xlabel("X")
ax.set_ylabel("Y")
fig.savefig('./fig/uni.png')
