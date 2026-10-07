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
import numpy as np
import functools
# from numba import njit


# Exc1
def approximate_pi(n):
    #skapar listor
    nc = []
    nk = []

    #skapar n-värden
    for i in range(n):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if x**2 + y**2 <= 1:
            nc.append([x,y]) #röd
        else:
            nk.append([x,y]) #blå
            
    #beräkna pi
    # f = lambda n: 4*(len(nc)/(n))
    # pi = f(n)
    pi = 4*(len(nc)/(n))

    #separeta x och y värden
    nc_x = [ii[0] for ii in nc]
    nc_y = [ii[1] for ii in nc]
    nk_x = [ii[0] for ii in nk]
    nk_y = [ii[1] for ii in nk]

    #plottar och sparar figur
    plt.scatter(nc_x, nc_y, color='r')
    plt.scatter(nk_x, nk_y, color='b')
    plt.savefig("MA3_piplot.png")
    plt.show()
    
    return pi

# Exc2, approximation
def sphere_volume(n, d): 
    # n is the number of points
    # d is the number of dimensions of the sphere
    xc = 0 #i sfären

    #skapar n-värden
    for i in range(n):
        x_lst = [random.uniform(-1,1) for i in range(d)]
        x_sum = functools.reduce(lambda x, y: x + y, [ii**2 for ii in x_lst])
        if x_sum <= 1: 
            xc += 1

    #beräknar Vd(1)
    Vd1 = 2**d * (xc / n) #V(sfär)/ V(kub) 
    return Vd1  

#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points
    # d is the number of dimensions of the sphere 
    f = lambda d: (np.pi**(d/2))/(m.gamma(d/2 + 1))
    Vd2 = f(d)
    return Vd2

#Exc3: numba version
# @njit
# def sphere_volume_numba(n:int, d:int)->float:
#     # n is the number of points
#     # d is the number of dimensions of the sphere
#     xc = 0 #i sfären

#     #skapar n-värden
#     for i in range(n):
#         x_lst = [random.uniform(-1,1) for i in range(d)]
#         x_sum = sum([ii**2 for ii in x_lst])
#         if x_sum <= 1: 
#             xc += 1

#     #beräknar Vd(1)
#     Vd1 = 2**d * (xc / n) #V(sfär)/ V(kub) 
#     return Vd1  

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes

    point_per_process = [n // np] * np #skapar lista
    d2 = [d] * np #skapar lista

    with future.ProcessPoolExecutor(max_workers=np) as ex:
        results = ex.map(sphere_volume, point_per_process, d2)

    Vd1 = sum(results) / np
    return Vd1
    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    # Exc2
    n = 100000
    d = 2
    sphere_volume(n, d)
    print(sphere_volume(n, d), hypersphere_exact(n,d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n, d)
    print(sphere_volume(n, d), hypersphere_exact(n,d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # # Exc3
    # n = 1000000
    # d = 11
    # for i in range(3):
    #     start = pc()
    #     sphere_volume(n, d)
    #     stop = pc()
    #     print(f"Exc3: Sequential time of {d} and {n}: {stop-start}")
    # for i in range(3):
    #     start2 = pc()
    #     sphere_volume_numba(n, d)
    #     stop2 = pc()
    #     print(f"What is numba time?: {stop2-start2}")

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    start2 = pc()
    sphere_volume_parallel(n,d)
    stop2 =pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    print(f"What is parallel time? {stop2-start2}")

    
    

if __name__ == '__main__':
	main()
