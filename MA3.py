""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
from numba import njit
import concurrent.futures as future
# Exc1
def approximate_pi(n):
    # nc is points inside of circle only. n is all points, becauase the area of the square contains all points
    # area of circle
    # as n grows, we come closer to the true value of pi. pi = 4 nc/n
    # n is the number of points. n= ns + nc
    # we need nc
    #1 produce random points betwee -1 1. n times
    #2 check if points are inside or outside circle
    #3 use len(inside_points) to get nc
    #4 approximate pi using nc

    print(n)

    count = 0
    inside_points = []
    outside_points = []

    while count < n:
        x = random.uniform(-1,1)
        y = random.uniform(-1, 1)

        if (pow(x,2) + pow(y,2))  <= 1:
            inside_points.append([x,y])
        else:
            outside_points.append([x,y])

        count = count + 1

    nc = len(inside_points)

    approximate = 4 * (nc/n)

    x_inside_values = []
    y_inside_values = []
    x_outside_values = []
    y_outside_values = []

    for point in inside_points:
        x_inside_values.append(point[0])
        y_inside_values.append(point[1])

    for point in outside_points:
        x_outside_values.append(point[0])
        y_outside_values.append(point[1])


    #plot

    plt.scatter(x_inside_values, y_inside_values, color="red")
    plt.scatter(x_outside_values, y_outside_values, color="blue")
    plt.savefig(f"approximate_pi_{n}.png")

    print(f"Approximate of pi: {approximate}")
    return approximate

# Exc2, approximation
def sphere_volume(n, d): 
    # n is the number of points
    # d is the number of dimensions of the sphere

    count = 0
    nc = 0

    # think matrix. each row is a point and each col is a coord
    while count < n:
        point = [random.uniform(-1,1) for _ in range(d)]
        #conidtion: if the sum is less than or equal to 1, add to nc
        if sum(map(lambda coord: pow(coord, 2), point)) <= 1:
            nc = nc + 1
        count = count + 1

    approximate = pow(2,d) * (nc/n)
    #print(f"Approximate value: {approximate}")

    return approximate

#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points

    # d is the number of dimensions of the sphere

    volume = (pow(m.pi,d/2))/(m.gamma((d/2)+1))

    return volume

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float:
    # n is the number of points

    # d is the number of dimensions of the sphere
    #np is the number of processes
    count = 0
    nc = 0

    # think matrix. each row is a point and each col is a coord
    while count < n:
        point = [random.uniform(-1,1) for _ in range(d)]
        #conidtion: if the sum is less than or equal to 1, add to nc
        sum_sq = 0.0
        for coord in point:
            sum_sq = sum_sq + coord ** 2
        if sum_sq <= 1:
            nc = nc + 1

        count = count + 1

    approximate = pow(2,d) * (nc/n)
    print(f"Approximate value: {approximate}")

    return approximate


#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes

    x = n//np
    process = []
    approximate = 0

    # each process gets x ammount of points
    # we add each result into a list to then get the approximate result values
    # then we get average of each value, since we used 10 processes for same task
    with future.ProcessPoolExecutor() as ex:
        for _ in range(np):
            process.append(ex.submit(sphere_volume, x, d))
        for i in process:
            approximate = approximate + i.result()


    average_approximate = approximate/np

    return average_approximate


    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    # Exc2
    n = 100000
    d = 2
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    n = 1000000
    d = 11

    #python version, faster after first run
    for i in range(3):
        start = pc()
        sphere_volume(n, d)
        stop = pc()

        print(f" RUN {i} Exc3: Sequential time of {d} and {n}: {stop - start}")

    print("What is numba time?")

    #numba version generally same times, no speed up
    for i in range(3):
        start = pc()
        sphere_volume_numba(n, d)
        stop = pc()

        print(f" NUMBA RUN {i} Exc3: Sequential time of {d} and {n}: {stop - start}")

    # Exc4
    n = 1000000
    d = 11
    for i in range(3):
        start = pc()
        sphere_volume(n, d)
        stop = pc()
        print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")

    print("What is parallel time?")

    for i in range(3):
        start = pc()
        sphere_volume_parallel(n, d, 10)
        stop = pc()
        print(f"Exc4: Parallel time of {d} and {n}: {stop-start}")

    
    

if __name__ == '__main__':
	main()
