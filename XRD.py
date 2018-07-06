# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 22:16:03 2018

@author: garci
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def scherrer(K,lmda,beta,theta):
    return K*lmda / (beta*np.cos(theta))    #tau

def locmax (x,y,x1=12,x2=13): 
    
    xsearch_index=[]
    for n in x:
        if n >= x1 and  n <= x2:
            xsearch_index.append(list(x).index(n))
    
    max_y = 0
    max_2theta = 0
    for i in xsearch_index:
        if y[i] > max_y:
            max_y = y[i]
            max_2theta = x[i]
    
    hm = max_y/2
    theta=max_2theta/2
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
    
    s=scherrer(0.9,1.54,beta,theta)
    print('size*: {} nm'.format(s))
            

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
                    
def data():
    
    filename=["dstape_perm.csv","dstape_rmvl.csv","MIL53-adv-001.csv","MIL53-adv-006.csv","MIL53-adv-006-uncalcined.csv",
              "MIL53-adv-008.csv","MIL53-adv-010.csv","MIL53-adv-011.csv","MIL53-adv-013.csv","MIL002-C-5umf-C.csv",
              "MIL003-C-5umf-C.csv","MIL004-C-5umf-C.csv","MIL53-adv-016.csv","MIL53-adv-016_hires.csv","MIL53-adv-017.csv",
              "MIL53-adv-019.csv","MIL53-adv-020.csv","MIL53-adv-021.csv","mil_pwc.csv"]
    

    M=len(filename)
    X = [[]]*M

    for i in range(M):
        with open(filename[i], 'r') as f:
            X[i] = list(csv.reader(f, delimiter=","))
        
    for i in range(M):
            X[i] = np.array(X[i][1:], dtype=np.float)

    return X


labels=['3M double-sided tape (Permanent)','3M double-sided tape (Removable)',
        'MIL 1','MIL 6','MIL 6_as','MIL 8','MIL 10','MIL 11',
        'MIL 13','MIL 2 C5umfC','MIL 3 C5umfC','MIL 4 C5umfC',
        'MIL 16', 'MIL 16 (hi-res)','MIL 17','MIL 19', 'MIL 20', 'MIL 21','MIL (simulation)']


f, axarr = plt.subplots(4, sharex=True,gridspec_kw={'height_ratios':[3.14,1,1,1]})
#f, axarr = plt.subplots(2, sharex=True,gridspec_kw={'height_ratios':[8,4]})


for i in range(2,18):
    
    '''only plot data w/ following indices'''
    if any([i ==2, i==13, i==14, i==15, i==16, i ==17]):

        
        ydat,xdat = np.shape(data()[i])
        x, y, yb = np.zeros((3,ydat))
        x=data()[i][:,0]
        y=data()[i][:,1]
        yb=bacsub(x,y,tol=1)
        x,yb = movnavg(x,yb)
        
#        plt.plot(x,yb,label=labels[i])
#        plt.legend(loc='best')   
        
        
        axarr[0].plot(x,yb,label=labels[i])
        axarr[0].legend(loc='best')   
        
        print(labels[i])
        locmax(x,yb)


for i in range(3):
    rydat,rxdat = np.shape(data()[i])
    rx, ry, ryb = np.zeros((3,rydat))
    rx=data()[i][:,0]
    ry=data()[i][:,1]
    ryb=bacsub(rx,ry,tol=1)
    rx,ryb = movnavg(rx,ryb)

    axarr[i+1].plot(rx,ryb,label=labels[i],color='k')
    axarr[i+1].legend(loc='best')
    
#    print(labels[i])
#    locmax(rx,ryb)
    
#print('\n*Crystallite size calculated using Scherrer equation.')
    
axarr[1].set_ylim([-1000, 20000])


f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)


plt.xlabel(r'$2\theta$ / deg')
plt.ylabel('Intensity / a.u.')