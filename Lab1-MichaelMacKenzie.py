# Code Written by: Michael MacKenzie
# Student Number: 10178040
# Course: CMPE 365

#######################################################################################################################

import matplotlib.pyplot as plt

#######################################################################################################################

# This is a graphing program to show the values printed

tempx = []
tempy = []

for k in range(1001):
    i = 0
    n = k + 1
    tempx.append(k)
    while n != 1:
        if n % 2 == 0:
            n = n/2
        else:
            n = 3*n + 1
        i += 1
    tempy.append(i)
print(len(tempy))
#plt.scatter(tempx, tempy)
plt.title("Number of Iterations for n Starting Value")
plt.xlabel("Starting Value n")
plt.ylabel("Number of Iterations")
#plt.show()

#######################################################################################################################

# This is the non-optimized algorithm that adds the number of iterations to check whether the Collatz program terminates
# up to a 'cap' value (1 to n). It is clearly not efficient, and we can see there are a few steps we can take to
# optimize it.

cap = 1000
checkArray = []
totalSteps = 0
stepArray = []

for i in range(1, cap + 1):
    n = i
    steps = 0
    checkArray.append(i)
    while n != 1:
        if n % 2 == 0:
            n = n/2
        else:
            n = 3*n + 1
        steps += 1
    totalSteps += steps
    stepArray.append(totalSteps)
print(stepArray[cap-1])

plt.plot(checkArray, stepArray)
plt.xlabel("n value")
plt.ylabel("iterations")
plt.title("Not Optimized")
#plt.show()

#######################################################################################################################

# This is the simple optimized code, which check from value 1 up to n whether the Collatz program terminates.  The
# optimization comes in the form of checking if the current program iteration dips below the current value; and hence it
# should also terminate.

cap1 = 1000
checkArray1 = []
totalSteps1 = 0
stepArray1 = []

for i in range(1, cap1 + 1):
    n = i
    steps = 0
    checkArray1.append(i)
    while n != 1:
        if n % 2 == 0:
            n = n/2
        else:
            n = 3*n + 1
        steps += 1
        if n < len(checkArray1):
            break
    totalSteps1 += steps
    stepArray1.append(totalSteps1)
print(stepArray1[cap1-1])

plt.plot(checkArray1, stepArray1)
plt.xlabel("n value")
plt.ylabel("iterations")
plt.title("Simple Optimized Algorithm - 1 Up to n")
#plt.show()

#######################################################################################################################

# Similar logic to the last algorithm, however instead of checking from 1 to n, it checks n to 1.  The optimization
# stores indicators in a dummy list when that number has been determined to terminate, then when another number is
# checked whether it terminates, it iterates through its sequence, and if one of the values in its sequence is the 
# beginning value of another sequence that terminates, it terminates

cap2 = 1000
checkArray2 = [0]*(cap2+1)
totalSteps2 = 0
stepArray2 = [-1]*(cap2+1)
k = 0

for i in range(cap2, 0, -1):
    n = i
    steps = 0
    checkArray2[k] = k
    while n != 1:

        if n % 2 == 0:
            n = n/2
        else:
            n = 3*n + 1
        if int(n) < len(stepArray2):
            if stepArray2[int(n)] > 0:
                break
        steps += 1
    totalSteps2 += steps
    stepArray2[k] = totalSteps2
    k += 1
print(stepArray2[cap2-1])
checkArray2[cap2] = cap2
stepArray2[cap2] = stepArray2[cap2-1]
plt.plot(checkArray2, stepArray2)
plt.xlabel("n value")
plt.ylabel("iterations")
plt.title("Simple Optimized Algorithm - n Down to 1")
#plt.show()

#######################################################################################################################

# This is the final optimization algorithm, and combines the simple optimization with a new optimization.  The new
# optimization stores all values that the program hits, not just the ones that it terminates for.  Then, when the
# program terminates, it populates a temporary list that the program later checks, and if that value has been hit, then
# we know the program terminates (since it terminated for it in a previous sequence). It is important to note that the
# temporary list is much larger than the cap (n) value.  This could be made more rigorously by creating a dummy variable
# that tracks the max value the Collatz program takes, then modifying this temporary list to accompany for this.

cap3 = 1000
checkArray3 = []
totalSteps3 = 0
stepArray3 = []
markVals3 = [-1]*cap3*7

for i in range(1, cap3 + 1):
    n = i
    steps = 0
    checkArray3.append(i)
    while n != 1:
        steps += 1
        if n % 2 == 0:
            n = n/2
        else:
            n = 3*n + 1
        if n < len(checkArray3):
            break
        if int(n) < len(markVals3):
            if markVals3[int(n)] != -1:
                break
            markVals3[int(n)] = 1
    totalSteps3 += steps
    stepArray3.append(totalSteps3)
print(stepArray3[cap3-1])

plt.plot(checkArray3, stepArray3)
plt.xlabel("n value")
plt.ylabel("iterations")
plt.title("Optimized Algorithm")
legendList = ["Non-optimized", "Simple Optimized 1 to n", "Simple Optimized n to 1", "Full optimized"]
plt.legend(legendList)
plt.show()

#######################################################################################################################
