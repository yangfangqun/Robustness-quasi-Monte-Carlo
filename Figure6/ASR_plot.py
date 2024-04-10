import operator, pylab, random
import matplotlib.pyplot as plt

#Karate
filename = 'Karate'
N = 34
y = [1, 1, 0.8, 1, 1, 1, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 1, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 0.8]
sol = ['33', '0', '32', '1', '2', '3', '5', '25', '4', '23', '24', '6', '8', '28', '29', '19', '20', '12', '13', '22', '17', '31', '21', '11', '16', '26', '27', '9', '14', '10', '15', '18', '30', '7']
Y = [0 for i in range(N)]
for i in range(N):
    Y[int(sol[i])] = y[i]


# #Krebs
# filename = 'Krebs'
# N = 62
# x = [i for i in range(N)]
# y = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]# Airport
# sol = ['1', '11', '7', '5', '22', '14', '49', '12', '15', '20', '2', '27', '29', '6', '19', '28', '40', '30', '43', '23', '24', '32', '45', '52', '3', '10', '25', '33', '47', '53', '54', '56', '36', '46', '37', '26', '57', '61', '34', '31', '41', '38', '18', '17', '42', '16', '55', '50', '35', '13', '51', '59', '39', '48', '58', '44', '0', '8', '60', '21', '4', '9']
#
# Y = [0 for i in range(N)]
# for i in range(N):
#     Y[int(sol[i])] = y[i]
# #     #




plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman', 'mathtext.fontset': 'stix'})
plt.rcParams['figure.dpi'] = 600
TickSize = 20
LabelSize = 28
Labelpad = 5
LegendSize = 14
# Linewidth = 4

fig, ax = plt.subplots(figsize=(8, 6))

plt.bar(range(N), Y, color='#204969')
ax.set_ylabel('ASR', labelpad=Labelpad, fontweight='bold', fontsize=LabelSize)
ax.set_xlabel('Node index', fontweight='bold', fontsize=LabelSize)
ax.set_xlim(-1,N)
ax.set_ylim([0, 1.2])
# ax.set_title(filename, fontweight='bold', fontsize=LabelSize)

# xmajorLocator = MultipleLocator(0.1)  # 将x主刻度标签设置为0.05的倍数
# xmajorFormatter = FormatStrFormatter('%.1f')  # 设置x轴标签文本的格式
# ax.xaxis.set_major_locator(xmajorLocator)
# ax.xaxis.set_major_formatter(xmajorFormatter)
#
# ymajorLocator = MultipleLocator(0.2)  # 将y轴主刻度标签设置为0.5的倍数
# ymajorFormatter = FormatStrFormatter('%.1f')  # 设置y轴标签文本的格式
# ax.yaxis.set_major_locator(ymajorLocator)
# ax.yaxis.set_major_formatter(ymajorFormatter)
# legend_properties = {'weight': 'bold'}
# ax.legend(loc='upper right', fontsize=LegendSize)

ax.tick_params(axis='x', labelsize=TickSize)
ax.tick_params(axis='y', labelsize=TickSize)
# fig.tight_layout()
fig.savefig('%sASR.png' %filename, bbox_inches='tight')


# #画图
# # pylab.figure(figsize=(9,6), dpi=300)
# pylab.figure(dpi=400)
# # pylab.title(filename)
# pylab.title('Karate')
# pylab.xlabel(r"Node attack sequence")
# pylab.ylabel(r"Attack success rate")
# pylab.ylim(0.89,1.03)
# pylab.xlim(0,N+1)
# pylab.plot(x, y1, "r:", alpha=1, linewidth=3, ms=2)
# pylab.plot(x, y2, "b--", alpha=1, linewidth=2, ms=0.5)
# pylab.plot(x, y3, "g-", alpha=1, linewidth=0.6, ms=0.5)
#
# #画图时的标签
# pylab.legend((r"Case 1",
#                   "Case 2",
#               "Case 3",
#               ),
#                  loc = "upper right", shadow = False)
# pylab.show()
# pylab.close(1)