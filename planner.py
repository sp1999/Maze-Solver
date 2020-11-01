#!/usr/bin/python

# Importing necessary libraries
import sys
import math
import random
import time
import numpy as np
import pulp as p
import matplotlib.pyplot as plt

mdp_file_path = sys.argv[2]
algorithm = sys.argv[4]
mdp_file = open(mdp_file_path,'r')
lines = mdp_file.readlines()
n = int(lines[0].strip().split()[1])
k = int(lines[1].strip().split()[1])
start = int
end = []
T = np.array([[[0. for i in range(n)] for a in range(k)] for j in range(n)])
R = np.array([[[0. for i in range(n)] for a in range(k)] for j in range(n)])
mdptype = str
gamma = float
for line in lines:
    l = line.strip().split()
    if l[0] == 'numStates':
        n = int(l[1])
    elif l[0] == 'numActions':
        k = int(l[1])
    elif l[0] == 'start':
        start = int(l[1])
    elif l[0] == 'end':
        for idx in range(1,len(l)):
            end.append(int(l[idx]))
    elif l[0] == 'transition':
        T[int(l[1])][int(l[2])][int(l[3])] = float(l[5])
        R[int(l[1])][int(l[2])][int(l[3])] = float(l[4])
    elif l[0] == 'mdptype':
        mdptype = l[1]
    else:
        gamma = float(l[1])
mdp_file.close()

def value_iteration(n,k,T,R,gamma,mdptype,end):
    precision = 1e-12
    V_prev = np.array([0. for _ in range(n)])
    V = np.array([0. for _ in range(n)])
    t = 0
    while True:
        V = np.amax(np.sum((T*(R+(gamma*V_prev))),axis = 2),axis = 1)
        if t and ((np.max(np.abs(np.subtract(V,V_prev)))) <= precision):
            break
        V_prev = V.copy()
        t += 1  
    return V,np.argmax(np.sum((T*(R+(gamma*V))),axis = 2),axis = 1)

def policy_evaluation(n,k,T,R,gamma,pi):
    V = np.array([0. for _ in range(n)])
    Q = np.array([[0. for _ in range(k)] for _ in range(n)])
    A = np.array([[0. for _ in range(n)] for _ in range(n)])
    B = np.array([0. for _ in range(n)])
    A = -gamma*T[range(len(pi)),pi]
    np.fill_diagonal(A, np.diag(A) + 1) 
    B = np.sum(T[range(len(pi)),pi]*R[range(len(pi)),pi], axis = 1)    
    V = np.linalg.solve(A,B)
    Q = np.sum(T*(R+gamma*V),axis = 2)
    return V,Q
    
def policy_iteration(n,k,T,R,gamma):
    pi = np.array([0 for _ in range(n)])
    IA = [[] for i in range(n)]
    IS = set()
    V,Q = policy_evaluation(n,k,T,R,gamma,pi)
    for i in range(n):
        for a in range(k):
            if Q[i][a] > V[i]:
                IA[i].append(a)
    for i in range(n):
        if len(IA[i]) >= 1:
            IS.add(i)
    t = 0
    while len(IS):
        for s in IS:
            action = IA[s][0]
            for a in IA[s]:
                if Q[s][a] > Q[s][action]:
                    action = a
            pi[s] = action
        IA = [[] for i in range(n)]
        IS = set()
        V,Q = policy_evaluation(n,k,T,R,gamma,pi)
        for i in range(n):
            for a in range(k):
                if (Q[i][a] - V[i]) > 1e-6:
                    IA[i].append(a)
        for i in range(n):
            if len(IA[i]) >= 1:
                IS.add(i)
        t += 1
    return V,pi

def linear_programming(n,k,T,R,gamma):
    Q = np.array([[0. for _ in range(k)] for _ in range(n)])
    pi = np.array([0 for _ in range(n)])
    prob = p.LpProblem('MDP_Problem',p.LpMaximize)
    V = p.LpVariable.dicts('V',[i for i in range(n)])
    prob += p.lpSum([-V[i] for i in range(n)])
    for i in range(n):
        for a in range(k):
            prob += p.lpSum([(1-(gamma*T[i][a][j])) * V[j] if (i == j) else (-gamma*T[i][a][j]) * V[j] for j in range(n)]) >= sum(T[i][a][j]*R[i][a][j] for j in range(n))
    status = prob.solve(p.PULP_CBC_CMD(msg = 0))
    V_values = np.array([V[i].varValue for i in range(n)])
    Q = np.sum(T*(R+(gamma*V_values)),axis = 2)
    pi = np.argmax(Q,axis = 1)
    return V_values,pi

if algorithm == 'vi':
    V,pi = value_iteration(n,k,T,R,gamma,mdptype,end)
elif algorithm == 'hpi':
    V,pi = policy_iteration(n,k,T,R,gamma)
else:
    V,pi = linear_programming(n,k,T,R,gamma)
for i in range(n):
    print(V[i],pi[i])
