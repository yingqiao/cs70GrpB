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
    # YOUR CODE HERE
    print('todo')


# input:  x, the number of lottery tickets and p, the probability of winning on a given day
# output: the probability of buying x lottery tickets (i.e. f(x))
def lotteryPmf(x,p):
    # YOUR CODE HERE
    print('todo')


# input: input:  x, the number of lottery tickets and p, the probability of winning on a given day
# output: the probability of buying x or fewer lottery tickets (i.e. F(x))
def lotteryCmf(x,p):
    # YOUR CODE HERE
    print('todo')


# Q5, part (b)
def partB(p=0.2, m=10000):
    # run trials
    # YOUR CODE HERE

    # overlay f(x)
    # YOUR CODE HERE

    # print the average number of lottery tickets
    # YOUR CODE HERE

    # set up plot
    plt.xlabel("x = number of lottery tickets")
    plt.ylabel("fraction of trials with x lottery tickets")
    plt.title("Q5, part (b)")
    plt.legend()
    plt.show()

    
# Q5, part (e)
def partF(p=0.2, m=10000):
    # run trials
    # YOUR CODE HERE

    # plot empirical cmf
    # YOUR CODE HERE

    # overlay F(x)
    # YOUR CODE HERE

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



