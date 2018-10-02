########################################################################################################################
# Code Written By: Michael MacKenzie, Date: 10/2/2018


########################################################################################################################
# Question 1 & Question 2

import random
import matplotlib.pyplot as plt
import math
import numpy

convexHull = []


# Generates n random points uniformly around the origin.
def uniformpoints(n):
    a = [0] * n
    for i in range(n):
        a[i] = [0] * 2
        a[i][0] = random.uniform(-5, 5)
        a[i][1] = random.uniform(-5, 5)
    for j in range(len(a)):
        plt.scatter(a[j][0], a[j][1], color='b')
    return a


# Generates n random points around the origin as per a gaussian distribution.
def gaussianpoints(n):
    a = [0] * n
    for i in range(n):
        a[i] = [0] * 2
        a[i][0] = random.gauss(0, 2.5)
        a[i][1] = random.gauss(0, 2.5)
    for j in range(len(a)):
        plt.scatter(a[j][0], a[j][1], color='b')
    return a


# Given a line joined by S & T, determines the farthest point away from it in the set 'a'.
def farthestpoint(S, T, a):
    max = 0
    max_point = S
    for i in range(len(a)):
        area = abs((S[0] - a[i][0]) * (T[1] - S[1]) - (S[0] - T[0]) * (a[i][1] - S[1]))
        if area > max:
            max = area
            max_point = a[i]
    return max_point


# Initial function call, it determines the right and left most points, then divides the original set 'a' into points on
# the left side and points on the right side.  This is then fed into subhull.
def quickhull(a):
    global convexHull
    leftval = [0,0]
    rightval = [0,0]
    left_list = []
    right_list = []
    for i in range(len(a)):
        if a[i][0] < leftval[0]:
            leftval = a[i]
        if a[i][0] > rightval[0]:
            rightval = a[i]
    convexHull.append(leftval)
    convexHull.append(rightval)
    for j in range(len(a)):
        if (a[j][1] - leftval[1]) * (rightval[0] - leftval[0]) - (rightval[1] - leftval[1]) * (a[j][0] - leftval[0]) > 0:
            right_list.append(a[j])
        else:
            left_list.append(a[j])
    subhull(right_list, leftval, rightval)
    subhull(left_list, rightval, leftval)


# Given a line formed by points P and Q, and a set 'a', using farthest point, this function determines the farthest
# point from the line and then recursively calls this for the lines formed by the original points linked to new point C.
def subhull(a, P, Q):
    global convexHull
    s1 = []
    s2 = []
    if len(a) == 0:
        return
    C = farthestpoint(P, Q, a)
    convexHull.append(C)
    if isinstance(a[0], list) != 1:
        if (a[1] - P[1]) * (C[0] - P[0]) - (C[1] - P[1]) * (a[0] - P[0]) > 0:
            s1.append(a)
        elif (a[1] - C[1]) * (Q[0] - C[0]) - (Q[1] - C[1]) * (a[0] - C[0]) > 0:
            s2.append(a)
    elif isinstance(a[0], list) == 1:
        for i in range(len(a)):
            if (a[i][1] - P[1]) * (C[0] - P[0]) - (C[1] - P[1]) * (a[i][0] - P[0]) > 0:
                s1.append(a[i])
            elif (a[i][1] - C[1]) * (Q[0] - C[0]) - (Q[1] - C[1]) * (a[i][0] - C[0]) > 0:
                s2.append(a[i])
    subhull(s1, P, C)
    subhull(s2, C, Q)


# Given a set of points (convex), this function sorts these points in order of polar angle, then using a shoestring
# style algorithm determines the area of the n-gon.
def hullarea(hullpoints):
    comx = 0
    comy = 0
    sortedhull = []
    for i in range(len(hullpoints)):
        comx += hullpoints[i][0]
    comx = comx/len(hullpoints)
    for i in range(len(hullpoints)):
        comy += hullpoints[i][1]
    comy = comy/len(hullpoints)
    plt.scatter(comx, comy, color='g')
    for x, y in hullpoints:
        an = (math.atan2(y - comy, x - comx) + 2.0 * math.pi) % (2.0 * math.pi)
        sortedhull.append((x, y, an))
    sortedhull.sort(key = lambda tup: tup[2])
    newsortedhull = numpy.array(sortedhull)[:, 0:2]
    area = 0.0
    for i in range(len(newsortedhull)):
        j = (i + 1) % (len(newsortedhull))
        area += newsortedhull[i][0] * newsortedhull[j][1]
        area -= newsortedhull[j][0] * newsortedhull[i][1]
    area = abs(area) / 2.0
    for i in range(1, len(newsortedhull)):
        plt.plot([newsortedhull[i-1][0], newsortedhull[i][0]], [newsortedhull[i-1][1], newsortedhull[i][1]], 'k-')
    plt.plot([newsortedhull[len(newsortedhull)-1][0], newsortedhull[0][0]], [newsortedhull[len(newsortedhull)-1][1],
                                                                             newsortedhull[0][1]], 'k-')
    return area


# This is a set of running code. ###################################################
points = uniformpoints(50)
print(points)
quickhull(points)
numconvexHull = numpy.array(convexHull)
print("Points in convex hull: ")
print(numconvexHull)
for k in range(len(numconvexHull)):  # This plots the convex hull points in a new colour and links them together.
    plt.scatter(numconvexHull[k][0], numconvexHull[k][1], color='r')
totalhullarea = hullarea(numconvexHull)
print("The area of the hull is: ", totalhullarea)
plt.show()
# End running code ##################################################################


# TEST SPOT #########################################################################
convexHull = []
for i in range(10, 111, 20):
    print(i)
    points = uniformpoints(i)
    quickhull(points)
    numconvexHull = numpy.array(convexHull)
    totalhullarea = hullarea(numconvexHull)
    ratio = totalhullarea/i
    print("ratio is: ", ratio)


# TEST SPOT #########################################################################
convexHull = []
for i in range(10, 111, 20):
    print(i)
    points = gaussianpoints(i)
    quickhull(points)
    numconvexHull = numpy.array(convexHull)
    totalhullarea = hullarea(numconvexHull)
    ratio = totalhullarea/i
    print("ratio is: ", ratio)