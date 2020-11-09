# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 14:53:46 2020

@author: Altair Dias dos Santos Junior
"""

import numpy as np
import random
import copy

def probProportinalArr(fit_arr):
    mean = np.mean(fit_arr)
    count = len(fit_arr)
    return [round(fit_arr[i]/(mean*count),2) for i in range(count)]

#retorna array de rank
#menor rank = 0
#maior rank = len(arr)-1
def getRankArray(fit_arr):
    array = np.array(fit_arr)
    order = array.argsort()
    ranks = order.argsort()
    return list(ranks)

def probLRArray(fit_arr,s):
    rank = getRankArray(fit_arr)
    probs = [(2-s)/len(fit_arr) + (2*rank[i]*(s-1))/(len(fit_arr)*rank[len(rank)-1])for i in range(len(rank))]
    return probs

def rouletteIndex(prob_arr):
    prob_arr = indexify(prob_arr)
    prob_arr = np.array(prob_arr)
    prob_arr = prob_arr[prob_arr[:,0].argsort()]
    running = np.cumsum(prob_arr[:,0])
    final = np.insert(prob_arr,2,running,axis=1)
    r = round(random.uniform(0,1),2)
    filtered = final[final[:,2]>=r]
    return int(filtered[0,1])

def indexify(arr):
    indexes = [arr.index(x) for x in arr]
    return [[arr[i],indexes[i]] for i in range(len(arr))]

def tournamentIndex(fit_arr,count):
    if count > len(fit_arr)-1:
        return
    tmp = copy.copy(fit_arr)
    random.shuffle(tmp)
    best = max(tmp[0:count])
    indexed = np.array(indexify(fit_arr))
    return indexed[indexed[:,0]==best][0,1]
    