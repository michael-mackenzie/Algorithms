import numpy as np
import os
import random
import math
import matplotlib.pyplot as plt
pathway = os.getcwd()


# Function to retrieve the data and compile into one passable 2-dimensional numpy array.
def fetch_data():
    # Insert folder name containing the sample data here (make sure its in the same pathway as this code
    folder = '\Lab4Data'
    os.chdir(pathway + folder)
    start_data1 = np.array(np.genfromtxt('start1.csv', delimiter=','))
    finish_data1 = np.array(np.genfromtxt('finish1.csv', delimiter=','))
    start_data2 = np.array(np.genfromtxt('start2.csv', delimiter=','))
    finish_data2 = np.array(np.genfromtxt('finish2.csv', delimiter=','))
    return np.vstack((start_data1, finish_data1)).T, np.vstack((start_data2, finish_data2)).T


# Given a 2-dimensional numpy array, sort it based on its second column (departure time).
def sort_by_depart(d):
    sorted_data = d[d[:, 1].argsort()]
    return sorted_data


# This is the main function that drives the greedy algorithm.  Given a set sorted by departure time, the
# algorithm determines the smallest number of gates required (greedily).
def number_of_gates(lis):
    overlap = 0
    issues = conflicts(lis)
    while len(issues) > 2:
        issues = conflicts(issues)
        overlap += 1
    return overlap


# This aids in returning the correct number of gates.  This function creates a list of the conflicting gates to the
# existing compare to gate in number_of_gates
def conflicts(lists):
    k = 0
    conf = []
    if len(lists) < 2:
        return conf
    for i in range(1, len(lists)):
        if lists[i][0] > lists[k][1]:
            k = i
        else:
            conf.append(lists[i])
    return conf


# Given a 2-dimensional array of corresponding arrival and departure times, and a given maximum delay, this
# function adds a random delay between 0 and max_del to arrival [rand_delay_arr = rand(0, max_del)], and adds a random
# delay between random delay added to arrival and max_del to departure [rand_delay_dep = rand(rand_delay_arr, ma_del)].
# It adds these delays to a generated random fractional set of these planes.
def delay(s, max_del, fract):
    test_set, num_delays = random_fraction(s, fract)
    new_delay_set = s
    for i in range(len(test_set)):
        if test_set[i] == 1:
            rand_delay = random.uniform(0, max_del)
            new_delay_set[i][0] += rand_delay
            new_delay_set[i][1] += random.uniform(rand_delay, max_del)
    return new_delay_set, num_delays


# Given a 2-dimensional array of corresponding arrival and departure times, this function creates an indicator list of
# same length as the orig_set, and tells the delay function where to add delay.
def random_fraction(orig_set, frac):
    # fraction = random.random()
    temp_set = [0]*len(orig_set)
    for i in range(len(temp_set)):
        temp_set[i] = i
    rand_set = random.sample(temp_set, math.floor(frac*len(temp_set)))
    temp_set = [0] * len(orig_set)
    for i in range(len(rand_set)):
        temp_set[rand_set[i]] = 1
    return temp_set, len(rand_set)


