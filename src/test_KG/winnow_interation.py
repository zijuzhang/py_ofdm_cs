# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../')
from util.metric import BMR,BGR
from KG import sampling,quantize_phase,quantize_ASBG_1bit,remain,merge,reconciliation

os.system('cls')
plt.close('all')

''' 参数 '''
sampling_period = 1
sampling_time   = 1
mtype = 'cross'
rtype = 'winnow'
iteration = [0,1,2,3,4]

''' 多组取平均 '''
group_num = 100
inter_num = len(iteration)
bmr = zeros((group_num,inter_num))
bgr = zeros((group_num,inter_num))

for i in range(group_num):
    for j in range(inter_num):
        print 'Running... Current group: ',i,j
        
        ''' 采样 '''
        rssi_A, rssi_B, rssi_E  = sampling('RSSI', sampling_period,sampling_time)  
        phase_A,phase_B,phase_E = sampling('Phase',sampling_period,sampling_time)
            
        ''' RSSI量化 '''
        bits_A_rssi,drop_list_A = quantize_ASBG_1bit(rssi_A)
        bits_B_rssi,drop_list_B = quantize_ASBG_1bit(rssi_B)
        bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
        bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
        
        ''' Phase量化 '''
        bits_A_phase = quantize_phase(phase_A)
        bits_B_phase = quantize_phase(phase_B)
        
        ''' 合并 '''
        bits_A = merge(bits_A_rssi,bits_A_phase,mtype)
        bits_B = merge(bits_B_rssi,bits_B_phase,mtype)
        
        ''' 信息协调 '''
        bits_A,bits_B = reconciliation(bits_A,bits_B,rtype,iteration[j])
        
        ''' 评价性能 '''
        bmr[i,j] = BMR(bits_A,bits_B)
        bgr[i,j] = BGR(bits_A,sampling_time,sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(iteration,bmr,'ko-')
plt.xlabel('Iteration')
plt.ylabel('BMR')
plt.title('BMR of different iteration')
plt.show()

plt.figure(figsize=(8,5))
plt.plot(iteration,bgr,'ko-',)
plt.xlabel('Iteration')
plt.ylabel('BGR')
plt.title('BGR of different iteration')
plt.show()

print 'Program Finished'