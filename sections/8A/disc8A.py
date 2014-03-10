# CS70, Spring 2014, discussion 8A
# Group B


import math
import random
import sys
#import matplotlib.pyplot as plt


#---------
# HELPERS
#---------


# print a histogram to the screen of a list L
def hist(L):
    # constants
    ratio_thres = 3  # increase for narrower histograms
    rescaling = 1    # decrease for wider histograms
    width_thres = 5  # this is only for printing the axis

    # set up parameters
    n = len(L)
    min_val = min(L)
    max_val = max(L)
    w = max_val - min_val
    bin_size = 1
    num_bins = float(w)/bin_size
    L = sorted(L)

    # create counts for each bin
    bin_counts = []
    for i in range(min_val,max_val+1):
        bin_counts.append(L.count(i))
    h = max(bin_counts)

    # if the ratio of h to w is too big, rescale
    ratio = float(h)
    if w != 0:
        ratio = float(h)/w
    if (ratio > ratio_thres):
        bin_counts = [int(float(x)*rescaling/ratio) for x in bin_counts]
        h = max(bin_counts)

    # create the histogram string
    hist_str = ''
    for j in range(h,-1,-1):
        j_str = ''
        for b in bin_counts:
            if b > j:
                j_str += '*'
            elif b == 0 and j == 0 and ratio > ratio_thres:
                j_str += '.'
            else:
                j_str += ' '
        hist_str += j_str + '\n'

    # axis for histogram
    hist_str += '-'*(w+1) + '\n'
    if (w > width_thres):
        avg_val = (max_val+min_val)/2
        space_count1 = int(math.floor(float(w-2)/2)) - len(str(min_val)) + 1
        space_count2 = int(math.ceil(float(w-2)/2)) - len(str(avg_val)) - len(str(max_val)) + 2
        hist_str += str(min_val) + ' '*space_count1 + str(avg_val) + ' '*space_count2 + str(max_val)
    elif w > 0:
        hist_str += str(min_val) + ' '*(w-1) + str(max_val)
    else:
        hist_str += str(min_val)

    return hist_str
        
# simulate from a uniform distribution with range [a,b]
def uni(a,b):
    number = random.randint(a,b)
    return number

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


# simulates from binom or pois depending on size of parameters
def sample(parameters):
    if len(parameters) == 1:
        lmbda = parameters[0]
        return pois(parameters[0])
    else:
        n,p = parameters
        return binom(n,p)
        

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
    input = raw_input("How many busses pass by in 1 hour?  ")
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
# runs a few trials.
# there is a "hidden" mode that prints a uniform distribution.
def whichMode():
    print "Seperate Trials or Histogram?"
    answer = raw_input("Type 0 for separate trials, 1 for a histogram:  ")
    if answer == "0":
        return 0
    if answer == "1":
        return 1
    if answer == "2":
        return 2
    else:
        "Please type 0 or 1"
        return whichMode()
    
# Asks input for how many trials
def howManyTrials():
    input = raw_input("how many trials do you want to run?  ")
    try:
        trials = int(input)
    except ValueError:
        print "Please enter a positive integer."
        return howManyTrials()
    return trials


#------
# MAIN
#------


histogram = whichMode()

#Run the uniform case
if (histogram == 2):
    print "Running a different experiment. . . "
    a = raw_input("What is the lowest number in the range? ")
    b = raw_input("What is the highest number in the range? ")
    trials = raw_input("how many trials? ")
    data = []
    for i in range(int(trials)):
        data.append(uni(int(a),int(b)))
    print (hist(data))
    #plt.hist(data)
    #plt.show()
    sys.exit()

parameters = getInput()
trials = howManyTrials()

data = []

for i in range(trials):
    data.append(sample(parameters))

if histogram:
    print(hist(data))
    #plt.hist(data)
    #plt.show()
else:
    for i in range (trials):
        string = "Trial " + str(i+1) + ":    " + str(data[i])
        print string


