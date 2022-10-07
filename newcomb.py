import random
from symbol import return_stmt
from tkinter import N
import numpy as np
import matplotlib.pyplot as plt
import math
import statistics

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTION 1: Running a given reliability and box choice a given number of times ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#----------------------------------------------------------------------------------------------------------------------------------------------------------

def newcombsinglesim():
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Getting user inputs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    inp_predictionproportion = input("How reliable would you like the predictor to be, as a proportion (between 0 and 1)? ") # How reliable should the predicter be?
    try:
        float(inp_predictionproportion) # Make sure the input's a number.
    except:
        print("Input must be a number.")
        return
    predictionproportion = float(inp_predictionproportion)
    if predictionproportion > 1 or predictionproportion < 0: # Make sure the input is a valid proportion.
        print("Input must be between 0 and 1 (inclusive).")
        return
    inp_boxchoiceproportion = input("How often would you like to pick both boxes, as a proportion (between 0 and 1)? ") # How often should each strategy be used?
    try:
        float(inp_boxchoiceproportion)
    except:
        print("Input must be a number.")
        return
    boxchoiceproportion = float(inp_boxchoiceproportion)
    if boxchoiceproportion > 1 or boxchoiceproportion < 0:
        print("Input must be between 0 and 1 (inclusive).")
        return
    inp_n = input("How many times would you like to simulate the game? ")
    try:
        int(inp_n)
    except:
        print("Input must be a number.")
        return
    n = int(inp_n)
    if n <= 0:
        print("Input must be greater than 0.")
        return
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Running the simulations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    average = 0 # Keep track of the average amount gained for the entire simulation.
    amtgained = [] # Keep track of the amount gained for each game.
    for i in list(range(n)):
        boxchoice = random.random()
        prediction = random.random()
        if boxchoice > boxchoiceproportion: # Player picks only the opaque box, which either contains $1,000,000 or $0.
            if prediction > predictionproportion: # Predictor predicts incorrectly, and so thought the player would pick both boxes. So the player gets $0.
                average += 0
                amtgained.append(0)
            else: # Predictor predicted correctly, and so the player gets $1,000,000.
                average += 1000000/n
                amtgained.append(1000000)
        else: # Player picks both boxes.
            if prediction > predictionproportion: # Predictor predicts incorrectly, and so thought the player would only pick one box. So the player gets $1,001,000.
                average += 1001000/n
                amtgained.append(1001000)
            else: # Predictor predicts correctly, and so the player gets only the guaranteed $1,000.
                average += 1000/n
                amtgained.append(1000)
    print("The average amount you won per game was " + str(average) + ".")
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Plotting if desired ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    plotamtgained = input("Would you like to see a plot of your average amount gained over time? Input Y for yes. ") # Allow the user to see how their average earnings changed over time.
    if plotamtgained == "Y":
        avg = [] # This list will contain an entry for each game played. The entry will be the average amount gained so far at that time step or game.
        for j in list(range(1, len(amtgained) + 1)):
            agg = 0 # This variable is the aggregate amount gained up to time step (game number) j.
            for i in list(range(j)): 
                agg += amtgained[i]
            timeavg = agg/j # This is the average amount gained at time step (game number) j.
            avg.append(timeavg)
        plt.plot(list(range(n)), avg, 'k') # Plot the points simply.
        plt.xlabel('Time') # Add labels and a titles
        plt.ylabel('Average amount gained (in dollars)')
        plt.title('Average amount gained over time')
        label = "Final avg: " + str(round(average, 2)) # Label the final average.
        plt.annotate(label,
                 (n,avg[-1]),
                 textcoords="offset points", 
                 xytext=(0,10), 
                 ha='right')
        plt.show()
        return
    else:
        return

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTION 2: 100000 samples of size n = 100, with a given reliability and box choice  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#----------------------------------------------------------------------------------------------------------------------------------------------------------

