# CS70, Spring 2014, discussion 8A
# Group B


import math
import matplotlib.pyplot as plt
import random


#---------
# GLOBALS
#---------


#--------------------------
# PARSE COMMAND LINE INPUT
#--------------------------


#---------
# HELPERS
#---------


# simulate from a binomial distribution: count the number of H coin
# tosses out of n total, with probability p of each toss being H
def binom(n,p):
    H_count = 0
    for i in range(n):
        u = random.random()
        if u < p:
            H_count += 1
    return H_count


# simulate from a poisson distribution with rate lambda
def pois(lmbda):
    L = math.exp(-lmbda)
    k = 0
    p = 1
    while (p > L):
        k += 1
        u = random.random()
        p *= u
    return k-1


#------
# MAIN
#------


L = []
for i in range(1000):
    L.append(binom(10,0.5))

M = []
for i in range(1000):
    M.append(pois(10))

#plt.hist(L)
plt.hist(M)
plt.show()

