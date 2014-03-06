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

# asks for type of trial. Returns "coin", "dice", or "bus"
def getTrialType():
    input = raw_input("Coin, Dice, or Bus?:  ")
    input = input.lower()
    if input == "coin" or input == "coins":
        return "coin"
    elif input == "dice" or input == "die":
        return "dice"
    elif input == "bus" or input == "busses":
        return "bus"
    else:
        print "Please choose either coin, dice, or bus."
        return getTrialType()

# gets the parameters for the coin tosses    
def getParametersForCoin():
    input = raw_input("How many flips?  ")
    try:
        n = int(input)
    except ValueError:
        print "Please enter a positive integer."
        return getParametersForCoin()
    if n <= 0:
        print "Please enter a positive integer."
        return getParametersForCoin()
    return [n, 0.5]

# gets parameters for the die rolls.
def getParametersForDice():
    input = raw_input("How many sides does the die have?  ")
    try:
        sides = int(input)
    except ValueError:
        print "Please enter a positive integer."
        return getParametersForDice()
    if sides <= 0:
        print "Please enter a positive integer."
        return getParametersForDice()
    properInput = False
    while not properInput:
        input = raw_input("How many rolls of the die?  ")
        try:
            n = int(input)
        except ValueError:
            print "Please enter a positive integer."
            continue
        if n <= 0:
            print "Please enter a positive integer."
            continue
        properInput = True
        p = 1.0 / sides
    return [n, p]

    
def getParametersForBus():
    input = raw_input("How many busses pass by in 20 minutes?  ")
    try:
        lmbda = int(input)
    except ValueError:
        print "Please enter a positive integer."
        return getParametersForBus()
    if lmbda <= 0:
        print "Please enter a positive integer."
        return getParametersForBus()
    return [lmbda]


# gets parameters for the trial
def getParameters(type):
    if type == "coin":
        return getParametersForCoin()
    if type == "dice":
        return getParametersForDice()
    if type == "bus":
        return getParametersForBus()

def getInput():
    type = getTrialType()
    params = getParameters(type)
    return params

# this asks which mode the student wants. We will have two modes:
# one that builds a histogram over many trials, and one that
# runs a single trial.

def whichMode():
    print "Single Trial or Multiple Trials?"
    answer = raw_input("Type 0 for single trial, 1 for multiple trials:  ")
    if answer == "0":
        return 0
    if answer == "1":
        return 1
    else:
        "Please type 0 or 1"
        return whichMode()
    



#------
# MAIN
#------

#unflag below

whichMode()
getInput()        

L = []
for i in range(1000):
    L.append(binom(10,0.5))

M = []
for i in range(1000):
    M.append(pois(10))

#plt.hist(L)
plt.hist(M)
plt.show()

