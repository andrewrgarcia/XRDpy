# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 15:06:48 2018

@author: garci
"""

import numpy as np


'''To find local maxima'''
def local_max(x,y,xrange=[12,13]): 
    x1,x2=xrange
    xsearch_index=[]
    for n in x:
        if n >= x1 and  n <= x2:
            xsearch_index.append(list(x).index(n))
    
    max_y = 0
    max_x = 0
    for i in xsearch_index:
        if y[i] > max_y:
            max_y = y[i]
            max_x = x[i]
    
    return max_x, max_y


'''Scherrer equation'''
def scherrer(K,lmda,beta,theta):
        
    return K*lmda / (beta*np.cos(theta))    #tau


'''To calculate the Scherrer width for a peak lying in a specific range'''
def schw_peakcal(x,y,xrange=[12,13]):
    
    x1,x2=xrange
    xsearch_index=[]
    for n in x:
        if n >= x1 and  n <= x2:
            xsearch_index.append(list(x).index(n))
    
    max_y = 0
    max_x = 0
    for i in xsearch_index:
        if y[i] > max_y:
            max_y = y[i]
            max_x = x[i]
    
    'scherrer width peak calculations'
    max_twotheta,max_y = max_x,max_y
    
    hm = max_y/2
    theta=max_twotheta/2
    theta=theta*np.pi/180
    
    tol=1
    beta_range = []
    for i in xsearch_index:
        if y[i] > hm :
            beta_range.append(x[i])
    
    
    beta_range = [max(beta_range), min(beta_range)]
    beta = max(beta_range) - min(beta_range)
    beta = beta*np.pi/180
#    print(hm)
#    print(theta)
#    print(beta_range)
#    print(beta)
    
    s=scherrer(0.9,0.154,beta,theta)
    return s


'''Background subtraction operation:'''
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


'''Function for an "n" point moving average: '''
def movnavg(xdata,ydata,n=1):
    
    L=int(len(xdata)//n)
    newy=np.zeros(L)
    for i in range(L):
        k=0
        while k < n:
           newy[i] += ydata[(i*n)+k]
           k += 1
#           print(i)
        newy[i]=newy[i]/n
    
    newx=np.zeros(L)
    for i in range(L):
        newx[i] = xdata[i*n]

#    'test it'
#    plt.plot(xdata,ydata)
#    plt.plot(newx,newy,linewidth=3)
        
    return newx,newy


'''Calculate relative peak intensity (i.e. comparing one peak to another)'''
def XRD_int_ratio(x,y,xR1=[8.88,9.6],xR2=[10.81,11.52]):
    'XRD b/t two intensities ratio'
    return local_max(x,y,xR2)[1]/local_max(x,y,xR1)[1]