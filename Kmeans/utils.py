# -*- coding: utf-8 -*-
"""
Created on Wed Jan 2 15:00:39 2021

@author: pablo
"""

import numpy as np
import pandas as pd


def euclidean(a,b):
    return np.linalg.norm(a-b, axis = 1)


def kmean(dot, k = 2):
    
    dt = pd.DataFrame(dot, columns = ['r','g','b'])    
    cent = dt.sample(k).reset_index(drop = True)
    dist = pd.DataFrame(np.zeros( ( len(dt), len(cent) ) ))
    old = pd.DataFrame([0,0,0]) # Init
    r = 0
    while not cent.equals(old):
        
        for cent_i, cent_r in cent.iterrows():
            dist.loc[:,cent_i] = euclidean( dt, list(cent_r) )
        
        #We obtain the labels
        old = cent.copy()
        label = dist.idxmin(axis=1)
        
        #Recalculate centroids
        for cent_i, cent_r in cent.iterrows():
            if dt[label == cent_i].empty:
                cent.loc[cent_i] = dt.sample(1).values
            else:
                cent.loc[cent_i] = np.mean(dt[label == cent_i], axis = 0)
        r += 1
    print('Number of iterations:', r)
    return cent.to_numpy(), label.to_numpy()

