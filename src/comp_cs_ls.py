# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
from numpy import zeros,mean,arange
import matplotlib.pyplot as plt
from pos_agreement import agreement
from part_sender import sender
from part_transmission import transmission
from part_receiver import receiver
from function import MSE,BMR,SecCap
  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
Ncp = 60                    # 循环前缀的长度,Ncp>L
P = 36                      # CS估计导频数，P<N
pos_ls = arange(0,N,5)      # LS估计的均匀导频图样
SNR = range(0,31,5)         # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
weight = 0.5                # 权重
gro_num = 100               # 进行多组取平均

''' 比较不同的信噪比SNR '''
SNR_num = len(SNR)
CS_MSE  = zeros((gro_num,SNR_num))
LS_MSE  = zeros((gro_num,SNR_num))
eva_MSE = zeros((gro_num,SNR_num))
CS_BER  = zeros((gro_num,SNR_num))
LS_BER  = zeros((gro_num,SNR_num))
eva_BER = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        print 'Running... Current group: ',i,j
        
        ''' CS '''
        pos_A,pos_B,pos_E = agreement(P,weight)
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
        h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR[j])
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,L,K,N,Ncp,pos_A,modulate_type,'CS','from_pos')
        h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR[j])
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type,'CS','from_pos')
        CS_MSE[i,j]  = MSE(H_ab,H_cs)
        eva_MSE[i,j] = MSE(H_ae,H_eva)
        CS_BER[i,j]  = BMR(bits_A,bits_cs)
        eva_BER[i,j] = BMR(bits_A,bits_eva)
 
        ''' LS '''
        bits_A,diagram_A,x = sender(N,Ncp,pos_ls,modulate_type)
        h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR[j])
        h_ls,H_ls,bits_ls,diagram_ls = receiver(y_b,L,K,N,Ncp,pos_ls,modulate_type,'LS','from_pos') 
        LS_MSE[i,j]  = MSE(H_ab,H_ls)
        LS_BER[i,j]  = BMR(bits_A,bits_ls)

''' 多组取平均 ''' 
CS_MSE  = mean(CS_MSE,0)
LS_MSE  = mean(LS_MSE,0)
eva_MSE = mean(eva_MSE,0)
CS_BER  = mean(CS_BER,0)
LS_BER  = mean(LS_BER,0)
eva_BER = mean(eva_BER,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE, 'g*-',label='CS(Random, P=%s)'%(P))
plt.plot(SNR,LS_MSE, 'bo-',label='LS(Even, P=%s)'%(len(pos_ls)))
plt.plot(SNR,eva_MSE,'r^--',label='Evasdropper(Random, P=%s)'%(P))
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_BER, 'g*-',label='CS(Random, P=%s)'%(P))
plt.semilogy(SNR,LS_BER, 'bo-',label='LS(Even, P=%s)'%(len(pos_ls)))
plt.semilogy(SNR,eva_BER,'r^--',label='Evasdropper(Random, P=%s)'%(P))
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

print 'Program Finished'