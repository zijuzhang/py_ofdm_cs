# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../../src')
from util.metric import MSE,BMR,SecCap
from KG import agreement
from OFDM import sender,transmission,receiver
  
os.system('cls')
plt.close('all')

''' 参数 '''
P = 36
block_size = range(5,41,5)

''' 多组取平均 '''
group_num = 100
bsize_num = len(block_size)
bob_MSE   = zeros((group_num,bsize_num))
eva_MSE   = zeros((group_num,bsize_num))
bob_BER   = zeros((group_num,bsize_num))
eva_BER   = zeros((group_num,bsize_num))
SC        = zeros((group_num,bsize_num))

for i in range(group_num):
    for j in range(bsize_num):
        print 'Running... Current group: ',i,j
        
        pos_A,pos_B,pos_E = agreement(P,{'block_size':block_size[j]})
        bits_A,diagram_A,x = sender(pos_A)
        h_ab,H_ab,y_b = transmission(x)
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,pos_B)
        h_ae,H_ae,y_e = transmission(x)
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,pos_E)
        bob_MSE[i,j] = MSE(H_ab,H_cs)
        eva_MSE[i,j] = MSE(H_ae,H_eva)   
        bob_BER[i,j] = BMR(bits_A,bits_cs)
        eva_BER[i,j] = BMR(bits_A,bits_eva)
        SC[i,j]      = SecCap(bob_BER[i,j],eva_BER[i,j])

bob_MSE = mean(bob_MSE,0)   
eva_MSE = mean(eva_MSE,0)
bob_BER = mean(bob_BER,0)
eva_BER = mean(eva_BER,0)
SC      = mean(SC,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(block_size,bob_MSE,'ko-')
plt.xlabel('Block size')
plt.ylabel('MSE(dB)')
plt.title('MSE')

plt.figure(figsize=(8,5))
plt.semilogy(block_size,bob_BER,'ko-')
plt.xlabel('Block size')
plt.ylabel('BER')
plt.title('BER')

plt.figure(figsize=(8,5))
plt.plot(block_size,SC,'ko-')
plt.xlabel('Block size')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')

print 'Program Finished'