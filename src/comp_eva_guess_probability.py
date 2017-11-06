# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 13:40:53 2016

@author: gymmer
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from numpy import zeros,argmax
from function import c

os.system('cls')
plt.close('all')

N = 512                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # 导频数，P<N

'''
非法用户猜测导频位置，猜对数的概率
窃听者从N个子载波中，猜测P个导频的位置。
假设窃听者猜中n个时，其概率为pro，则n=0,1,2,...,P时，各有对应的概率
'''
pro = zeros(P+1)            # 猜中的概率
for i in range(P+1):        # 猜中的导频数
    pro[i] = c(P,i)*c(N-P,P-i)/(c(N,P)+0.0)
maxright = argmax(pro)      # 找到概率最大对应的位置

print ('Most probabily guess right:Pro(%d)=%f'%(maxright,pro[maxright]))

plt.figure(figsize=(8,5))
plt.plot(pro,'bo-')
plt.plot(maxright,pro[maxright],'ro')
plt.xlabel('number of right pilots')
plt.ylabel('probability')
plt.title('Probability of the number of right pilots')