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
from  matplotlib.pyplot import xticks
from matplotlib.font_manager import FontProperties
from XRD_functions import *


from XRD_database import database, select
'''Make your own database script! ha!
check the Jupyter notebook in this same repository for some help on that...'''


fpath = r'C:\Users\garci\Dropbox (UFL)\Research\XRD\_files/'
def data(dbase,index_file):
    '''files: .csv file NAMES'''
    
    filename= dbase()['file'][index_file]

    '''specify path'''
    fname_path=fpath

    with open( fname_path+filename , 'r') as f:
        x = list(csv.reader(f, delimiter=","))

    return np.array(x[1:], dtype=np.float)



def make(dbase,selectn,xaxis_units='braggs'):

    labels=dbase()['name']

    '''labels_for_csvfiles: returns vector of labels chosen for each of the .csv files in csvfiles
    in the string form of ['xxx', ... , ...., ..., 'xxx']'''
    
    overlaid,indiv, ncharts = selectn()

#    f, axarr = plt.subplots(4, sharex=True,gridspec_kw={'height_ratios':[3.14,1,1,1]})
    if ncharts == 3:
        f, axarr = plt.subplots(ncharts, sharex=True)
#        f, axarr = plt.subplots(ncharts, sharex=True,gridspec_kw={'height_ratios':[2,1,1]})
    else:
        f, axarr = plt.subplots(ncharts, sharex=True)

    

    for i in range(0,100):

        if any([ i==overlaid[0], i==overlaid[1], i==overlaid[2], i==overlaid[3], i==overlaid[4] ]):


#            ydat,xdat = np.shape(data()[i])
            ydat,xdat = np.shape(data(dbase,i))

            x, y, yb = np.zeros((3,ydat))
#            x, y = data()[i][:,0], data()[i][:,1]
            x, y = data(dbase,i)[:,0], data(dbase,i)[:,1]


            yb=backsub(x,y,tol=1)
            x,yb = movnavg(x,yb)

            if ncharts == 1:
                pax = axarr
            else:
                pax = axarr[0]

            if xaxis_units == 'braggs':
#                pax.plot(braggs(x),yb,label=labels[i])
                pax.plot(x,yb,label=labels[i])
                
                locs, tickls = xticks()
                
               
                print(braggs(locs))
                print(locs)
                xticks(locs,braggs(locs))


            else:
                pax.plot(x,yb,label=labels[i])
                
                


#            axarr.plot(x,yb,label=labels[i],color='k')
            pax.legend(loc='best')

            print(labels[i])

#            print('Scherrer width: {} nm'.format(schw_peakcal(x,yb,[17,18])))
#            print('Intensity ratio: {} \n'.format(XRD_int_ratio(x,yb)))


    if ncharts != 1:

        indiv = indiv[-(ncharts-1):]


        ix=1
        for i in indiv:

#            rydat,rxdat = np.shape(data()[i])
            rydat,rxdat = np.shape(data(dbase,i))

            rx, ry, ryb = np.zeros((3,rydat))
#            rx, ry = data()[i][:,0], data()[i][:,1]
            rx, ry = data(dbase,i)[:,0], data(dbase,i)[:,1]

            ryb=backsub(rx,ry,tol=1.0)
            rx,ryb = movnavg(rx,ryb)

            if xaxis_units == 'braggs':
#                axarr[ix].plot(braggs(rx),ryb,label=labels[i],color='k')
                
                axarr[ix].plot(rx,ryb,label=labels[i],color='k')


            else:
                axarr[ix].plot(rx,ryb,label=labels[i],color='k')

            axarr[ix].legend(loc='best')

            print(labels[i])
#            print('Scherrer width: {} nm'.format(schw_peakcal(rx,ryb,[17,18])))
#            print('Intensity ratio: {} \n'.format(XRD_int_ratio(rx,ryb)))

            ix+=1


    print('\n*Crystallite size calculated using Scherrer equation.')



    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

    if xaxis_units == 'braggs':
        plt.xlabel(r'Interplanar lattice spacing / $\AA$')
    else:
        plt.xlabel(r'$2\theta$ / deg')

    plt.ylabel('Intensity / a.u.')


#def selection():    
#    
#    oplts,iplts,n = select()
#        
#    return oplts,iplts,n


make(database,select,'')