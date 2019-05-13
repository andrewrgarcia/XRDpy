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

'''Get your own database! ha!
(You may start by cloning the template XRD_database_template.py)'''
from XRD_mydatabase import csvfiles, labels_for_csvfiles


labels= labels_for_csvfiles()



def data(index_file):
    '''csvfiles: vector of .csv file NAMES in the string form of
    [ 'sample_1 .csv ', .... , 'sample_N .csv'] '''
    
    filename=csvfiles()[index_file]
    '''if the csv files are in a subfolder to this script's, specify path'''
    fname_path='XRD_files/'

    with open( fname_path+filename , 'r') as f:
        x = list(csv.reader(f, delimiter=","))

    return np.array(x[1:], dtype=np.float)



def plotting(xaxis_units='braggs'):

    labels=labels_for_csvfiles()
    '''labels_for_csvfiles: returns vector of labels chosen for each of the .csv files in csvfiles
    in the string form of ['xxx', ... , ...., ..., 'xxx']'''
    
    I,ind_items, ncharts = selection()

#    f, axarr = plt.subplots(4, sharex=True,gridspec_kw={'height_ratios':[3.14,1,1,1]})
    if ncharts == 3:
        f, axarr = plt.subplots(ncharts, sharex=True)
#        f, axarr = plt.subplots(ncharts, sharex=True,gridspec_kw={'height_ratios':[2,1,1]})
    else:
        f, axarr = plt.subplots(ncharts, sharex=True)

    

    for i in range(0,100):

        if any([ i==I[0], i==I[1], i==I[2], i==I[3], i==I[4] ]):


#            ydat,xdat = np.shape(data()[i])
            ydat,xdat = np.shape(data(i))

            x, y, yb = np.zeros((3,ydat))
#            x, y = data()[i][:,0], data()[i][:,1]
            x, y = data(i)[:,0], data(i)[:,1]


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

        ind_items = ind_items[-(ncharts-1):]


        ix=1
        for i in ind_items:

#            rydat,rxdat = np.shape(data()[i])
            rydat,rxdat = np.shape(data(i))

            rx, ry, ryb = np.zeros((3,rydat))
#            rx, ry = data()[i][:,0], data()[i][:,1]
            rx, ry = data(i)[:,0], data(i)[:,1]

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



from XRD_mydatabase import select

#def select():
#    
#    '''FIRST CHART (OVERLAID PLOTS)'''
#    
#    oplts = [
#            list.index(labels,'example 1'),
#            list.index(labels,'example 2'),
#            list.index(labels,'example 3')
#            ]
#    
#    
#    [oplts.append('empty') for i in range(5)]
#    
#
#    '''---------------------------------------------------------------'''
#
#    '''NEXT CHARTS BEYOND FIRST (INDIVIDUAL PLOTS PER CHART)'''
#    
#    iplts = [
#            list.index(labels,'example 1'),
#            list.index(labels,'example 5')
#            ]
#    
#    '''---------------------------------------------------------------'''
#    n = 1 + len (iplts)
#
#    oplts,iplts,n


def selection():    
    
    oplts,iplts,n = select()
        
    return oplts,iplts,n


#plotting('braggs')
plotting('')
