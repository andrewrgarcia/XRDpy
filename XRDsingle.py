# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 21:00:03 2018

@author: garci
"""

'''Background subtraction and plotting algorithms for XRD files in .csv format
Developer: Andrew
'''

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def bacsub(xdata,ydata,tol=1):
    'approx. # points for half width of peaks'
    L=len(ydata)
    lmda = int(0.50*L/(xdata[0]-xdata[L-1]))
    
    newdat=np.zeros(L)
    for i in range(L):        
        if ydata[(i+lmda)%L] > tol*ydata[i]:          #tolerance 'tol'
            newdat[(i+lmda)%L] = ydata[(i+lmda)%L] - ydata[i]
        else:
            if ydata[(i+lmda)%L] < ydata[i]: 
                newdat[(i+lmda)%L] = 0
    
    return newdat

def data():
    '''put .csv file in python directory 
    replace "sample.csv" with name of .csv file to be analyzed below '''
    
    with open("sample.csv", 'r') as f:
        X = list(csv.reader(f, delimiter=","))        
    Xc=np.array(X[1:], dtype=np.float)        

    return Xc, np.shape(Xc)

#y,x = data()[1]
#xi, yi, ybi = np.zeros((3,x,y))
xi=data()[0][:,0]
yi=data()[0][:,1]
ybi=bacsub(xi,yi,tol=1)
plt.plot(xi,yi,color='darkorange')
plt.xlabel(r'$2\theta$ / deg')
plt.ylabel('Intensity / a.u.')

plt.figure()
plt.plot(xi,ybi,color='navy')
plt.title('(background subtracted)')
plt.xlabel(r'$2\theta$ / deg')
plt.ylabel('Intensity / a.u.')
