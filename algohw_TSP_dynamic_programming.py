# -*- coding: utf-8 -*-
"""
Created on Fri May 14 00:29:59 2021

@author: User
"""

import numpy as np
from itertools import combinations
from sys import maxsize
import time
import algohw_TSP_genetic
import matplotlib.pyplot as plt


def createMatrix(n):
    W = np.random.randint(low = 1, high = 30, size=(n, n))
    for i in range(n):
        for j in range(n):
            if i==j:
                W[i][j] = 0
            elif i>j:
                W[i][j] = W[j][i]
    return n, W


def traveling_salesperson_DP(n, W):
    start_time = time.time()
    D={}
    P={}
    for i in range(1, n):
        D[str(i),()] = W[i][0]
        P[str(i),()] = 0
    
    d_set = [i for i in range(1, n)]
    
    
    for k in range(1, n-1):
        com_set = tuple(combinations(d_set,k)) #((1,),(2,)...)
        
        
        for a in range(len(com_set)):
            A = com_set[a]
            not_A = set(d_set)-set(A)
            A = tuple(sorted(A))
            not_A = tuple(sorted(not_A))
            d_set = tuple(sorted(d_set))
            
            #R=A-{j}
            R=[]
            for j in A:
                temp_R = set(A)-{j}
                temp_R = tuple(sorted(temp_R))
                R.append(temp_R)
            
            for i in not_A:
                j_smallest = 0
                j_path = maxsize
                for (j, r) in zip(A, R):
                    temp = W[i][j]+D[str(j),r]
                    if temp < j_path:
                        j_path = temp
                        j_smallest = j
                D[str(i),A] = j_path
                P[str(i),A] = j_smallest
    
    #印出Shortest Path
    j_smallest_final=0
    j_path_final = maxsize
    for j in d_set:
        d_set_temp = sorted(d_set).copy()
        d_set_temp = tuple(sorted(set(d_set_temp)-{j}))
        temp_final = W[0][j]+D[str(j),d_set_temp]
        if temp_final < j_path_final:
            j_path_final = temp_final
            j_smallest_final = j
    d_set_temp = tuple(sorted(d_set).copy())
    D[str(0),d_set_temp] = j_path_final
    P[str(0),d_set_temp] = j_smallest_final
    
#    print("Shortest length:", j_path_final)
    
    #印出最後的P
    path = [0]
    d_set_copy_final = list(d_set).copy()
    path.append(j_smallest_final)
    for i in range(len(d_set_copy_final)-1):
        d_set_copy_final = set(d_set_copy_final)-{j_smallest_final}
        j_smallest_final = P[str(j_smallest_final),tuple(sorted(d_set_copy_final))]
        path.append(j_smallest_final)
    path.append(0)
#    print("Path:", path)
    end_time = time.time()
#    print("Run time:", end_time-start_time)
    return j_path_final, end_time-start_time


#main
average_sl_total = []
average_rt_DP_total = []
average_rt_genetic_total = []
for n in range(4, 21):
    average_sl = []
    average_rt_DP = []
    average_rt_genetic = []
    for i in range(5):
        print("n=", n, ", number of time=", i+1)
        n, W = createMatrix(n)
#        print("Dynamic programming:")
        shortest_length_DP, runtime_DP = traveling_salesperson_DP(n, W)
#        print("Genetic:")
        shortest_length_genetic, runtime_genetic = algohw_TSP_genetic.traveling_salesperson_genetic(n, W)
        
        average_sl.append((shortest_length_genetic-shortest_length_DP)/shortest_length_DP)
        average_rt_DP.append(runtime_DP)
        average_rt_genetic.append(runtime_genetic)
    average_sl_total.append(np.mean(average_sl))
    average_rt_DP_total.append(np.mean(average_rt_DP))
    average_rt_genetic_total.append(np.mean(average_rt_genetic))
#print(average_sl_total)
#print(average_rt_DP_total)
#print(average_rt_genetic_total)

#畫圖
plt.figure(figsize=(6,2.5))
plt.subplot(1, 2, 1)
Data_1, = plt.plot([n for n in range(4, 21)],average_rt_DP_total,'s-',color = 'r', label="DP")
Data_2, = plt.plot([n for n in range(4, 21)],average_rt_genetic_total,'o-',color = 'g', label="genetic")
plt.xlabel("n", fontsize=8)
plt.ylabel("Average Runtime", fontsize=8)
plt.legend(handles=[Data_1, Data_2])
plt.title("Picture 1", fontsize=8)

plt.subplot(1, 2, 2)
plt.plot([n for n in range(4, 21)],average_sl_total,'o-',color = 'b')
plt.xlabel("n", fontsize=8)
plt.ylabel("Average Deviation", fontsize=8)
plt.title("Picture 2", fontsize=8)

plt.tight_layout() #防止兩個圖重疊
plt.show()