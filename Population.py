#! usr/bin/env python
# -*- coding: utf-8 -*-

import networkx
import time
from Individu import Individu
import random as rd
import numpy as np


############## j'attends d'avoir le constructeur de classe, a ce moment la il faudra remplacer les pop par self.pop

pop = [Individu(40, 2) for i in range(0,5)]
print "fatness de la pop initiale : ",[i.fat for i in pop]

#----------------------

def selection(N, method = "random"):
	#returns N individuals, which probability of selection is based on their fatness
	if (method == "roulette"):
		sum_fat = sum([i.fat for i in pop])
		probas = [i.fat/sum_fat for i in pop]
		selected_ind = []
		selected = []
		ind = None
		while(len(selected)<N):
			while(ind in selected_ind or ind == None):
				
				ind = rd.randint(0,len(pop)-1)
				print ind
				
			if(probas[ind]<rd.random()):
				selected.append(pop[ind])
				selected_ind.append(ind)
				
		return selected
		
	if(method == "lion"):
		#returns the N individuals with the lowest fatness
		rank=np.argsort([i.fat for i in pop])
		return[pop[r] for r in rank[0:N]]
		
	if(method == "random"):
		#returns N random individuals
		return rd.sample(pop, N)
		
res = selection(3, "roulette")
print "fatness selectionnees : ",[i.fat for i in res]
