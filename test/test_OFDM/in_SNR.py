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
P = 36                      # 导频数，P<N
SNR = range(0,31,5)         # AWGN信道信噪比

''' 多组取平均 '''
gro_num = 100
SNR_num = len(SNR)
lx_MSE  = zeros((gro_num,SNR_num))
CS_MSE  = zeros((gro_num,SNR_num))
eva_MSE = zeros((gro_num,SNR_num))
lx_BER  = zeros((gro_num,SNR_num))
CS_BER  = zeros((gro_num,SNR_num))
eva_BER = zeros((gro_num,SNR_num))
lx_SC   = zeros((gro_num,SNR_num))
CS_SC   = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        print 'Running... Current group: ',i,j
        
        ''' 根据RSSI/Phase产生随机导频图样'''
        pos_A,pos_B,pos_E = agreement(P)
        
        ''' 发送端 '''
        bits_A,diagram_A,x = sender(pos_A)
        
        ''' 信道传输 '''
        h_ab,H_ab,y_b = transmission(x,SNR[j])
        
        ''' 理想条件下的信道估计'''
        # 合法用户确切知道发送端导频
        h_lx,H_lx,bits_lx,diagram_lx = receiver(y_b,pos_A)
    
        ''' 接收端 信道估计'''
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,pos_B)
        
        ''' 窃听信道 '''
        h_ae,H_ae,y_e = transmission(x,SNR[j])
        
        ''' 非法用户 '''
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,pos_E)
        
        ''' 评价性能 '''
        lx_MSE[i,j]  = MSE(H_ab,H_lx)
        CS_MSE[i,j]  = MSE(H_ab,H_cs)
        eva_MSE[i,j] = MSE(H_ae,H_eva)   
        lx_BER[i,j]  = BMR(bits_A,bits_lx)
        CS_BER[i,j]  = BMR(bits_A,bits_cs)
        eva_BER[i,j] = BMR(bits_A,bits_eva)
        lx_SC[i,j]   = SecCap(lx_BER[i,j],eva_BER[i,j])
        CS_SC[i,j]   = SecCap(CS_BER[i,j],eva_BER[i,j])

lx_MSE  = mean(lx_MSE,0)   
CS_MSE  = mean(CS_MSE,0)
eva_MSE = mean(eva_MSE,0)
lx_BER  = mean(lx_BER,0)
CS_BER  = mean(CS_BER,0)
eva_BER = mean(eva_BER,0)
lx_SC   = mean(lx_SC,0)
CS_SC   = mean(CS_SC,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(SNR,lx_MSE, 'ko-', label='Bob(Method 1)')
plt.plot(SNR,CS_MSE, 'k^:', label='Bob(Method 2)')
plt.plot(SNR,eva_MSE,'ks--',label='Eve')
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,lx_BER, 'ko-', label='Bob(Method 1)')
plt.semilogy(SNR,CS_BER, 'k^:', label='Bob(Method 2)')
plt.semilogy(SNR,eva_BER,'ks--',label='Eve')
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(SNR,lx_SC,'ko-',label='Bob(Method 1)')
plt.plot(SNR,CS_SC,'k^:',label='Bob(Method 2)')
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()

print 'Program Finished'