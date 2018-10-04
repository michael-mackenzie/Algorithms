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
def uniformpoints(n, s):
    a = [0] * n
    for i in range(n):
        a[i] = [0] * 2
        a[i][0] = random.uniform(-5+s, 5+s)
        a[i][1] = random.uniform(-5, 5)
    return a


# Generates n random points around the origin as per a gaussian distribution.
def gaussianpoints(n):
    a = [0] * n
    for i in range(n):
        a[i] = [0] * 2
        a[i][0] = random.gauss(0, 2.5)
        a[i][1] = random.gauss(0, 2.5)
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


# Given a set of unsorted points, this functions sorts them in terms of their polar coordinate and returns the new list
def sortpolar(hullpoints):
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
    return newsortedhull


# Given a set of polarly-sorted points, this function draws the convex hull
def drawhull(hullpoints):
    newsortedhull = sortpolar(hullpoints)
    for i in range(1, len(newsortedhull)):
        plt.plot([newsortedhull[i-1][0], newsortedhull[i][0]], [newsortedhull[i-1][1], newsortedhull[i][1]], 'k-')
    plt.plot([newsortedhull[len(newsortedhull)-1][0], newsortedhull[0][0]], [newsortedhull[len(newsortedhull)-1][1],
                                                                             newsortedhull[0][1]], 'k-')


# This is a set of running code for Q1. ###########################################

points = uniformpoints(50, 0)  # Generate points
quickhull(points)  # Find convex hull of points
print("Q1 - Points in convex hull: ")
print(numpy.array(convexHull))
for i in range(len(points)):
    plt.scatter(points[i][0], points[i][1], color="b", label='data')
for k in range(len(convexHull)):  # This plots the convex hull points in a new colour and links them together.
    plt.scatter(convexHull[k][0], convexHull[k][1], color='r', label='hull')
drawhull(convexHull)
plt.title("Q1: Demonstration of Uniform Points QuickHull")
plt.show()

# TEST SPOT: Average Ratio of Uniform #
s = 0
avgr1 = 0
for i in range(10, 211, 20):
    convexHull = []
    s += 1
    points = uniformpoints(i, 0)
    quickhull(points)
    ratio1 = len(convexHull)/i
    avgr1 += ratio1
avgr1 = avgr1/s
print("Q1 (Uniform) Average ratio is: ", avgr1)

# End running code ################################################################


# This is a set of running code for Q2. ###########################################

convexHull = []
points = gaussianpoints(50)  # Generate points
quickhull(points)  # Find convex hull of points
print("Q2 - Points in convex hull: ")
print(numpy.array(convexHull))
for i in range(len(points)):
    plt.scatter(points[i][0], points[i][1], color="b", label='data')
for k in range(len(convexHull)):  # This plots the convex hull points in a new colour and links them together.
    plt.scatter(convexHull[k][0], convexHull[k][1], color='r', label='hull')
drawhull(convexHull)
plt.title("Q2: Demonstration of Gaussian Points QuickHull")
plt.show()

# TEST SPOT: Average Ratio of Gaussian #
t = 0
avgr2 = 0
for j in range(10, 211, 20):
    convexHull = []
    t += 1
    points = gaussianpoints(j)
    quickhull(points)
    ratio2 = len(convexHull)/j
    avgr2 += ratio2
avgr2 = avgr1/s
print("Q2 (Gaussian) Average ratio is: ", avgr2)

# End running code ################################################################


########################################################################################################################
# Question 3: Testing to see if two hulls intersect based on the bounding circle method.

def distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def doesintersect(com1, com2 , r1, r2):
    if r1 + r2 > distance(com1, com2):
        return 1
    else:
        return 0

def doeshullintersect(set1, set2):
    global convexHull
    convexHull = []
    quickhull(set1)
    set1hull = convexHull
    convexHull = []
    quickhull(set2)
    set2hull = convexHull
    comx1 = 0
    comy1 = 0
    comx2 = 0
    comy2 = 0
    for i in range(len(set1)):
        comx1 += set1[i][0]
    comx1 = comx1/len(set1)
    for i in range(len(set1)):
        comy1 += set1[i][1]
    comy1 = comy1/len(set1)
    for i in range(len(set2)):
        comx2 += set2[i][0]
    comx2 = comx2/len(set2)
    for i in range(len(set2)):
        comy2 += set2[i][1]
    comy2 = comy2/len(set2)
    com1 = [comx1, comy1]
    com2 = [comx2, comy2]
    r1 = 0
    for i in range(len(set1hull)):
        if set1hull[i][0] == 0:
            r1 = r1
        else:
            if distance(com1, set1hull[i]) > r1:
                r1 = distance(com1, set1hull[i])
    r2 = 0
    for j in range(len(set2hull)):
        if set2hull[j][0] == 0:
            r2 = r2
        else:
            if distance(com2, set2hull[j]) > r2:
                r2 = distance(com2, set2hull[j])
    c1 = plt.Circle((com1[0], com1[1]), radius=r1, color='b', fill=False)
    c2 = plt.Circle((com2[0], com2[1]), radius=r2, color='r', fill=False)
    fig, ax = plt.subplots()
    for j in range(len(set1)):
        plt.scatter(set1[j][0], set1[j][1], color='b')
    for j in range(len(set2)):
        plt.scatter(set2[j][0], set2[j][1], color='r')
    ax.add_patch(c1)
    ax.add_patch(c2)
    plt.axis('scaled')
    plt.title("Q3: Do The Bounding Circles Intersect?")
    plt.show()
    yn = doesintersect(com1, com2, r1, r2)
    if yn == 1:
        print("Q3. Do Hull Approximations Intersect: Yes")
    else:
        print("Q3. Do Hull Approximations Intersect: No")
    return


# Test the code ###########################
set1 = uniformpoints(10, 6)
set2 = uniformpoints(10, -6)
doeshullintersect(set1, set2)
###########################################


########################################################################################################################
# Question 4: Pseudo Code Testing to see if two hulls absolutely overlap or not.

"""
def properHullIntersect(hull_one, hull_two):
    draw line between polygons to determine orientation
    left_object = hull_one
    right_object = hull_two

    for (left_object)
        if(left_object(segment_i) does not intersect right_object and is on the right side of left_object)
            add line to separating_list
            
    for (right_object)
        if(right_object(segment_i) does not intersect left_object and is on the left side of right_object)
            add line to separating_list

    if (separating_list is empty):
        return (the hulls do intersect)
    else:
        return (the hulls don't intersect)
"""