# Function that plots and prints trends of different data
def q2_help_plot():
    data1, data2 = fetch_data()
    fraction = 0.5
    lateness = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    num_gates1 = []
    num_gates2 = []
    print()
    print("Holding Fraction Constant (0.5) and Changing Maximum Lateness:")
    for i in range(len(lateness)):
        delayed1, num_del1 = delay(data1, lateness[i], fraction)
        delayed2, num_del2 = delay(data2, lateness[i], fraction)
        sorted1 = sort_by_depart(delayed1)
        sorted2 = sort_by_depart(delayed2)
        num_gates1.append(number_of_gates(sorted1))
        num_gates2.append(number_of_gates(sorted2))
        print("Max Lateness:", lateness[i], ", Number of Gates (set1):", number_of_gates(sorted1))
        print("Max Lateness:", lateness[i], ", Number of Gates (set2):", number_of_gates(sorted2))

    # Plot for set1 holding fraction constant and changing lateness
    plt.title("Set 1: How Gates Increase as a Function of Allowed Lateness")
    plt.xlabel("Allowed Lateness")
    plt.ylabel("Number of Gates Needed")
    plt.scatter(lateness, num_gates1)
    z = np.polyfit(lateness, num_gates1, 1)
    p = np.poly1d(z)
    plt.plot(lateness, p(lateness), "r--")
    plt.show()

    # Plot for set2 holding fraction constant and changing lateness
    plt.title("Set 2: How Gates Increase as a Function of Allowed Lateness")
    plt.xlabel("Allowed Lateness")
    plt.ylabel("Number of Gates Needed")
    plt.scatter(lateness, num_gates2)
    z = np.polyfit(lateness, num_gates2, 1)
    p = np.poly1d(z)
    plt.plot(lateness, p(lateness), "r--")
    plt.show()

    data1, data2 = fetch_data()
    fraction = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    lateness = 0.5
    num_gates1 = []
    num_gates2 = []
    print()
    print("Holding Lateness Constant (0.5) and Changing Maximum Fraction:")
    for i in range(len(fraction)):
        delayed1, num_del1 = delay(data1, lateness, fraction[i])
        delayed2, num_del2 = delay(data2, lateness, fraction[i])
        sorted1 = sort_by_depart(delayed1)
        sorted2 = sort_by_depart(delayed2)
        num_gates1.append(number_of_gates(sorted1))
        num_gates2.append(number_of_gates(sorted2))
        print("Planes Delayed (%):", fraction[i], ", Number of Gates (set1):", number_of_gates(sorted1))
        print("Planes Delayed (%):", fraction[i], ", Number of Gates (set2):", number_of_gates(sorted2))

    # Plot for set1 holding lateness constant and changing fraction
    plt.title("Set 1: How Gates Increase as a Function of Fraction Delayed")
    plt.xlabel("Fraction of Planes Delayed")
    plt.ylabel("Number of Gates Needed")
    plt.scatter(fraction, num_gates1)
    z = np.polyfit(fraction, num_gates1, 1)
    p = np.poly1d(z)
    plt.plot(fraction, p(fraction), "r--")
    plt.show()

    # Plot for set2 holding lateness constant and changing fraction
    plt.title("Set 2: How Gates Increase as a Function of Fraction Delayed")
    plt.xlabel("Fraction of Planes Delayed")
    plt.ylabel("Number of Gates Needed")
    plt.scatter(fraction, num_gates2)
    z = np.polyfit(fraction, num_gates2, 1)
    p = np.poly1d(z)
    plt.plot(fraction, p(fraction), "r--")
    plt.show()


# Question 1: Code that fetches the data, sorts it and then determines the minimum number of gates.
def q1():
    data_set1, data_set2 = fetch_data()
    sorted_data_set1 = sort_by_depart(data_set1)
    sorted_data_set2 = sort_by_depart(data_set2)
    min_gates1 = number_of_gates(sorted_data_set1)
    min_gates2 = number_of_gates(sorted_data_set2)
    print("The minimum number of gates required for set 1:", min_gates1)
    print("The minimum number of gates required for set 2:", min_gates2)
    return


# Question 2: Code that does the same above, however implements a random delay of size up max_delay.
def q2(max_delay):
    fraction = 0.5
    data_set1, data_set2 = fetch_data()
    delayed_set1, num_delays1 = delay(data_set1, max_delay, fraction)
    delayed_set2, num_delays2 = delay(data_set2, max_delay, fraction)
    sorted_data_set1 = sort_by_depart(delayed_set1)
    sorted_data_set2 = sort_by_depart(delayed_set2)
    min_gates1 = number_of_gates(sorted_data_set1)
    min_gates2 = number_of_gates(sorted_data_set2)
    print("Set 1:", min_gates1, ", Max Delay:", max_delay)
    print("Set 2:", min_gates2, ", Max Delay:", max_delay)
    return


# Test q1 and q2

q1()
q2_help_plot()

