# CS70, Spring 2014
# Homework 12, problem 5 lab
# python (version 2.7.6) skeleton


import math
import matplotlib.pyplot as plt
import numpy as np
import random
import sys


#---------
# GLOBALS
#---------


FONTSIZE = 24
COLORS = ['b','k','g','r']


#---------
# HELPERS
#---------


# Creates a biased coin with Pr(Head) = p
# Returns true if heads and false otherwise
def biasedCoin(p):
    return random.random() <= p


# input:  the probability p of winning the lottery on any given day
# output: the number of tickets Lily has to buy to win the lottery
def lotteryTrial(p):
    if biasedCoin(p):
        return 1
    else:
        return 1 + lotteryTrial(p)


# input:  x, the number of lottery tickets and p, the probability of winning on a given day
# output: the probability of buying x lottery tickets (i.e. f(x))
def lotteryPmf(x,p):
    return pow(1-p,x-1)*p


# input: input:  x, the number of lottery tickets and p, the probability of winning on a given day
# output: the probability of buying x or fewer lottery tickets (i.e. F(x))
def lotteryCmf(x,p):
    return 1 - pow(1-p,x)


# Q5, part (b)
def partB(p=0.2, m=10000):
    trialList = []
    for trial in range(m):
        trialList.append(lotteryTrial(p))
    plt.hist(trialList, bins=20, normed=True, label="m=" + str(m) + " trials")

    # overlay f(x)
    x_values = np.linspace(0,20,100)
    plt.plot(x_values, [lotteryPmf(x,p) for x in x_values], label="f(x)")

    # print the average number of lottery tickets
    print("average is: " + str(sum(trialList)/float(len(trialList))))

    # set up plot
    plt.xlabel("x = number of lottery tickets")
    plt.ylabel("fraction of trials with x lottery tickets")
    plt.title("Q5, part (b)")
    plt.legend()
    plt.show()

    
# Q5, part (e)
def partF(p=0.2, m=10000):
    trialList = []
    for trial in range(m):
        trialList.append(lotteryTrial(p))

    # plot empirical cmf
    x_values = range(0,max(trialList)+1)
    empiricalCmf = []
    for i in x_values:
        empiricalCmf.append([x <= i for x in trialList].count(True)/float(m))
    plt.bar(x_values ,empiricalCmf, label="m=" + str(m) + " trials")

    # overlay F(x)
    plt.plot(x_values, [lotteryCmf(x,p) for x in x_values], label="F(x)")

    # set up plot
    plt.xlabel("x = number of lottery tickets")
    plt.ylabel("fraction of trials with x or fewer lottery tickets")
    plt.title("Q5, part (e)")
    plt.legend()
    plt.show()
    
    
    

#------
# MAIN
#------


partmap = {'b':partB, 'B':partB,
           'e':partF, 'E':partF}

if __name__=='__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] in partmap:
            partmap[sys.argv[1]]()
        else: print("Invalid part number %s."%sys.argv[1])
    else:
        print('Usage: python hw12_skeleton.py [part number]')



