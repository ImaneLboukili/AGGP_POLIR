#! usr/bin/env python
# -*- coding: utf-8 -*-

import networkx
import datetime
import time
from Individu import Individu
import random as rd
import numpy as np
import sys


#imports only above this line
#----------------------


class Population(object):
  """docstring for Population"""
  def __init__(self, nInd, N, M, method="random", logfile=False):
    
    self.nInd = nInd
    self.method = method

    self.logfile = logfile
    if self.logfile :
      with open(self.logfile, 'w') as o:
        pass

    log = "##========================="+\
          "\n## "+str(datetime.datetime.now())+" : Simulation started."+\
          "\n## Parameters are the following :" +\
          "\n##      nInd = "+str(self.nInd)+"  N = "+str(N)+"  M = "+str(M) +\
          "\n##      method = "+self.method
    
    self.wlog(log)

    # Population generation
    start_gen = time.time()
    self.pop = [Individu(N, M) for _ in range(self.nInd)]
    init_gen_time = time.time()-start_gen


    log = "\n## \n## "+str(datetime.datetime.now())+" : Generation of population done."+\
          "\n##      Done in "+str(init_gen_time)+"s\n"
    self.wlog(log)

    self.ech = None



  def wlog(self, log):
    if self.logfile:
      with open(self.logfile, 'a') as o :
        o.write(log)
    else :
      print log
    
    
  def selection(self, N):
  	# selects N individuals, which probability of selection is based on their fatness
  	if "roulette" == self.method:

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
  				
  		
  	if "lion" == self.method:
  		#returns the N individuals with the lowest fatness
  		rank = np.argsort([i.fat for i in pop])
  		self.ech = [pop[r] for r in rank[0:N]]

  		
  	if "random" == self.method :
  		#returns N random individuals
  		self.ech = rd.sample(pop, N)

  def crossing_over(self, A, B):
    # A and B are 2 Individu objects
    n = rd.randint(0, int((A.N-1)/2))
    C = A.copy()

    nodes_A = [rd.randint(0, A.N-1) for _ in range(n)]
    nodes_B = [rd.randint(0, B.N-1) for _ in range(n)]

    new_edges = []
    del_edges = []
    for i in range(n):
      # get the connections in graph B
      for b in B.G[nodes_B[i]]:
        if b in nodes_B:
          new_edges.append((nodes_A[i], b))

      # get existing connections in graph A
      for c in C.G[nodes_A[i]]:
        if c in nodes_A:
          del_edges.append((nodes_A[i], c))

    # remove edges from A and add the edges from B
    C.G.remove_edges_from(del_edges)
    C.G.add_edges_from(new_edges)
    return C


