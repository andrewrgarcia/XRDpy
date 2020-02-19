# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 21:00:03 2018

@author: garci
"""
'''XRDpy - A module for X-Ray Diffraction (XRD) pattern analysis
Andrew Garcia, 2018
Last edit: 02/18/2020'''

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.signal import argrelextrema

from XRD_functions import *


import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", \
                default = r'C:\Users\garci\DROPBO~2\scripts\XRD\XRD-patterns-fake/',\
                type = str, help="path where all your csv files may be. \
                Please update the default with your common folder.")
ap.add_argument("-s", "--file_name",\
                default = 'sample1.csv', type = str, help = "your file's name \
                located in the defined path")

ap.add_argument("-ka", "--K_alpha_wavelength", default = 0.154, type = float,
                help = "wavelength of K-alpha radiation default Cu-Ka (nm)")
ap.add_argument("-se", "--second_emission", default = False, type = bool,
                help="remove secondary emission peaks (K-beta) ")
ap.add_argument("-kb", "--K_beta_wavelength", default = 0.139, type = float,
                help = "wavelength of secondary emission (nm)")        
  
ap.add_argument("-b", "--background_sub", default = True,
                help="background subtraction")
ap.add_argument("-xl", "--toexcel", default = False, type=bool,
                help="make an Excel copy of treated XRD pattern (background subtraction OR\
                back. subtraction and 2ry emission peaks subtraction")
                
ap.add_argument("-r", "--Scherrer_range", default = -1, nargs = '+', type =float,
                help="x axis units (type angle OR braggs)")
ap.add_argument("-K", "--shape_factor_K", default = 0.9, type = float,
                help = "for Scherrer length calculation; shape factor 'K'")

args = vars(ap.parse_args())


def data( path ):
    
    '''specify path of file'''    
    with open(path, 'r') as f:
        X = list(csv.reader(f, delimiter=","))        
    Xc=np.array(X[1:], dtype=np.float)        

    return Xc, np.shape(Xc)

'EXCEL'
import xlwings as xw

def excel(x,y):
    wb=xw.Book()
    xw.Range((1,1)).options(transpose=True).value=x
    xw.Range((1,2)).options(transpose=True).value=y

def make0():
    
    xi=data(args["path"]+args["file_name"])[0][:,0]
    yi=data(args["path"]+args["file_name"])[0][:,1]
    ybi=backsub(xi,yi,tol=1.00)
    
    
    if args["second_emission"] is True:
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
            
            Kbeta = \
            emission_lines_plt(xi_lm,\
            ybi_lm,twothet_range_Ka=[xi_lm[i]-0.1,xi_lm[i]+0.1],plt='n',\
            lmda_Ka = args["K_alpha_wavelength"],lmda_Ki=args["K_beta_wavelength"])
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
        
                
        'Plot #2'
        plt.figure()
        plt.plot(xi,ybi_t0,color='b',label='smoothed plot for Kbeta analysis')
        plt.plot(xi_lm,ybi_lm,'ro',label='local maxima')
        
        ##plt.title('')
        plt.xlabel(r'$2\theta$ / deg')
        plt.ylabel('Intensity / a.u.')
        plt.legend(loc='best')
        
        'Plot #3'
        plt.figure()
        
        #plt.plot(xi,ybi_t,color='navy',label=r'subtracted peaks from $K_\beta$ emission')
        plt.plot(xi,ybi_t,color='C1')
        
        ###plt.title('')
        plt.xlabel(r'$2\theta$ / deg')
        plt.ylabel('Intensity / a.u.')
        plt.legend(loc='best')

                
        'END CODE BLOCK'
        
    plt.figure()
    plt.xlabel(r'$2\theta$ / deg')
    plt.ylabel('Intensity / a.u.')
#    plt.legend(loc='best')
    if args["background_sub"] is True:
        plt.plot(xi,ybi,label='background-subtracted')
    else:
        plt.plot(xi,yi,label='raw pattern')
    
       
    if args["Scherrer_range"] is not -1:
        ls,hs=args["Scherrer_range"]
        print('---CRYSTALLITE SIZE CALCULATION - SCHERRER WIDTH---')
        
        if args["background_sub"] is True:
            Sch,xseg,yseg = schw_peakcal(xi,ybi,args["shape_factor_K"],\
                                     args["K_alpha_wavelength"],[ls,hs])
        else:
            Sch,xseg,yseg = schw_peakcal(xi,yi,args["shape_factor_K"],\
                         args["K_alpha_wavelength"],[ls,hs])
        print('\nSCHERRER WIDTH: {} nm'.format(Sch))

        plt.plot(xseg,yseg,color='m')
#        plt.legend(loc='best')

    if args["toexcel"] is True:
        if args["second_emission"] is True:
            excel(xi,ybi_t)
        else: 
            excel(xi,ybi)
    
    plt.show()
        
make0()