# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 22:16:03 2018

@author: garci
"""
'''XRD.py - A program for X-Ray Diffraction (XRD) pattern analysis using Python
Andrew Garcia, 2018'''

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from XRD_functions import *

'''Get your own database! ha!
(You may start by cloning the template XRD_database_template.py)'''
from XRD_mydatabase import csvfiles, labels_for_csvfiles


labels= labels_for_csvfiles()

def data():
    '''csvfiles: returns vector of .csv file names in the string form of 
    [" sample_1 .csv ", ... , ...., ..., " sample_N .csv "]'''
    filename=csvfiles()
    
    '''if the csv files are in a subfolder to this script's, specify path'''
    fname_path='XRD_files/'


    M=len(filename)
    X = [[]]*M

    for i in range(M):
        with open( fname_path+filename[i] , 'r') as f:
            X[i] = list(csv.reader(f, delimiter=","))
        
    for i in range(M):
            X[i] = np.array(X[i][1:], dtype=np.float)

    return X


def plotting(nplots=3,xax=''):
    
    labels=labels_for_csvfiles()
    '''labels_for_csvfiles: returns vector of labels chosen for each of the .csv files in csvfiles
    in the string form of ['xxx', ... , ...., ..., 'xxx']'''
    

#    f, axarr = plt.subplots(4, sharex=True,gridspec_kw={'height_ratios':[3.14,1,1,1]})
    if nplots == 3:
        f, axarr = plt.subplots(nplots, sharex=True)
#        f, axarr = plt.subplots(nplots, sharex=True,gridspec_kw={'height_ratios':[2,1,1]})
    else:
        f, axarr = plt.subplots(nplots, sharex=True)
        


    for i in range(0,100):
           
        
        I=['empty']*5
#        I[0]=list.index(labels,'Comm M')
#        I[1]=list.index(labels,'M 1')
#        I[2]=list.index(labels,'M 28')
#        I[2]=list.index(labels,'M 1')
        
#        I[0]=list.index(labels,'M 21 as')
#        I[0]=list.index(labels,'M 28 as')
        I[1]=list.index(labels,'M 29 (ground on M)')        
#        I[2]=list.index(labels,'M B2 as (ground)')

                
        if any([ i==I[0], i==I[1], i==I[2], i==I[3], i==I[4] ]):

    
            ydat,xdat = np.shape(data()[i])
            x, y, yb = np.zeros((3,ydat))
            x, y = data()[i][:,0], data()[i][:,1]
            
            yb=backsub(x,y,tol=1.0)
            x,yb = movnavg(x,yb)
            
            if nplots == 1: 
                pax = axarr
            else:
                pax = axarr[0]
            
            if xax == 'braggs':
                pax.plot(braggs(x),yb,label=labels[i],color='k')

            else:
                pax.plot(x,yb,label=labels[i])

            
#            axarr.plot(x,yb,label=labels[i],color='k')
            pax.legend(loc='best')   

            
            print(labels[i])
            print('Scherrer width: {} nm'.format(schw_peakcal(x,yb,[17,18])))
            print('Intensity ratio: {} \n'.format(XRD_int_ratio(x,yb)))
    
    
    if nplots != 1: 
    
        i1=list.index(labels,'M 29')
        i2=list.index(labels,'M 28')
#        i3=list.index(labels,'M 22 as (reference)')
        i3=list.index(labels,'M 1')
    
    
        ind_items = [i1,i2,i3]
        
        ind_items = ind_items[-(nplots-1):]
        
        
        ix=1
        for i in ind_items:
            
            rydat,rxdat = np.shape(data()[i])
            rx, ry, ryb = np.zeros((3,rydat))
            rx, ry = data()[i][:,0], data()[i][:,1]
            ryb=backsub(rx,ry,tol=1.0)
            rx,ryb = movnavg(rx,ryb)
            
            if xax == 'braggs':
                axarr[ix].plot(braggs(rx),braggs(ryb),label=labels[i],color='k')
            else:
                axarr[ix].plot(rx,ryb,label=labels[i],color='k')
            
            axarr[ix].legend(loc='best')
            
            print(labels[i])
            print('Scherrer width: {} nm'.format(schw_peakcal(rx,ryb,[17,18])))
            print('Intensity ratio: {} \n'.format(XRD_int_ratio(rx,ryb)))
            
            ix+=1
        
        
    print('\n*Crystallite size calculated using Scherrer equation.')


    
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    
    plt.xlabel(r'$2\theta$ / deg')
    plt.ylabel('Intensity / a.u.')
    
    
plotting(4)