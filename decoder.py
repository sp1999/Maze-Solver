#!/usr/bin/python

# Importing necessary libraries
import sys
import math
import random
import time
import numpy as np
import pulp as p
import matplotlib.pyplot as plt

grid_file_path = sys.argv[2]
value_and_policy_file_path = sys.argv[4]
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
grid_dict = {}
for i in range(len(grid)):
    for j in range(len(grid)):
        if grid[i][j] == 1:
            continue
        else:
            grid_dict[n] = (i,j)
            if grid[i][j] == 2:
                start = n
            if grid[i][j] == 3:
                end.append(n)
            n += 1
value_and_policy_file = open(value_and_policy_file_path,'r')
lines1 = value_and_policy_file.readlines()
value_and_policy_file.close()
policy = []
for line in lines1:
    l1 = line.strip().split()
    policy.append(int(l1[1]))
shortest_path = []
direction = {0:'N',1:'S',2:'W',3:'E'}
s = start 
while s not in end:
    shortest_path.append(direction[policy[s]])
    if policy[s] == 0: 
        i = grid_dict[s][0]
        j = grid_dict[s][1]
        t = 0
        for m in range(j,len(grid)):
            if grid[i-1][m] != 1:
                t += 1
        for m in range(j):
            if grid[i][m] != 1:
                t += 1
        s -= t
    elif policy[s] == 1:
        i = grid_dict[s][0]
        j = grid_dict[s][1]
        t = 0
        for m in range(j+1,len(grid)):
            if grid[i][m] != 1:
                t += 1
        for m in range(j+1):
            if grid[i+1][m] != 1:
                t += 1
        s += t
    elif policy[s] == 2:
        s -= 1
    else:
        s += 1
for path in shortest_path:
    print(path,end=' ')
print()