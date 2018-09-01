# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 22:16:03 2018

@author: garci
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from XRD_functions import *

'Get[/build] your own database! (A collection of XRD files in .csv format)'
from XRD_mydatabase import csvfiles, labels_for_csvfiles

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


def plotting():
    
    labels=labels_for_csvfiles()
    '''labels_for_csvfiles: returns vector of labels chosen for each of the .csv files in csvfiles
    in the string form of ['xxx', ... , ...., ..., 'xxx']'''
    
    f, axarr = plt.subplots(4, sharex=True,gridspec_kw={'height_ratios':[3.14,1,1,1]})
#    f, axarr = plt.subplots(3, sharex=True,gridspec_kw={'height_ratios':[2,1,1]})
    
    

#    for i in range(2,16):
    for i in range(0,8):
           
#        if any([i==14,i==19, i==21]):
#        if any([i==2,i==37,i==38]):
#        if any([i==2, i==5,i==8]):


    
            ydat,xdat = np.shape(data()[i])
            x, y, yb = np.zeros((3,ydat))
            x, y = data()[i][:,0], data()[i][:,1]
            
            yb=bacsub(x,y,tol=1)
            x,yb = movnavg(x,yb)
            
            axarr[0].plot(x,yb,label=labels[i])
            axarr[0].legend(loc='best')   
            axarr[0].set_xlim(8.5)
#            twothet_Ka_deg, int_Ka, twothet_Ki_deg = emission_lines(x, yb,twothet_range_Ka=[10,13])
#            axarr[0].vlines(twothet_Ka_deg,0,int_Ka, colors='k', linestyles='solid')
#            axarr[0].vlines((twothet_Ka_deg+twothet_Ki_deg)/2,0,int_Ka, colors='k', linestyles='--')
#            axarr[0].vlines(twothet_Ki_deg,0,int_Ka, colors='r', linestyles='solid')
            
            print(labels[i])
            print('Scherrer width: {} nm'.format(schw_peakcal(x,yb)))
            print('Intensity ratio: {} \n'.format(XRD_int_ratio(x,yb)))
    
    
    for i in range(3):
        rydat,rxdat = np.shape(data()[i])
        rx, ry, ryb = np.zeros((3,rydat))
        rx, ry = data()[i][:,0], data()[i][:,1]
        ryb=bacsub(rx,ry,tol=1)
        rx,ryb = movnavg(rx,ryb)
    
        axarr[i+1].plot(rx,ryb,label=labels[i],color='k')
        axarr[i+1].legend(loc='best')
        
#        print(labels[i])
#        schw_peakcal(rx,ryb)
        
    print('\n*Crystallite size calculated using Scherrer equation.')
        
    axarr[1].set_ylim([-1000, 20000])
    axarr[2].set_ylim([-100, 4000])

    
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    
    plt.xlabel(r'$2\theta$ / deg')
    plt.ylabel('Intensity / a.u.')
    
    
plotting()