def newcombhistogramsim():
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Getting user inputs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    inp_predictionproportion = input("How reliable would you like the predictor to be, as a proportion (between 0 and 1)? ") # Same inputs as before, except for the number of simulations.
    try:
        float(inp_predictionproportion) # Make sure the input's a number.
    except:
        print("Input must be a number.")
        return
    predictionproportion = float(inp_predictionproportion)
    if predictionproportion > 1 or predictionproportion < 0: # Make sure the input's a valid proportion.
        print("Input must be between 0 and 1 (inclusive).")
        return
    inp_boxchoiceproportion = input("How often would you like to pick both boxes, as a proportion (between 0 and 1)? ")
    try:
        float(inp_boxchoiceproportion)
    except:
        print("Input must be a number.")
        return
    boxchoiceproportion = float(inp_boxchoiceproportion)
    if boxchoiceproportion > 1 or boxchoiceproportion < 0:
        print("Input must be between 0 and 1 (inclusive).")
        return
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Running the simulations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    averagelist = [] # This will be the list of the sample means.
    for j in list(range(100000)):
        average = 0
        n = 100 # Sample size.
        for i in list(range(n)):
            boxchoice = random.random()
            prediction = random.random()
            if boxchoice > boxchoiceproportion: #Player picks only the opaque box, which either contains $1,000,000 or $0.
                if prediction > predictionproportion: #Predictor predicts incorrectly, and so thought the player would pick both boxes. So the player gets $0.
                    average += 0
                else: #Predictor predicted correctly, and so the player gets $1,000,000.
                    average += 1000000/n
            else: #Player picks both boxes.
                if prediction > predictionproportion: #Predictor predicts incorrectly, and so thought the player would only pick one box. So the player gets $1,001,000.
                    average += 1001000/n
                else: #Predictor predicts correctly, and so the player gets only the guaranteed $1,000.
                    average += 1000/n
        averagelist.append(average)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Computing stats and plotting the data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    mean = statistics.mean(averagelist) # Find the important stats for the sample distribution.
    median = statistics.median(averagelist)
    sd = statistics.stdev(averagelist)
    Q = statistics.quantiles(averagelist, n=4, method='exclusive') # These are the quartiles.
    print("The mean between all of the samples was", mean)
    print("The median of the samples was", median)
    print("With a standard deviation of", sd)
    fig = plt.figure() # Use a figure to plot a histogram and boxplot, one on top of the other, with the important stats on top.
    ax = fig.add_axes([0, 0, 1, 1])
    plt.subplot(211) # Make a histogram.
    plt.title("Sample distribution for " + str(round(predictionproportion*100, 2)) + "% reliability and " + str(round(boxchoiceproportion*100, 2)) + "% 2-boxing")
    numbins = 30 # The number of bins is a matter of personal preference. I've gone with 30 here for some detail but a clear trend.
    plt.hist(averagelist, bins = numbins)
    plt.text(0.01, 0.95 , "mean = " + str(round(mean, 2)) + ", median = " + str(round(median, 2)) + ", sd = " + str(round(sd, 2)), transform = ax.transAxes)
    plt.text(0.01, 0.92 , "Q1 = " + str(round(Q[0], 2)) + ", Q3 = " + str(round(Q[2], 2)), transform = ax.transAxes)
    plt.ylabel("Count")
    plt.subplot(212) # Make a boxplot.
    plt.boxplot(averagelist, vert = False, sym = '.')
    plt.tick_params(left = False, labelleft = False) # Turn off vertical label and tick mark for the boxplot.
    plt.xlabel("Average amount gained")
    plt.show()
    return

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTION 3: Given a reliability, what's the most optimal solution for n games played??  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#----------------------------------------------------------------------------------------------------------------------------------------------------------

def newcombscatter():
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Getting the user input ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    inp_predictionproportion = input("How reliable would you like the predictor to be, as a proportion (between 0 and 1)? ")
    try:
        float(inp_predictionproportion) # Make sure the input's a number.
    except:
        print("Input must be a number.")
        return
    predictionproportion = float(inp_predictionproportion)
    if predictionproportion > 1 or predictionproportion < 0: # Make sure the input's a valid proportion.
        print("Input must be between 0 and 1 (inclusive).")
        return
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Running the simulations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    averagelist = []
    for boxchoicepercent in list(range(0, 101, 2)): # Picking which boxchoice percents to simulate. Increment is up to personal preference. I've chosen increments of 2%, but 5% would also be fine.
        boxchoiceproportion = boxchoicepercent/100
        average = 0
        n = 10000 # The number of games played. I've chosen 10000, but you could pick more, if you wanted. 
        for i in list(range(n)):
            boxchoice = random.random()
            prediction = random.random()
            if boxchoice > boxchoiceproportion: # Player picks only the opaque box, which either contains $1,000,000 or $0.
                if prediction > predictionproportion: # Predictor predicts incorrectly, and so thought the player would pick both boxes. So the player gets $0.
                    average += 0
                else: # Predictor predicted correctly, and so the player gets $1,000,000.
                    average += 1000000/n
            else: # Player picks both boxes.
                if prediction > predictionproportion: # Predictor predicts incorrectly, and so thought the player would only pick one box. So the player gets $1,001,000.
                    average += 1001000/n
                else: # Predictor predicts correctly, and so the player gets only the guaranteed $1,000.
                    average += 1000/n
        averagelist.append(average)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Plotting the data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    x = list(range(0, 101, 2)) # Data plotting is a simple scatterplot. Here, for clarity, I've explicitly defined the x and y variables.
    y = averagelist
    z = np.polyfit(x, y, 1) # This line and the next add a linear regression line.
    p = np.poly1d(z)
    intercept = p(1)
    slope = p(2) - p(1)
    fig = plt.figure() # Use a figure to add the trend line data on top.
    ax = fig.add_axes([0, 0, 1, 1])
    plt.subplot(111)
    plt.title("Average amount gained for each strategy, given a " + str(round(predictionproportion*100, 2)) + "% reliability")
    plt.plot(x,p(x),"r--")
    plt.scatter(x, y)
    plt.text(0.01, 0.92 , "trend line intercept =  " + str(round(intercept, 2)) + ", slope = " + str(round(slope, 2)), transform = ax.transAxes)
    plt.xlabel("Percent of games in which the player picks both boxes")
    plt.ylabel("Average amount gained")
    plt.show()
    return