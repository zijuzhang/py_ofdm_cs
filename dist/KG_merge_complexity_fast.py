# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

sampling_time = range(1,30,1)
times = array([[   26.6 ,    10.7 ,    43.25,    71.45],
       [   54.  ,    20.3 ,   111.4 ,   101.8 ],
       [  115.3 ,    36.3 ,   155.35,   148.6 ],
       [  148.8 ,    48.95,   200.35,   207.4 ],
       [  168.15,    81.25,   269.8 ,   254.45],
       [  223.5 ,    70.65,   314.4 ,   293.15],
       [  250.7 ,   111.45,   387.4 ,   344.5 ],
       [  275.75,   117.05,   433.85,   409.25],
       [  315.45,   127.2 ,   510.65,   450.75],
       [  355.4 ,   148.55,   560.85,   510.8 ],
       [  410.3 ,   157.05,   635.1 ,   583.3 ],
       [  455.6 ,   185.15,   707.25,   649.3 ],
       [  492.4 ,   181.7 ,   761.2 ,   702.  ],
       [  542.95,   222.35,   840.65,   768.95],
       [  580.95,   247.15,   893.1 ,   811.15],
       [  623.25,   251.2 ,   976.3 ,   873.  ],
       [  659.7 ,   282.1 ,  1031.7 ,   932.3 ],
       [  684.05,   296.35,  1109.95,   973.4 ],
       [  711.85,   320.3 ,  1170.8 ,  1032.35],
       [  786.85,   329.85,  1245.95,  1114.5 ],
       [  810.65,   340.3 ,  1302.3 ,  1172.25],
       [  856.35,   386.15,  1362.6 ,  1214.95],
       [  904.3 ,   372.8 ,  1444.25,  1307.75],
       [  966.25,   404.  ,  1551.85,  1375.  ],
       [ 1038.9 ,   419.3 ,  1618.45,  1480.95],
       [ 1079.55,   461.4 ,  1727.6 ,  1553.8 ],
       [ 1161.65,   485.55,  1823.15,  1620.1 ],
       [ 1213.1 ,   530.55,  1913.8 ,  1718.15],
       [ 1258.3 ,   536.65,  2027.  ,  1762.35]])
       
plt.figure(figsize=(8,5))
plt.plot(sampling_time,times[:,0],'ko-', label='RSSI Only')
plt.plot(sampling_time,times[:,1],'k^:', label='Phase Only')
plt.plot(sampling_time,times[:,2],'ks--',label='Cross')
plt.plot(sampling_time,times[:,3],'kp--',label='AND')
plt.xlabel('Sampling Time(s)')
plt.ylabel('Time(ms)')
plt.title('Time of different sampling time')
plt.legend()
plt.show()