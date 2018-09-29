import math
import random

########################################################################################################################
# Part 1: Function definition for optimization

def maxsegment(arr,low,high): # Returns first index, last index and sum of the list
    if high != low:
        mid = math.floor((low+high)/2)
        [lowleft, highleft, sumleft] = maxsegment(arr, low, mid)
        [lowright, highright, sumright] = maxsegment(arr, mid+1, high)
        [lowcross, highcross, sumcross] = maxcrosssegment(arr, low, mid, high)
        if (sumleft >= sumright) & (sumleft >= sumcross):
            return lowleft, highleft, sumleft
        elif (sumright >= sumleft) & (sumright >= sumcross):
            return lowright, highright, sumright
        else:
            return lowcross, highcross, sumcross
    else:
        return low, high, arr[high]

def maxcrosssegment(arr,low,mid,high): # Called in maxsegment, checks sum accross children border
    maxL = 0; sum = 0; sumL = -10000
    for i in range(mid, low-1, -1):
        sum += arr[i]
        if sum > sumL:
            sumL = sum; maxL = i
    maxR = 0; sum = 0; sumR = -10000
    for j in range(mid+1, high+1):
        sum += arr[j]
        if sum > sumR:
            sumR = sum; maxR = j
    return maxL, maxR, sumL + sumR

########################################################################################################################
# Part 1: A testing spot for the algorithm. Uses a randomly generated array, of random length (all constrained)

a = random.randint(5,10) #length of array
#### test values for the defined program
low_test = 0
high_test = a
####
test_array = []
for i in range(0, a):
    test_array.append(random.randint(-20, 20))
print("###################################")
[x, y, z] = maxsegment(test_array, low_test, high_test-1)
print("Original Array:", test_array)
print("Max Segment Sum:", test_array[x:y+1], ", Sum:", z)
print("###################################")

########################################################################################################################
# Part 2: This finds the 2 max non-overlapping sub-arrays. It uses the technique of finding the first max sub array,
# then replaces that entire sub-array with the lowest value in the list

def dualmaxsegments(arr):
    arrtemp = arr
    [x1, y1, z1] = maxsegment(arr, 0, len(arr)-1)
    print("###################################")
    print("Original Array:", arr)
    print("1st Max Segment Sum:", arr[x1:y1+1], ", Sum:", z1)
    if len(arr) == 1+y1-x1:
        return print("No 2nd max. 1st Max Segment Was the Entire Array!")
    else:
        for k in range(x1, y1+1):
            arrtemp[k] = min(arr)-1
        [x2, y2, z2] = maxsegment(arrtemp, 0, len(arrtemp)-1)
        print("2nd Max Segment Sum:", arrtemp[x2:y2+1], ", Sum:", z2)
        print("###################################")

########################################################################################################################
# Part 2: A testing spot for the second question.  Uses a randomly generated array, of random length (all constrained)

b = random.randint(10,20) #length of array
test_array2 = []
for i in range(0, b):
    test_array2.append(random.randint(-20, 20))
dualmaxsegments(test_array2)

########################################################################################################################
# Part 3: This finds the 2 max non-overlapping sub-arrays (if time permits)
# efesffsjefensfjlnsjlfnlsjn

