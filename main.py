# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
import matplotlib.pyplot as plt
from numpy import size,zeros
from channel import channel
from MSE_com import MSE_com

os.system('cls')
plt.close('all')

L = 50                      # L:信道长度
K = 6                       # K:稀疏度/多径数，满足:K<<L
N = [128,256,512]           # 训练序列长度/载波数,满足：L<=N
SNR = [0,5,10,15,20,25,30]  # AWGN信道信噪比

''' 时域的信道脉冲响应'''
h = channel(L, K)

''' LS/MMSE/CS信道估计，得MSE
    比较不同的载波数N和信噪比SNR '''
N_num   = size(N)
SNR_num = size(SNR)
cs      = zeros((N_num,SNR_num))
for i in range(N_num):
    cs[i,:] = MSE_com(K,h,SNR,N[i])
    
plt.figure(figsize=(8,5))
plt.semilogy(SNR,cs[0,:],'ro-',linewidth=1,label='CS(Min N)')
plt.semilogy(SNR,cs[1,:],'rp-',linewidth=1.5,label='CS(Mid N)')
plt.semilogy(SNR,cs[2,:],'rs-',linewidth=2,label='CS(Max N)')
plt.legend()

print 'Program Finished'