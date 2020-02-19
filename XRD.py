# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 22:16:03 2018

@author: garci
"""
'''XRDpy - A module for X-Ray Diffraction (XRD) pattern analysis
Andrew Garcia, 2018
Last edit: 02/18/2020'''

import csv
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib.pyplot import xticks
from matplotlib.font_manager import FontProperties
from XRD_functions import *

import pandas

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path_database_file", \
                default = r'C:\Users\garci\DROPBO~2\scripts\XRD\database_template.xlsx',\
                type = str, help="Path and filename of Excel database which is used\
                to call all your files. Please update with your path and databse file name.")
ap.add_argument("-p2", "--path_files_folder", \
                default = r'C:\Users\garci\DROPBO~2\scripts\XRD\XRD-patterns-fake/',\
                type = str, help="path to FOLDER containing XRD files listed in Excel database'")
ap.add_argument("-d", "--see_database", default = False,
                help="see database only ")
ap.add_argument("-ka", "--K_alpha_wavelength", default = 0.154, type = float,
                help = "wavelength of K-alpha radiation default Cu-Ka (nm)")
ap.add_argument("-b", "--background_sub", default = True, 
                help="background subtraction")
ap.add_argument("-o", "--overlaid", default = -1, nargs = '+', type=str,
                help="sample names for overlaid plots")
ap.add_argument("-x", "--overlaid_split", default = 1, nargs = '+', type =int,
                help="split - number of plots per overlaid chart (i.e. 2 3 for 2 in first and 3 in third overlaid chart)")
ap.add_argument("-s", "--single", default = -1, nargs = '+',type=str,
                help="sample names for individual plots")
ap.add_argument("-u", "--units", default = '', type = str,
                help="x axis units (type angle OR braggs)")
ap.add_argument("-r", "--Scherrer_range", default = -1, nargs = '+', type =float,
                help="x axis units (type angle OR braggs)")
ap.add_argument("-K", "--shape_factor_K", default = 0.9, type = float,
                help = "for Scherrer length calculation; shape factor 'K'")
args = vars(ap.parse_args())


'''Excel database:
see database_template.xlsx in this repository for an easy-to-edit template
compatible with the XRD.py program'''
def database():
    'path to Excel database'
    return pandas.read_excel(args["path_database_file"])


def data(dbase,index_file):
    '''files: .csv file NAMES'''

    filename= dbase()['file'][index_file]

    '''specify path'''
    fname_path=args["path_files_folder"]

    with open( fname_path+filename , 'r') as f:
        x = list(csv.reader(f, delimiter=","))

    return np.array(x[1:], dtype=np.float)


def make(dbase):

    labels=list(dbase()['name'])

    '''labels_for_csvfiles: returns vector of labels chosen for each of the .csv files in csvfiles
    in the string form of ['xxx', ... , ...., ..., 'xxx']'''

    # overlaidvec,indiv, ncharts = selectn()
    
    indiv, ncharts = args["single"], len(args["overlaid_split"])+len(args["single"])

    for i in range(len(indiv)):
        indiv[i] = labels.index(indiv[i])

    start_ov = args["overlaid"]
    for i in range(len(start_ov)):
        start_ov[i] = labels.index(start_ov[i])

    overlaidvec = []
    for i in args["overlaid_split"]:

        overlaidvec.append(start_ov[:i]+['empty']*(5-len(start_ov[:i]) ))
        start_ov = start_ov[i:]


    print(overlaidvec)


#    f, axarr = plt.subplots(4, sharex=True,gridspec_kw={'height_ratios':[3.14,1,1,1]})
    if ncharts == 3:
        f, axarr = plt.subplots(ncharts, sharex=True)
#        f, axarr = plt.subplots(ncharts, sharex=True,gridspec_kw={'height_ratios':[2,1,1]})
    else:
        f, axarr = plt.subplots(ncharts, sharex=True)

    oneoplt = (len(overlaidvec) != np.size(overlaidvec))

    lovec = len(overlaidvec) if oneoplt else 1
    for j in range(lovec):

        overlaid = overlaidvec[j] if oneoplt else overlaidvec

        for i in range(0,100):

            if any([ i==overlaid[0], i==overlaid[1], i==overlaid[2], i==overlaid[3], i==overlaid[4] ]):


    #            ydat,xdat = np.shape(data()[i])
                ydat,xdat = np.shape(data(dbase,i))

                x, y, yb = np.zeros((3,ydat))
    #            x, y = data()[i][:,0], data()[i][:,1]
                x, y = data(dbase,i)[:,0], data(dbase,i)[:,1]

                if args["background_sub"] is True:
                    yb=backsub(x,y,tol=1)
                    x,yb = movnavg(x,yb)
                else:
                    yb=y
                    
                if ncharts == 1:
                    pax = axarr
                else:
                    pax = axarr[j] if oneoplt else axarr[0]

                if args["units"] == 'braggs':
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


#        ix=1
        ix=1+(lovec-1) if lovec > 1 else 1
        for i in indiv:

            print(labels[i])

                
#            rydat,rxdat = np.shape(data()[i])
            rydat,rxdat = np.shape(data(dbase,i))

            rx, ry, ryb = np.zeros((3,rydat))
#            rx, ry = data()[i][:,0], data()[i][:,1]
            rx, ry = data(dbase,i)[:,0], data(dbase,i)[:,1]

            if args["background_sub"] is True:
                ryb=backsub(rx,ry,tol=1.0)
                rx,ryb = movnavg(rx,ryb)
            else:
                ryb=ry

            
            if args["Scherrer_range"] is not -1:
                ls,hs=args["Scherrer_range"]
                print('---CRYSTALLITE SIZE CALCULATION - SCHERRER WIDTH---')

                Sch,xseg,yseg = schw_peakcal(rx,ryb,args["shape_factor_K"],\
                                             args["K_alpha_wavelength"],[ls,hs])

                print('\nSCHERRER WIDTH: {} nm\n\n'.format(Sch))

            if args["units"] == 'braggs':
                axarr[ix].plot(braggs(rx),ryb,label=labels[i]) 
#                axarr[ix].plot(rx,ryb,label=labels[i],color='k')
                
            else:
                axarr[ix].plot(rx,ryb,label=labels[i]) 
                axarr[ix].plot(xseg,yseg,color='m') if args["Scherrer_range"] is not -1 else None

            axarr[ix].legend(loc='best')


#            print('Intensity ratio: {} \n'.format(XRD_int_ratio(rx,ryb)))

            ix+=1


    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

    if args["units"] == 'braggs':
        plt.xlabel(r'Interplanar lattice spacing / $\AA$')
    else:
        plt.xlabel(r'$2\theta$ / deg')

    plt.ylabel('Intensity / a.u.')
    plt.show()

def make_s(dbase):
    
    labels=list(dbase()['name'])

    '''labels_for_csvfiles: returns vector of labels chosen for each of the .csv files in csvfiles
    in the string form of ['xxx', ... , ...., ..., 'xxx']'''
  
    indiv, ncharts = args["single"], len(args["single"])

    for i in range(len(indiv)):
        indiv[i] = labels.index(indiv[i])

#    f, axarr = plt.subplots(4, sharex=True,gridspec_kw={'height_ratios':[3.14,1,1,1]})
    if ncharts == 3:
        f, axarr = plt.subplots(ncharts, sharex=True)
#        f, axarr = plt.subplots(ncharts, sharex=True,gridspec_kw={'height_ratios':[2,1,1]})
    else:
        f, axarr = plt.subplots(ncharts, sharex=True)

    
    if ncharts != 1:

        indiv = indiv[-(ncharts):]

        ix=0

        for i in indiv:

            print(labels[i])

                
            rydat,rxdat = np.shape(data(dbase,i))

            rx, ry, ryb = np.zeros((3,rydat))
            rx, ry = data(dbase,i)[:,0], data(dbase,i)[:,1]

            if args["background_sub"] is True:
                ryb=backsub(rx,ry,tol=1.0)
                rx,ryb = movnavg(rx,ryb)
            else:
                ryb=ry

            
            if args["Scherrer_range"] is not -1:
                ls,hs=args["Scherrer_range"]
                print('---CRYSTALLITE SIZE CALCULATION - SCHERRER WIDTH---')

                Sch,xseg,yseg = schw_peakcal(rx,ryb,args["shape_factor_K"],\
                                             args["K_alpha_wavelength"],[ls,hs])

                print('\nSCHERRER WIDTH: {} nm\n\n'.format(Sch))

            if args["units"] == 'braggs':
                axarr[ix].plot(braggs(rx),ryb,label=labels[i]) 
#                axarr[ix].plot(rx,ryb,label=labels[i],color='k')
                
            else:
                axarr[ix].plot(rx,ryb,label=labels[i]) 
                axarr[ix].plot(xseg,yseg,color='m') if args["Scherrer_range"] is not -1 else None

            axarr[ix].legend(loc='best')


            ix+=1


    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

    if args["units"] == 'braggs':
        plt.xlabel(r'Interplanar lattice spacing / $\AA$')
    else:
        plt.xlabel(r'$2\theta$ / deg')

    plt.ylabel('Intensity / a.u.')
    plt.show()

'''execution of code:
display database alone or display database and make plots'''
pandas.set_option('display.max_rows', 100)
print(database()['name'],'\n')

if args["see_database"] is False:
    if args["overlaid"] is -1:
        make_s(database)
    else:
        make(database)

