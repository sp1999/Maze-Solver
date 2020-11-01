#!/usr/bin/python

# Importing necessary libraries
import sys
import math
import random
import time
from collections import defaultdict
import numpy as np
import pulp as p
import matplotlib.pyplot as plt

grid_file_path = sys.argv[2]
grid_file = open(grid_file_path,'r')
lines = grid_file.readlines()
grid_file.close()
grid = []
for line in lines:
    l = list(map(int,line.strip().split()))
    grid.append(l)
start = 0
end = []
n = 0
for i in range(len(grid)):
    for j in range(len(grid)):
        if grid[i][j] == 1:
            continue
        else:
            if grid[i][j] == 2:
                start = n
            if grid[i][j] == 3:
                end.append(n)
            n += 1
T = defaultdict(lambda: 0)
R = defaultdict(lambda: 0)
gamma = 1
c = 0
for i in range(len(grid)):
    for j in range(len(grid)):
        if grid[i][j] == 3:
            c += 1
            continue
        elif grid[i][j] == 1:
            continue
        else:
            if i >= 1:
                t = 0
                for m in range(j,len(grid)):
                    if grid[i-1][m] != 1:
                        t += 1
                for m in range(j):
                    if grid[i][m] != 1:
                        t += 1 
                if grid[i-1][j] == 0:
                    T[(c,0,c-t)] = 1
                    R[(c,0,c-t)] = -1
                elif grid[i-1][j] == 2:
                    T[(c,0,c-t)] = 1
                    R[(c,0,c-t)] = -1
                elif grid[i-1][j] == 3:
                    T[(c,0,c-t)] = 1
                    R[(c,0,c-t)] = 100000
                else:
                    T[(c,0,n)] = 1
                    R[(c,0,n)] = -100000
            if i < len(grid)-1:
                t = 0
                for m in range(j+1,len(grid)):
                    if grid[i][m] != 1:
                        t += 1
                for m in range(j+1):
                    if grid[i+1][m] != 1:
                        t += 1
                if grid[i+1][j] == 0:
                    T[(c,1,c+t)] = 1
                    R[(c,1,c+t)] = -1
                elif grid[i+1][j] == 2:
                    T[(c,1,c+t)] = 1
                    R[(c,1,c+t)] = -1
                elif grid[i+1][j] == 3:
                    T[(c,1,c+t)] = 1
                    R[(c,1,c+t)] = 100000
                else:
                    T[(c,1,n)] = 1
                    R[(c,1,n)] = -100000
            if j >= 1:
                if grid[i][j-1] == 0:
                    T[(c,2,c-1)] = 1
                    R[(c,2,c-1)] = -1
                elif grid[i][j-1] == 2:
                    T[(c,2,c-1)] = 1
                    R[(c,2,c-1)] = -1
                elif grid[i][j-1] == 3:
                    T[(c,2,c-1)] = 1
                    R[(c,2,c-1)] = 100000
                else:
                    T[(c,2,n)] = 1
                    R[(c,2,n)] = -100000
            if j < len(grid)-1:
                if grid[i][j+1] == 0:
                    T[(c,3,c+1)] = 1
                    R[(c,3,c+1)] = -1
                elif grid[i][j+1] == 2:
                    T[(c,3,c+1)] = 1
                    R[(c,3,c+1)] = -1
                elif grid[i][j+1] == 3:
                    T[(c,3,c+1)] = 1
                    R[(c,3,c+1)] = 100000
                else:
                    T[(c,3,n)] = 1
                    R[(c,3,n)] = -100000
            c += 1
print('numStates {}'.format(n+1))
print('numActions {}'.format(4))
print('start {}'.format(start))
print('end {}'.format(n),end = ' ')
for x in range(len(end)):
    if (x+1) == len(end):
        print('{}'.format(end[x]))
    else:
        print('{}'.format(end[x]),end = ' ')
for x,y,z in T:
    print('transition {} {} {} {} {}'.format(x,y,z,R[(x,y,z)],T[(x,y,z)]))
print('mdptype episodic')
print('discount {}'.format(gamma))
