# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 21:00:03 2018

@author: garci
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.signal import argrelextrema


from XRD_functions import *

'write the name of your csv file below:'
name = "MIL53-022as.csv"

def data( filename = name ):
    
    
    '''if the csv file is in a subfolder to this script's, specify path'''
    fname_path='XRD_files/'
    
    with open(fname_path+filename, 'r') as f:
        X = list(csv.reader(f, delimiter=","))        
    Xc=np.array(X[1:], dtype=np.float)        

    return Xc, np.shape(Xc)


xi=data()[0][:,0]
yi=data()[0][:,1]
ybi=backsub(xi,yi,tol=1.00)



'THIS CODE BLOCK: data treatment for plots #2 and #3, subtraction of extraneous peaks'
ybi_t0=backsub(xi,yi,tol=1.4)
ybi_t=backsub(xi,yi,tol=1.0)

locmax_index=argrelextrema(ybi, np.greater)

len_lmi = len(locmax_index[0])
ybi_lm, xi_lm = np.zeros(len_lmi), np.zeros(len_lmi)

for i in range(len_lmi):
    xi_lm [i] = xi[locmax_index[0][i]] 
    ybi_lm [i] = ybi_t0[locmax_index[0][i]] 

for i in range(len_lmi):
    
    Kbeta = emission_lines_plt(xi_lm, ybi_lm,twothet_range_Ka=[xi_lm[i]-0.1,xi_lm[i]+0.1],plt='n')
#    print(Kbetapeak)    
    
    k=0
    while k < len_lmi:

        if Kbeta < (xi_lm[k] + 0.04) and Kbeta > (xi_lm[k] - 0.04):
           print('found', xi_lm[k]) 
           
           k2=-20
           while k2 < 21:
               
               ybi_t[list(xi).index(xi_lm[k])+k2]= 0
               k2+=1
        k+=1
        
'END CODE BLOCK'

'Plot #1'
plt.figure()
plt.plot(xi,yi,color='darkorange',label='not treated')
plt.plot(xi,ybi,color='navy',label='subtracted background')

plt.title(name[:-4])
plt.xlabel(r'$2\theta$ / deg')
plt.ylabel('Intensity / a.u.')
plt.legend(loc='best')

'Plot #2'
plt.figure()
plt.plot(xi,ybi_t0,color='b',label='smoothed plot for Kbeta analysis')
plt.plot(xi_lm,ybi_lm,'ro',label='local maxima')

plt.title(name[:-4])
plt.xlabel(r'$2\theta$ / deg')
plt.ylabel('Intensity / a.u.')
plt.legend(loc='best')

'Plot #3'
plt.figure()

plt.plot(xi,ybi_t,color='navy',label=r'subtracted peaks from $K_\beta$ emission')

plt.title(name[:-4])
plt.xlabel(r'$2\theta$ / deg')
plt.ylabel('Intensity / a.u.')
plt.legend(loc='best')


#emission_lines_plt(xi, ybi,twothet_range_Ka=[17,18])
#emission_lines_plt(xi, ybi,twothet_range_Ka=[20,30])
#emission_lines_plt(xi, ybi,twothet_range_Ka=[27,27.5])
#emission_lines_plt(xi, ybi,twothet_range_Ka=[30,40])


'EXCEL'

import xlwings as xw

def excel(x,y):
    wb=xw.Book()
    xw.Range((1,1)).options(transpose=True).value=x
    xw.Range((1,2)).options(transpose=True).value=y

excel(xi,ybi_t)