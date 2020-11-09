# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 13:14:14 2020

@author: Junior
"""

import math
import numpy as np
import Selection as sel
import Substitution as sub
from copy import deepcopy,copy
import time
import matplotlib.pyplot as plt

import multiprocessing as mp

cities = 131
pop_count = 4
def singleDistance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def isValid(indiv):
    indiv = indiv.tolist()
    #print(indiv)
    result = [x for x in indiv if indiv.count(x) > 1]
    return len(result) == 0

def caixFitness(indiv):
    fit = 0
    for i in range(len(indiv)-1):
        fit += singleDistance(indiv[i][0],indiv[i][1],indiv[i+1][0],indiv[i+1][1])
                        
    return fit

def distArray(indiv):
    arr = []
    for i in range(indiv.shape[0]-1):
        dist = singleDistance(indiv[i][0],indiv[i][1],indiv[i+1][0],indiv[i+1][1])
        arr.append(dist)
    return arr

def readIndiv():
    data = np.loadtxt(".\\base.txt")
    #remove os indexes
    data = data[:,1:]
    np.random.shuffle(data)
    return copy(data)

def greedIndiv(data):
    data = deepcopy(data)
    np.random.shuffle(data)
    for i in range (1000):
        dist_arr = distArray(data)
        rank_dist = sel.getRankArray(dist_arr)
        m_idx = rank_dist.index(max(rank_dist))
        # m_idx = np.random.randint(data.shape[0]-1)
        #s_idx = getClosest(m_idx,data)
        s_idx = np.random.randint(data.shape[0])
        tmp = deepcopy(data)
        if(s_idx >= 0 and s_idx != m_idx+1):
            #print("Swap: ",data[s_idx],data[m_idx+1],m_idx,s_idx)
            tmp[[s_idx,m_idx+1]] = tmp[[m_idx+1,s_idx]]
            if caixFitness(tmp) < caixFitness(data):
                data = tmp
    return data

def generatePop():
    pop = []
    for i in range(mp.cpu_count()):
        pop.append(readIndiv())
    return pop

def mutate(orig_indiv):
    orig_indiv = deepcopy(orig_indiv)
    fit = caixFitness(orig_indiv)
    for i in range(10000):
        indiv = deepcopy(orig_indiv)
        r = np.random.randint(indiv.shape[0])
        r_tmp = np.random.randint(indiv.shape[0])
        if r == r_tmp:
            continue
        indiv[[r,r_tmp]] = indiv[[r_tmp,r]]
        new_fit = caixFitness(indiv)
        if new_fit < fit:
            fit = new_fit
            orig_indiv = deepcopy(indiv)
            continue
    return indiv


if __name__ == "__main__":
    xx = []
    yy = []
    fits = []
    
    for execucao in range(1):
        m = 99999999
        t = time.time()
        #indiv = deepcopy(readIndiv())
        pop = generatePop()
        fit_arr = [caixFitness(indiv) for indiv in pop]
        t = time.time()
        xx.append(0)
        yy.append(min(fit_arr))
        
        for k in range(10):
            
            p = mp.Pool()
            candidates = p.map(greedIndiv, pop)
            p.close()
            p.join()
            
            #candidates = [greedIndiv(indiv) for indiv in pop]
            #indiv_tmp,_ = greedIndiv(indiv)
            
            p = mp.Pool()
            candidates = p.map(mutate, candidates)
            p.close()
            p.join()
            
            #candidates = [mutate(indiv) for indiv in candidates]
            
            fit_arr = [caixFitness(indiv) for indiv in pop]
            print(fit_arr)
            fit_arr_candidates = [caixFitness(indiv) for indiv in candidates]
            fit_all = fit_arr + fit_arr_candidates
            fit = sel.getRankArray(fit_all)
            n_pop = pop + candidates
            pop = []
            for foo in range(mp.cpu_count()):
                pop.append(n_pop[fit.index(foo)])
            
            
            xx.append(time.time()-t)
            yy.append(min(fit_all))
            
            # indiv_local = mutate(indiv_tmp)
            # if (caixFitness(indiv_local) < caixFitness(indiv)):
            #     indiv = deepcopy(indiv_local)
            # y.append(caixFitness(indiv))
    
    
    #plt.plot(list(range(len(yy))),np.mean(yy,axis=0).tolist(),label="Media")
    plt.plot(xx,yy,label="Minimo")
    plt.legend(loc="upper right")
    plt.xlabel('Tempo (s)')
    plt.ylabel('FO - Unidades de Distancia')
    plt.title('TSP')
    plt.grid(True)
    # print ("probProportinalArr: ",sel.probProportinalArr(fit_arr))
    # print ("probLRArray: ",sel.probLRArray(fit_arr,2))
    # print ("rouletteIndex: ",pop[sel.rouletteIndex(sel.probProportinalArr(fit_arr))])
