# -*- coding: utf-8 -*-
"""make the graphs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dso-_Sx8jdRctGTPxpvzcWm_IlE3ZkaQ
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np 
import matplotlib as plt 
import pandas as pd 
import math 
from array import array
import seaborn as sns
import statsmodels.api as sm
from google.colab import files
from scipy import stats
#uploaded = files.upload()

cd drive/My Drive/data

!ls

j11 = np.load('')
j12 = np.load('')
f11 = np.load('')
f12 = np.load('')
f21 = np.load('')
f22 = np.load('')
j21 = np.load('')
j22 = np.load('')
j31 = np.load('')
j32 = np.load('')
f31 = np.load('')
f32 = np.load('') 
j42 = np.load('')
f42 = np.load('')
j41 = np.load('')
f41 = np.load('')
f52 = np.load('')
j52 = np.load('')
j51 = np.load('')
f51 = np.load('')
j61 = np.load('')
f62 = np.load('')

plt.rcParams['figure.figsize'] = [10, 10]
x = abs(f22)
time = np.arange(1,321,1)
plt.pyplot.plot(time[:80],x[:80])
plt.pyplot.plot(time[79:240],x[79:240])
plt.pyplot.plot(time[239:],x[239:])

avg1 = np.array(j12)
avgd = np.mean(avg1.reshape(-1, 8), axis=1)
plt.pyplot.plot(avgd)

"""Fancy Graphs"""

tav,tste = standard_error(avg)
tav2,tste2 = standard_error(avg2)

avg = f22
avg1 = np.array(avg)
avgd = np.mean(avg1.reshape(-1, 8), axis=1)
plt.pyplot.plot(avgd)

plt.rcParams['figure.figsize'] = [13, 13]
x = f22
time = np.arange(1,321,1)
time2 = np.arange(1,41,1)
time2 *= 8
plt.pyplot.title('Single Participant Force Sensor Visual Field Disturbance Error',fontsize = 20)
plt.pyplot.ylabel('Error ',fontsize = 20)
plt.pyplot.xlabel('Trial #',fontsize = 20)
plt.pyplot.plot(time[:80],x[:80],alpha=0.5)
plt.pyplot.plot(time[79:240],x[79:240],alpha=0.5)
plt.pyplot.plot(time[239:],x[239:],alpha=0.5)
plt.pyplot.plot((time2-4),avgd,color = 'red')
plt.pyplot.errorbar((time2-4),avgd,tste,ecolor= 'black')
#plt.pyplot.savefig('g_f22_2.jpg')

plt.rcParams['figure.figsize'] = [13, 13]
x = avg
time = np.arange(1,321,1)
time2 = np.arange(1,41,1)
time2 *= 8
plt.pyplot.title('Comparison of Visual Field Disturbance for Force Sensor and Joystick',fontsize = 20)
plt.pyplot.ylabel('Error ',fontsize = 20)
plt.pyplot.xlabel('Trial #',fontsize = 20)
plt.pyplot.plot(time[:80],x[:80],alpha=0.5)
plt.pyplot.plot(time[79:240],x[79:240],alpha=0.5)
plt.pyplot.plot(time[239:],x[239:],alpha=0.5)
plt.pyplot.plot((time2-4),avgd)
plt.pyplot.errorbar((time2-4),avgd,tste)


x= avg2
plt.pyplot.plot(time[:80],x[:80],alpha=0.5)
plt.pyplot.plot(time[79:240],x[79:240],alpha=0.5)
plt.pyplot.plot(time[239:],x[239:],alpha=0.5)
plt.pyplot.plot((time2-4),avgd2)
plt.pyplot.errorbar((time2-4),avgd2,tste2)
#plt.pyplot.savefig('compare_vf.jpg')

plt.rcParams['figure.figsize'] = [13, 13]
time = np.arange(1,321,1)
time2 = np.arange(1,41,1)
time2 *= 8
plt.pyplot.plot(time,avg,alpha=0.5,label ='Joystick Visual Rotation Error')
plt.pyplot.plot(time,avg2,alpha=0.5,label='Force Sensor Visual Rotation Error')
plt.pyplot.errorbar((time2-4),avgd)
plt.pyplot.errorbar((time2-4),avgd2,color='black')
plt.pyplot.errorbar((time2-4),avgd,tste,label='8 Block Average for Joystick Visual Rotation Error')
plt.pyplot.errorbar((time2-4),avgd2,tste2, label = '8 Block Average for Force Sensor Visual Rotation Error')

plt.pyplot.title('Comparison of Visual Rotation for Force Sensor and Joystick',fontsize = 20)
plt.pyplot.ylabel('Error ',fontsize = 20)
plt.pyplot.xlabel('Trial #',fontsize = 20)


plt.pyplot.legend(loc = 'lower left',fontsize=12)
#plt.pyplot.savefig('Comparing_vr2.jpg')

plt.rcParams['figure.figsize'] = [20, 20]
x = avg
time = np.arange(1,321,1)
plt.pyplot.plot(time[:80],x[:80])
plt.pyplot.plot(time[79:240],x[79:240])
plt.pyplot.plot(time[239:],x[239:])

plt.rcParams['figure.figsize'] = [13,13]
x = avgd
time = np.arange(1,41,1)

plt.pyplot.plot(time[:10],x[:10],color = 'orange')

plt.pyplot.plot(time[9:30],x[9:30],color='red')

plt.pyplot.plot(time[29:],x[29:],color= 'green')
plt.pyplot.errorbar(time[:10],avgd[:10],tste[:10],ecolor= 'black')
plt.pyplot.errorbar(time[9:30],avgd[9:30],tste[9:30],ecolor= 'black')
plt.pyplot.errorbar(time[29:],avgd[29:],tste[29:],ecolor= 'black')

"""Joystick Rotation"""

avg = (j11+j21[:320]+j31+j41+j51+j61)/6
plt.rcParams['figure.figsize'] = [10, 10]
plt.pyplot.plot(avg)

'''calcutate the ttest from the begining of the experimental trials and the end to see if any learning occured'''

#avg[80:88]
#avg[232:240]
jr_ttest = stats.ttest_ind(avg[80:88],avg[232:240])

avg1 = np.array(avg)
avgd = np.mean(avg1.reshape(-1, 8), axis=1)
plt.pyplot.plot(avgd)

"""Joystick Distortion"""

avg = (abs(j12)+abs(j22)+abs(j32)+abs(j42)+abs(j52))/5
plt.rcParams['figure.figsize'] = [10, 10]
plt.pyplot.plot(avg)

avg = (j12+j22+j32+j42+j52)/5
plt.rcParams['figure.figsize'] = [10, 10]
plt.pyplot.plot(avg)

avg1 = np.array(avg)
avgd = np.mean(avg1.reshape(-1, 8), axis=1)
plt.pyplot.plot(avgd)

'''calcutate the ttest from the begining of the experimental trials and the end to see if any learning occured'''

#avg[80:88]
#avg[232:240]
jd_ttest=stats.ttest_ind(avg[80:88],avg[232:240])
print(jd_ttest)

"""Force Rotation"""

avg2 = (f11+f21+f31+f41+f51)/5
plt.rcParams['figure.figsize'] = [10, 10]
plt.pyplot.plot(avg2)

'''calcutate the ttest from the begining of the experimental trials and the end to see if any learning occured'''
#avg[80:88]
#avg[232:240]
fr_ttest=stats.ttest_ind(avg2[80:88],avg2[232:240])

avg1 = np.array(avg2)
avgd2 = np.mean(avg1.reshape(-1, 8), axis=1)
plt.pyplot.plot(avgd2)

"""Force Distortion"""

avg = (abs(f12)+abs(f22)+abs(f32)+abs(f42)+abs(f52)+abs(f62))/6
plt.rcParams['figure.figsize'] = [10, 10]
plt.pyplot.plot(avg)

avg2 = (f12+f22+f32+f42+f52+f62)/6
plt.rcParams['figure.figsize'] = [10, 10]
plt.pyplot.plot(avg2)

'''calcutate the ttest from the begining of the experimental trials and the end to see if any learning occured'''

#avg[80:88]
#avg[232:240]
fd_ttest=stats.ttest_ind(avg2[80:88],avg2[232:240])

avg1 = np.array(avg2)
avgd2 = np.mean(avg1.reshape(-1, 8), axis=1)
plt.pyplot.plot(avgd2)

'''calculate ttest to compare force and joystick trials'''

#avg[80:88]
#avg[232:240]
vr_begining = stats.ttest_ind(avg[80:88],avg2[80:88])
vr_end = stats.ttest_ind(avg[232:240],avg2[232:240])

'''calculate ttest to compare force and joystick trials'''

#avg[80:88]
#avg[232:240]
vd_begining = stats.ttest_ind(avg[80:88],avg2[80:88])
vd_end = stats.ttest_ind(avg[232:240],avg2[232:240])

print(jr_ttest)
print(jd_ttest)
print(fr_ttest)
print(fd_ttest)
print(vr_begining)
print(vr_end)
print(vd_begining)
print(vd_end)

ttest = pd.DataFrame(data=(jr_ttest.pvalue,fr_ttest.pvalue,vr_begining.pvalue,vr_end.pvalue,jd_ttest.pvalue,fd_ttest.pvalue,vd_begining.pvalue,vd_end.pvalue))
ttest.index = ('Joystick Rotation ttest','Force Sensor Rotation ttest','Joystick and Force Sensor Visual Rotation Begining Comparison','Joystick and Force Sensor Visual Rotation End Comparison',
                 'Joystick Visual Field Disturbance ttest','Force Sensor Visual Field Disturbance ttest','Joystick and Force Sensor Visual Field Disturbance Begining Comparison',
                 'Joystick and Force Sensor Visual Field Disturbance End Comparison')
ttest.columns = ['pvalue']

#dfStyler = ttest.style.set_properties(**{'text-align': 'left'})
#dfStyler.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
#ttest.pvalue.round(7)
ttest