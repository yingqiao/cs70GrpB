# CS70, Spring 2014
# Homework 9, problem 1
# python (version 2.7.6) solutions


import math
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.integrate
import sys


#---------
# GLOBALS
#---------


FONTSIZE = 24
COLORS = ['b','k','g','r']


#---------
# HELPERS
#---------


# Creates a biased coin with p(Head) = p
# Returns true if heads and false otherwise
def biasedCoin(p):
    return random.random() <= p


# Runs a trial of k tosses of a biased coin (w.p. p of heads)
# and returns number of heads
def runTrial(p, k):
    return sum([biasedCoin(p) for _ in xrange(k)])


# Runs m trials of k tosses of a biased coin (w.p. p of heads)
# and returns all the numbers of heads
def runManyTrials(p, k, m):
    return [runTrial(p, k) for _ in xrange(m)]
    

# normal distribution
def normal(x):
    return 1/math.sqrt(2*math.pi)*math.exp(-x*x/2)
    
    
# integrate normal distribution
def integrate_normal(d):
    return scipy.integrate.quad(lambda x: normal(x), -float('inf'), d)[0]


# compute "choose" function
def choose(n,k):
    assert n >= 0
    assert k >= 0
    assert n >= k
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))


# compute KL divergence
def KL(a,p):
    return a*math.log(float(a)/p) + (1-a)*math.log(float(1-a)/(1-p))


# Q1 part (a)
def partA(p=0.7, krange=[10,100,1000,4000], m=10000):

    # plot empirical cdf
    std = math.sqrt(p*(1-p))
    for k in krange:
        results = {}
        results[k] = [(Sk-k*p)/(math.sqrt(k)*std) for Sk in runManyTrials(p, k, m)]
        results[k].sort()
        plt.plot(results[k],[float(y)/m for y in range(1,m+1)],label='k=' + str(k))
        
    # overlay normal cdf
    num_points = 1000
    min_max = 3
    x_values = [float(x)/num_points for x in range(-min_max*num_points,min_max*num_points)]
    plt.plot(x_values,[integrate_normal(x) for x in x_values],lw=3,label='normal CDF')

    # set up plot
    plt.legend(loc=2)
    plt.xlabel('Normalized and centered fraction of heads',fontsize=FONTSIZE)
    plt.ylabel('Frequency',fontsize=FONTSIZE)
    plt.xlim(-min_max,min_max)
    plt.title('p=' + str(p) + ', k = ' + str(krange) + ', m=' + str(m),fontsize=FONTSIZE)
    plt.show()


# Q1 part (c)
def partC(p=0.7, krange=[10,100,1000,4000], m=10000):

    # plot histograms
    std = math.sqrt(p*(1-p))
    for k in krange:
        results = [(Sk-k*p)/(math.sqrt(k)*std) for Sk in runManyTrials(p, k, m)]
        plt.hist(results, bins=20, align='mid', normed=True, label='k=' + str(k))

    # overlay normal distribution
    x_values = np.linspace(-3,3,100)
    plt.plot(x_values,[normal(x) for x in x_values],lw=3,label='normal PDF')

    # set up plot
    plt.legend()
    plt.xlabel('Number of heads',fontsize=FONTSIZE)
    plt.ylabel('Frequency',fontsize=FONTSIZE)
    min_max = 3
    plt.xlim(-min_max,min_max)
    plt.title('p=' + str(p) + ', k = ' + str(krange) + ', m=' + str(m),fontsize=FONTSIZE)
    plt.show()


# Q1 part (d)
def partD(prange=[0.3,0.7], krange=range(10,201), m=10000):
    log_thresh = 1e-3
    erange=[0.05,0.1]
    color_idx = 0

    # plot fraction of heads above ak
    for p in prange:
        all_trials = []
        for k in krange:
            trials_k = runManyTrials(p, k, m)
            all_trials.append(trials_k)
        arange = [p+e for e in erange]
        for a in arange:
            frac_lst = []
            for i in range(len(krange)):
                k = krange[i]
                frac_above = [Sk > a*k for Sk in all_trials[i]].count(True)/float(m)
                frac_lst.append(max(frac_above,log_thresh))
            lbl = 'p=' + str(p) + ', a=' + str(a)
            plt.plot(krange,frac_lst,COLORS[color_idx] + '.-',label=lbl)

            # fit a line to each set of points
            ls_line = np.polyfit(krange,[math.log(f) for f in frac_lst],1)
            lbl = 'fitted line'
            plt.plot(krange,[math.exp(ls_line[0]*k + ls_line[1]) for k in krange],COLORS[color_idx],label=lbl)

            # overlay KL divergence
            lbl = 'exp(-KL divergence)'
            plt.plot(krange,[math.exp(-KL(a,p)*k) for k in krange],COLORS[color_idx] + '--',label=lbl)
            color_idx += 1

    # set up plot
    plt.xlabel('Number of coin flips, k',fontsize=FONTSIZE)
    plt.ylabel('Fraction of trials with more than a*k heads',fontsize=FONTSIZE)
    plt.title('p = ' + str(prange) + ', m=' + str(m),fontsize=FONTSIZE)
    plt.yscale('symlog', linthreshy=log_thresh*math.sqrt(1e-1))
    plt.axis([krange[0]-5,krange[-1]+5,log_thresh*math.sqrt(1e-1),1])
    plt.legend(loc=3)
    plt.show()


# Q1 part (e)
def partE(p=0.3, krange=range(10,201), erange=[0.1,0.2,0.3], m=10000):
    colors = ['b','k','g']
    color_idx = 0

    all_trials = []
    for k in krange:
        trials_k = runManyTrials(p, k, m)
        all_trials.append(trials_k)
  
    for e in erange:

        # plot the fraction of trials where |S_k - kp| >= epsilon*k
        frac_lst = []
        for i in range(len(krange)):
            k = krange[i]
            trials_k = all_trials[i]
            frac_close = [abs(Sk - k*p) >= e*k for Sk in trials_k].count(True)/float(m)
            frac_lst.append(frac_close)
        plt.plot(krange,frac_lst,COLORS[color_idx],label='epsilon=' + str(e) + ', frac of trials')

        # overlay Chebyshev bound
        plt.plot(krange,[p*(1-p)/(k*e*e) for k in krange],colors[color_idx] + '--',label='Chebyshev bound')
        color_idx += 1

    # set up plot
    plt.legend()
    plt.axis([krange[0]-5,krange[-1]+5,0,1])
    plt.xlabel('Number of coin flips, k',fontsize=FONTSIZE)
    plt.ylabel("Chebyshev's inequality",fontsize=FONTSIZE)
    plt.title('p=' + str(p) + ', m=' + str(m),fontsize=FONTSIZE)
    plt.show()


# Q1 part (f)
def partF(n=50):
    plt.plot(range(0,n+1),[choose(n,k) for k in range(0,n+1)])
    plt.xlabel('k',fontsize=FONTSIZE)
    plt.ylabel('n choose k',fontsize=FONTSIZE)
    plt.title('n = %i'%n,fontsize=FONTSIZE)
    plt.show()


#------
# MAIN
#------


partmap = {'a':partA, 'A':partA,
           'c':partC, 'C':partC,
           'd':partD, 'D':partD,
           'e':partE, 'E':partE,
           'f':partF, 'F':partF}

if __name__=='__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] in partmap:
            partmap[sys.argv[1]]()
        else: print("Invalid part number %s."%sys.argv[1])
    else:
        print('Usage: python hw9.py [part number]')



