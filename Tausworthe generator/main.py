# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 10:57:09 2021

@author: Pablo González
"""

import seaborn as sns
import numpy as np
import time
 
def tausworthe(n = 1, r = 3, q = 5, l = 4, seed = None):
        
    # Step 1: Initialize binary sequence
    binary = bin(seed)[2:] if seed else bin(clock())[2:]
    storage = ( binary*( 1 + q//len(binary) ) )[:q]
    position = q
    
    # Step 2: "The period of 0-1 bits is always 2**q - 1"
    period = 2**q - 1
    if n > period:
        n = period
        print(f"You have exceeded the period, {period} numbers will be returned")
    
    # Step 3:
    for i in range(l*n):
        # B_i = (B_{i-r} + B_{i-q} mod 2) 
        B_i = (int(storage[position-r]) + int(storage[position-q]))%2
        storage += str(B_i)
        position += 1
            
    storage = storage[:-q]
    
    storage = [ int(storage[i:i+l],2)/2**l for i in range(0, len(storage), l)]
    return storage

def clock():
    temp = round(time.time()*100000)
    inverse = int(str(temp)[::-1])
    time.sleep(0.00001)
    return inverse

def unif(n = 1000000, a = 0, b = 1, seed = None):
    # This function returns n uniform random variables between a and b.
    temp = [(b-a)*i + a for i in tausworthe(n,18,31,35,seed)] #53,60,35 ## 28,31,18
    return temp


def norm(n, mu = 0, var = 1, seed = None):
    # Using the Box-Muller transformation, this function returns the inputted
    # uniform random variables as normal rvs with mean "mu" and variance "var"
    x = unif(n, seed = seed)
    z = []
    for i in range(0, len(x),2):
        # To reduce computation time (i.e. given the logs), the calculations 
        # are first separated to then only change whether we apply a sin or a cos function
        p1, p2 = np.sqrt(-2*np.log(x[i])), 2*np.pi*x[i+1]
        z1 = p1*np.radians( np.cos(p2) )
        z2 = p1*np.radians( np.sin(p2) )
        z1, z2 = var*z1+mu, var*z2+mu
        z = np.append(z, [z1,z2])
    return z


def gof(prns, nbins = 10):
    # Goodness of fit test: H0 of uniformity.
    bins = np.array(list(range(0,nbins,1)))/nbins # As in the exercises
    expected = [len(prns)/nbins]*nbins
    observed = np.bincount(np.digitize(prns,bins))[1:]
    chi0 = sum( np.divide( (observed-expected)**2, expected) )
    return chi0 > 16.919 # Do we reject?


def correlation(prns):
    return np.corrcoef( prns[:-1], prns[1:] )[1,0]


def runs(prns):
    # Runs test: H0 of independence.
    temp = np.sign( np.diff( np.sign( np.append([0], np.diff(prns,1)) ) ) )
    runs, n = np.count_nonzero(temp), len(prns)
    A_mean, A_var = (2*n-1)/3, (16*n-29)/90
    z0 = (runs-A_mean)/np.sqrt(A_var)
    return abs(z0) > 1.96 # Do we reject?


def tests(prns):
    if gof(prns) == False:
        print("We fail to reject the null hypothesis of uniformity")
    else:
        print("We reject the null hypothesis of uniformity")
    if runs(prns) == False:
        print("We fail to reject the null hypothesis of independence")
    else:
        print("We reject the null hypothesis of independence")        
    cor = correlation(prns)
    print(f"Additionally, the autocorrelation coefficient is equal to: {cor}")
    return None


if __name__ == '__main__':
    
    seq1 = unif(1000000, seed = 6644) # 10000 #1000000
    tests(seq1)
    hist = sns.displot(seq1, bins = 50)
    hist.set(xlabel = "Value", ylabel = "Counts", 
             title = "Figure 1: Histogram of observed PRN's")
    hist.savefig("uniform_hist.png")
    hist.fig.clf()

    displot = sns.displot(seq1, kind = "kde", fill = True)
    displot.set(xlabel = "Value", ylabel = "Probability", 
                title = "Figure 2: Uniform PRN's - Kernel density plot")
    displot.savefig("uniform_kde.png")
    displot.fig.clf()
    
    seq2 = seq1[:1000]
    a = [seq2[i] for i in range(len(seq2)) if i%2==1]
    b = [seq2[i] for i in range(len(seq2)) if i%2==0]
    dots = sns.scatterplot( x = a, y = b , legend = None)
    dots.set(xlabel = "i", ylabel = "i+1", 
             title = "Figure 3: Scatter plot of adjacent PRN's")
    dots.figure.subplots_adjust(top=.95)
    dots.figure.savefig("uniform_sct.png")
    dots.figure.clf()
    
    dev = norm(500000,0,1, seed = 12345)
    displot2 = sns.displot(dev, kind = "kde", fill = True)
    displot2.set(xlabel = "Value", ylabel = "Probability", 
                 title = "Figure 4: Normal PRN's - Kernel density plot")
    displot2.savefig("normal_kde.png")
    displot2.fig.clf()
    
    
    
