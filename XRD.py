# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 22:16:03 2018

@author: garci
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from confidential_XRD import csvfiles, labels_for_csvfiles

def scherrer(K,lmda,beta,theta):
        
    return K*lmda / (beta*np.cos(theta))    #tau

def local_max(x,y,xrange=[12,13]): 
    'find local maxima'
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

def XRD_int_ratio(x,y,xR1=[8.88,9.6],xR2=[10.81,11.52]):
    'XRD b/t two intensities ratio'
    return local_max(x,y,xR2)[1]/local_max(x,y,xR1)[1]


def data():
    
    filename=csvfiles()
    '''csvfiles: returns vector of .csv file names in the string form of 
    [" xxx .csv", ... , ...., ..., "xxx.csv"]'''

    M=len(filename)
    X = [[]]*M

    for i in range(M):
        with open(filename[i], 'r') as f:
            X[i] = list(csv.reader(f, delimiter=","))
        
    for i in range(M):
            X[i] = np.array(X[i][1:], dtype=np.float)

    return X

    labels=labels_for_csvfiles()
    '''labels_for_csvfiles: returns vector of labels chosen for each of the .csv files in csvfiles
    in the string form of ['xxx', ... , ...., ..., 'xxx']'''


#f, axarr = plt.subplots(4, sharex=True,gridspec_kw={'height_ratios':[3.14,1,1,1]})
f, axarr = plt.subplots(3, sharex=True,gridspec_kw={'height_ratios':[2,1,1]})


for i in range(2,16):
#for i in range(27,35):

        
#    if any([i==8,i==10, i==11, i==12,i==13]):

        ydat,xdat = np.shape(data()[i])
        x, y, yb = np.zeros((3,ydat))
        x=data()[i][:,0]
        y=data()[i][:,1]
        yb=bacsub(x,y,tol=1)
        x,yb = movnavg(x,yb)
        
        
        axarr[0].plot(x,yb,label=labels[i])
        axarr[0].legend(loc='best')   
        
        print(labels[i])
        print('Sc width: {} nm'.format(schw_peakcal(x,yb)))
        print('C11/C9: {} \n'.format(XRD_int_ratio(x,yb)))


for i in range(2):
    rydat,rxdat = np.shape(data()[i+1])
    rx, ry, ryb = np.zeros((3,rydat))
    rx=data()[i+1][:,0]
    ry=data()[i+1][:,1]
    ryb=bacsub(rx,ry,tol=1)
    rx,ryb = movnavg(rx,ryb)

    axarr[i+1].plot(rx,ryb,label=labels[i+1],color='k')
    axarr[i+1].legend(loc='best')
    
#    print(labels[i])
#    schw_peakcal(rx,ryb)
    
print('\n*Crystallite size calculated using Scherrer equation.')
    
axarr[1].set_ylim([-1000, 20000])


f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)


plt.xlabel(r'$2\theta$ / deg')
plt.ylabel('Intensity / a.u.')