# CS70, Spring 2014
# Homework 9, problem 1
# python (version 2.7.6) solutions


import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import random
import sys


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
def runManyTrials (p, k, m):
    return [runTrial(p, k) for _ in xrange(m)]


# compute "choose" function
def choose(n,k):
    assert n >= 0
    assert k >= 0
    assert n >= k
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))


# Q1 part (a)
def partA(p=0.7, k=1000, m=1000):
    print('Question 1 part (a):')
    print('Probability of head: %f'%p)
    print('Number of tosses: %i'%k)
    print('Number of trials: %i'%m)

    # plot empirical cdf
    std = math.sqrt(p*(1-p))
    results = {}
    results[k] = [(Sk-k*p)/(math.sqrt(k)*std) for Sk in runManyTrials(p, k, m)]
    results[k].sort()
    plt.plot(results[k],[float(y)/m for y in range(1,m+1)],label='k=' + str(k))
        
    # overlay normal cdf
    num_points = 1000
    min_max = 3
    x_values = [float(x)/num_points for x in range(-min_max*num_points,min_max*num_points)]
    plt.plot(x_values,[0.5 + 0.5*math.erf(x/math.sqrt(2)) for x in x_values],label='normal CDF')

    # set up plot
    plt.legend(loc=2)
    plt.xlabel('Normalized and centered fraction of heads',fontsize='large')
    plt.ylabel('Frequency',fontsize='large')
    plt.xlim(-min_max,min_max)
    plt.title('k = %s, p = %.1f'%(k,p))
    plt.show()


# Q1 part (c)
def partC(p=0.7, k=5000, m=1000):
    print('Question 1 part (c):')
    print('Probability of head: %f'%p)
    print('Number of tosses: %i'%k)
    print('Number of trials: %i'%m)

    # plot histogram
    std = math.sqrt(p*(1-p))
    results = [(Sk-k*p)/(math.sqrt(k)*std) for Sk in runManyTrials(p, k, m)]
    plt.hist(results, bins=24, align='mid', normed=True)

    # overlay normal distribution
    mean = 0
    variance = 1
    sigma = np.sqrt(variance)
    x = np.linspace(-3,3,100)
    plt.plot(x,mlab.normpdf(x,mean,sigma),label='normal PDF')

    # set up plot
    plt.legend()
    plt.xlabel('Number of heads',fontsize='large')
    plt.ylabel('Frequency',fontsize='large')
    min_max = 3
    plt.xlim(-min_max,min_max)
    plt.title('k = %i, p = %.1f'%(k,p))
    plt.show()


# Q1 part (d)
def partD(p=0.7, k=5000, m=1000):
    print('todo')


# Q1 part (e)
def partE(p=0.7, k=5000, m=1000):
    print('todo')


# Q1 part (f)
def partF(n=50):
    plt.plot(range(0,n+1),[choose(n,k) for k in range(0,n+1)])
    plt.xlabel('k',fontsize='large')
    plt.ylabel('n choose k',fontsize='large')
    plt.title('n = %i'%n)
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



