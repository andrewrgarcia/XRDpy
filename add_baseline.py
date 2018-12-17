# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 23:23:55 2018

@author: garci
"""
import numpy as np
import csv
import xlwings as xw
''' an algorithm for adding a flat baseline (values of zero) to array 
with characteristic values [helps to create simulated peaks]'''
X=[]

with open( 'XRD_files/sample.csv' , 'r') as f:
    X = list(csv.reader(f, delimiter=","))


x,y = np.transpose(X)
#x,y = list(x),list(y)  

print(y)


def excel(x,y):
    wb=xw.Book()
    xw.Range((1,1)).options(transpose=True).value=x
    xw.Range((1,2)).options(transpose=True).value=y


def insertion(x,x_b,y,y_b,N):
    for i in range(len(x)):
        elem_x=float(x[i])
        elem_y=float(y[i])

        k=0
        while k<N: 
            if elem_x > x_b[k] and elem_x < x_b[k+1]:
                x_b.insert(k+1,elem_x)
                y_b.insert(k+1,elem_y)
                k=N
            else:
                k+=1
            
    return x_b,y_b

def make(start,end,interval):    
    
    N =(end-start+1)/(interval)
    
    x_b=list(np.linspace(start,end,N))
    y_b=list(np.zeros(int(N)))           

    x_b,y_b = insertion(x,x_b,y,y_b,N)

    plot(x_b,y_b)
    
    excel(x_b,y_b)

            
make(8,1000,0.1)