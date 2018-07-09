# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:22:43 2018

@author: garci
"""
'''code finds h k l lattice indices for an XRD peak @ a certain 'twotheta' value
given the known a b c lattice parameters of the crystal studied'''

import numpy as np
import math
import lattice_params as mof

def braggslaw(twotheta,n):

    '2d sin(theta)=n*lmda'

    twotheta=(np.pi/180)*twotheta
    lmda = 0.154 #nm
    d = n*lmda / (2*np.sin(twotheta/2))
    return d

def intspace_orthorhombic(h,k,l,a,b,c):

    '1/d_hkl^2 = '
    return h**2/a**2 + k**2/b**2 + l**2/c**2

def intspace_cubic(h,k,l,a):

    '1/d_hkl^2 = '
    return (h**2 + k**2 + l**2)/a**2

def intspace_hexagonal(h,k,l,a,c):

    '1/d_hkl^2 = '
    return ((4/3)*(h**2 + h*k + k**2)/a**2) + (l**2/c**2)

def index_search(twotheta,tol,args=()):

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
            h,k,l=randint(0,5,(3))

#            ds_diff= recip_ds - intspace_orthorhombic(h,k,l,*args)
            ds_diff= recip_ds - intspace_hexagonal(h,k,l,*args)

            print('({} {} {})'.format(h,k,l))
        print('n = ',n)
        count +=1


    return h,k,l,n,ds_diff

#twotheta=9.35
#twotheta=12.54
#a,b,c = mof.param()

'sjoegrenite'
twotheta=11.3
a = 3.113
c = 15.61


ix=index_search(twotheta,tol=1e-4,args=(a,c))
d=braggslaw(twotheta,ix[3])

print('h,k,l indices: {} \nn (order): {} \nresolution {} \nint. spacing: {} nm'.format(ix[0:3],ix[3],ix[4],d))
