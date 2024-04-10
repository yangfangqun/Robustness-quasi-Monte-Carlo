import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return np.sin(x) + np.cos(2*x)

x = np.linspace(0, 2*np.pi, 1000) # 生成0到2π的1000个点
y = f(x)

fig, ax = plt.subplots()
ax.plot(x, y, 'r-', linewidth=2)
ax.fill_between(x, 0, y, facecolor='blue', alpha=0.3)

n = 10 # 随机生成10个点
xi = np.random.uniform(0, 2*np.pi, n)
yi = f(xi)

bar_width = 0.2
ax.bar(xi, yi, width=bar_width, alpha=0.5, color='green')

# 标出第一个柱子的宽度
rect = ax.patches[0]
x_pos = rect.get_x() + bar_width/2
y_pos = rect.get_height() + 0.1
ax.annotate(f'width={bar_width:.2f}', (x_pos, y_pos), ha='center', va='center', fontsize=12, color='red')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('f(x) = sin(x) + cos(2x)')
plt.grid(True)
plt.show()
