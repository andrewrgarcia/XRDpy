# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:22:43 2018

@author: garci
"""
'''code finds h k l lattice indices for an XRD peak @ a certain 'twotheta' value
given the known a b c lattice parameters of the crystal studied'''

import numpy as np
import math
import mof_lattice_params as mof

from scipy.optimize import minimize

#def braggslaw(twotheta,n):
#
#    '2d sin(theta)=n*lmda'
#
#    twotheta=(np.pi/180)*twotheta
#    lmda = 0.154 #nm
#    
#    d = n*lmda / (2*np.sin(twotheta/2))
#    return d

def braggslaw(twotheta):

    '2d sin(theta)=n*lmda'

    twotheta=(np.pi/180)*twotheta
    lmda = 1.54 #Angstroms
    
    d = lmda / (2*np.sin(twotheta/2))
    return 1/(d**2)


'interplanar space "isp_" functions'
def isp_orthorhombic(h,k,l,a,b,c):

    '1/d_hkl^2 = '
    return h**2/a**2 + k**2/b**2 + l**2/c**2

def isp_cubic(h,k,l,a):

    '1/d_hkl^2 = '
    return (h**2 + k**2 + l**2)/a**2

def isp_tetragonal(h,k,l,a,c):

    '1/d_hkl^2 = '
    return ((h**2 + k**2)/ a**2) + (l**2/c**2) 

def isp_hexagonal(h,k,l,a,c):

    '1/d_hkl^2 = '
    return ((4/3)*(h**2 + h*k + k**2)/a**2) + (l**2/c**2)


def index_search(isp_type,twotheta,tol,args=()):

    n=1
    ds_diff=1

    count =0
    while abs(ds_diff) > tol:
        d=braggslaw(twotheta,n)

        recip_ds=1/d**2

        if count > 1000:
            n+=1
            count=0
        else:
            h,k,l=randint(0,3,(3))

            ds_diff= recip_ds - isp_type(h,k,l,*args)

            print('({} {} {})'.format(h,k,l))
        count +=1


    return h,k,l,n,ds_diff



def find_latticeparams():    
    '''EXAMPLE FOR FINDING LATTICE PARAMETERS FROM POWDER PATTERNS [WHEN H K L INDICES ARE KNOWN]
    (using data from:
        https://cbc-wb01x.chemistry.ohio-state.edu/~woodward/ch754/indexing.pdf
        https://www.researchgate.net/file.PostFileLoader.html?id...assetKey...
        '''
    
    def srfun(x):
        '''Sum of squared residuals function (sqresid)'''
        a,c= x
        
        '''1/d^2 (rld_sq): values for all 2-theta values obtained through Braggs Law'''
        twotheta_list=[27.4344,30.179,36.071,39.1885,41.239,44.0389,56.6232,62.7525,64.0439,68.9969]
        rld_sq=[braggslaw(twotheta_list[i]) for i in range(len(twotheta_list))]
    
        
        '''1/d_hkl^2 (rlhkl_sq):  values obtained using lattice equation and hkl values obtained from indexing'''
        'structure name'
        isp_type = isp_tetragonal
        hkllist = [(1,1,0),(0,0,1),(1,0,1),(2,0,0),(1,1,1),(2,1,0),(2,2,0),(0,0,2),(3,1,0),(3,0,1)]   
        rlhkl_sq = [isp_type(*indices,a,c) for indices in hkllist]
    
        sqresid=0
        for i,j in zip(rld_sq,rlhkl_sq):
            sqresid += (i-j)**2
            
        return sqresid 
    
    x0=[1,1]
    sol = minimize(srfun,x0)
    
    return sol
    
print(find_latticeparams())
print('lattice parameters are:',find_latticeparams().x)

#twotheta,a,b,c = mof.param()
#
#'sjoegrenite'
##twotheta,a,c = 11.33, 3.113, 15.61
#
#ix=index_search(isp_orthorhombic,twotheta,tol=1e-3,args=(a,b,c))
##ix=index_search(isp_hexagonal,twotheta,tol=1e-3,args=(a,c))
#
#
#d=braggslaw(twotheta,ix[3])
#
#print('2-theta = {} \nh,k,l indices: {} \nn (order): {} \nerror: {} \nint. spacing: {} nm'.format(twotheta,ix[0:3],ix[3],ix[4],d))
