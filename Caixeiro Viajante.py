# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:41:59 2020

@author: Altair Dias dos Santos Junior
"""

import math
import numpy as np
import Selection as sel
import Substitution as sub
from copy import copy
import time
import matplotlib.pyplot as plt

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
                        
    # for i in range(len(indiv)):
    #     for j in range(i+1,len(indiv)):
    #         fit += math.sqrt( 
    #                         (indiv[i][0]-indiv[j][0])**2 
    #                         +
    #                         (indiv[i][1]-indiv[j][1])**2
    #                     )
    return fit

def generateIndiv():
    indiv = []
    for i in range(cities):
        indiv.append([np.random.randint(70),np.random.randint(70)])
    return indiv

def generatePop():
    pop = []
    for i in range(pop_count):
        pop.append(generateIndiv())
    return pop

def readPop():
    data = np.loadtxt(".\\base.txt")
    #remove os indexes
    data = data[:,1:]
    return np.array([ (np.random.shuffle(data),copy(data.tolist())) for i in range(pop_count)])[:,1]

def crossoverSplit(pop,l,pc,isDual=False):
    ret = []
    size = int(len(pop)/2)
    for i in range(size):
        prob = np.random.uniform(0,high=1)
        if prob <= pc:
            if isDual:
                pos = np.random.randint(len(pop[i])-l)
                split = pop[i,pos:pos+l]
                s1 = np.concatenate((pop[i,:pos],split,pop[i*2-1,pos+l:]))
                split = pop[i*2-1,pos:pos+l]
                s2 = np.concatenate((pop[i*2-1,pos+l:],split,pop[i,:pos]))
            else:                    
                s1 = np.concatenate((pop[i,:l],pop[i*2-1,l:]))
                s2 = np.concatenate((pop[i*2-1,:l],pop[i,l:]))
            
            if(isValid(s1) and isValid(s2)):
                ret.append(s1)
                ret.append(s2)
        else:
            ret.append(pop[i])
            ret.append(pop[i*2-1])
    return np.array(ret)

def mutate(indiv):
    indiv = copy(indiv)
    r = np.random.randint(len(indiv))
    r_tmp = np.random.randint(len(indiv))
    flip = indiv[r]
    indiv[r] = indiv[r_tmp]
    indiv[r_tmp] = flip
    return indiv

def crossoverDualSplit(pop,l,pc):
     return crossoverSplit(pop,l,pc,True).tolist()

#pop = generatePop()

xx = []
yy = []
fits = []

for execucao in range(1):
    pop = readPop().tolist()
    fit_arr = [caixFitness(indiv) for indiv in pop]
    m = 99999999
    t = time.time()
    
    x = []
    y = []
    xx.append(0)
    yy.append(min(fit_arr))
    for k in range(60000):
        fit_arr = [caixFitness(indiv) for indiv in pop]
        if k%10 == 0:
            xx.append(time.time()-t)
            yy.append(min(fit_arr))

        if min(fit_arr) < m:
            m = min(fit_arr)
            print(m,time.time()-t)
        
        #Array com probabilidade de selecao
        s_prob = sel.probLRArray(fit_arr,2) # <--------------------------- Prob Selecao
        
        #Coloca indexes para serem utilizados apos o filtro da array
        s_prob = np.array(sel.indexify(s_prob))
        
        #Gera a probabilidade de selecao
        prob = np.random.uniform(0,high=1)
        
        #Filtra o array com quem possui a probabilidade de ser selecionado
        s_prob = s_prob[s_prob[:,0]>=prob]
        selected = []
        
        #gera o array com os selecionados
        for i in range(len(s_prob)):
            index = int(s_prob[i,1])
            selected.append(copy(pop[index])) # <---------------------------- Selecao
        selected = np.array(selected)
        
        #faz o cruzamento
        qt = crossoverDualSplit(selected,np.random.randint(4)+1,0.8) # <-------------------- Cruzamento
        
        #faz a mutacao
        for i in range(len(qt)):    
            prob = np.random.uniform(0,high=1)
            if prob <= 0.5:
                qt[i] = mutate(qt[i]) # <------------------------------ Mutacao
        
        qt = [e for e in qt if e not in pop]
        
        pop+=qt
        fit_arr = [caixFitness(indiv) for indiv in pop]
        pop = sub.getBestIndivs(pop,fit_arr,pop_count,minimize=True)# <---------------------- Substituicao
    



# plt.plot(xx[0],np.mean(yy,axis=0).tolist(),label="Media")
# plt.plot(xx[0],np.amin(yy,axis=0).tolist(),label="Minimo")
plt.plot(xx,yy,label="Minimo")
plt.legend(loc="upper right")
plt.xlabel('Tempo (s)')
plt.ylabel('FO - Unidades de Distancia')
plt.title('TSP')
plt.grid(True)
# print ("probProportinalArr: ",sel.probProportinalArr(fit_arr))
# print ("probLRArray: ",sel.probLRArray(fit_arr,2))
# print ("rouletteIndex: ",pop[sel.rouletteIndex(sel.probProportinalArr(fit_arr))])
