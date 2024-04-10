
# file = 'Karate'
# file = 'Krebs'
# file = 'Airport'
# file = 'Crime'
# file = 'Power'
file = 'Oregon1'

pv_file =  file + '_ASR.txt'
f = open(pv_file, encoding='utf-8')
f_list = f.readlines()
p_vi = [float(i) for i in f_list] # 注意有些gml文件的节点是str，有些是int
f.close()
print(p_vi)
count = sum(1 for x in p_vi if x != 1.0)

print("不等于1的元素数量为：", count)