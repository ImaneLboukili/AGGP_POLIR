#! usr/bin/env python
# -*- coding: utf-8 -*-

import networkx
import time
from Individu import Individu
import random as rd
import numpy as np

#imports only above this line
#----------------------


class Population(object):
  """docstring for Population"""
  def __init__(self, nInd, N, M):
    
    self.nInd = nInd
    self.pop = [Individu(N, M) for _ in range(self.nInd)]
    self.ech = None
    
    
  def selection(self, N, method = "random"):
  	# selects N individuals, which probability of selection is based on their fatness
  	if "roulette" == method:

  		sum_fat = sum([i.fat for i in self.pop])
  		probas = [i.fat/sum_fat for i in self.pop]
  		selected_ind = []
  		self.ech = []
  		ind = None

  		while len(self.ech)<N :
  			while ind in selected_ind or ind == None:
  				
  				ind = rd.randint(0, self.nInd-1)
  				print ind
  				
  			if(probas[ind]<rd.random()):
  				self.ech.append(self.pop[ind])
  				selected_ind.append(ind)
  				
  		
  	if "lion" == method:
  		#returns the N individuals with the lowest fatness
  		rank = np.argsort([i.fat for i in pop])
  		self.ech = [pop[r] for r in rank[0:N]]

  		
  	if "random" == method :
  		#returns N random individuals
  		return rd.sample(pop, N)

Pop = Population(20, 40, 2)
print "fatness de la pop initiale : ",[i.fat for i in Pop.pop]
	
Pop.selection(3, method="roulette")
print "fatness selectionnees : ",[i.fat for i in Pop.ech]
