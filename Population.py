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

  def crossing_over(self, A, B):
    n = rd.randint(0, A.N-1)
    C = A.copy()

    nodes_A = [rd.randint(0, A.N-1) for _ in range(n)]
    nodes_B = [rd.randint(0, B.N-1) for _ in range(n)]

    new_edges = []
    del_edges = []
    for i in range(n):
      # get the connections in graph B
      j = 0
      for b in B.G[nodes_B[i]]:
        if b in nodes_B:
          new_edges.append((nodes_A[i], nodes_A[j]))
        j += 1

      # get existing connections in graph A
      j = 0
      for c in C.G[nodes_A[i]]:
        if c in nodes_A:
          del_edges.append((nodes_A[i], nodes_A[j]))
        j += 1

    # remove edges from A and add the edges from B
    C.G.remove_edges_from(del_edges)
    C.G.add_edges_from(new_edges)
    return C


