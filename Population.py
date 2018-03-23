#! usr/bin/env python
# -*- coding: utf-8 -*-

import networkx
import datetime
import time
from Individu import Individu
import random as rd
import numpy as np
import sys
import networkx as nx

# In theory, it's better to use this for classes and stuff but 
# it's not installed and it's kind of a pain...

#from pathos.multiprocessing import ProcessingPool as Pool

# SO. Instead, we use the basic version which needs to be able to convert
# the functions with cPickle (ie. no class methods etc.) This means, we'll need
# to externalize some functions to muliprocess them. It's ugly but hey, whatever works...
from multiprocessing import Pool


#imports only above this line
#----------------------


# exists because of Pool
def mk_i(nm):
  return Individu(nm[0], nm[1], nm[2])

# is outside of class because of Pool
def evolve(Pop):
  # Get mother indiv from selected
  mother = Pop.ech[rd.randint(0, Pop.echsize-1)]

  while True:
    try:
      # Create child
      child = mother.copy()
      
      # Eventual modifications to child
      p = rd.random()

      if p < Pop.pMut:
        child.basic_mut()

      if p < Pop.pCros:
        father = Pop.pop[rd.randint(0, Pop.nInd-1)]
        child1 = Pop.crossing_over(child, father)
        child = child1.copy()

      #update fatness
      child.fat = child.fatness()
      break
    except nx.NetworkXError :
      # if the child has a disconnected graph, an error will be raised so 
      # the child dies and another one is produced.
      pass
  return child

def bfs(graph, start, N, path=[]):
  queue = [start]
  while (queue and len(path) < N):
   vertex = queue.pop(0)
   if vertex not in path:
    path.append(vertex)
    queue.extend(set(graph[vertex]) - set(path))

  return path

class Population(object):
  """docstring for Population
  Parameters :
    nInd  = number of Individus in population
    N     = number of nodes in Individus (given to constructor of Individu)
    M     = number of edges addes per node in BA method ('' '')
    params = parameters of the ideal network we're trying to converge towards (ga, dm, cc) ('' '')
    echsize = size of selected sample used to produce next generation
    method = method of selection of the sample 'lion', 'roulette' or 'random'
    pMut = probability of a mutation happening
    pCros = probability of a crosing-over happening (in the GenAlg sense of the term)
    logfile = name.path to of the logfile in which progress is written
    nprocess = number of processors to use for multiprocess parts

  """
  def __init__(self, nInd, N, M, params=(1,1,1), echsize=None,  method="random", pMut=0.001, pCros=0.0001, logfile=False, nprocess = 3):
    
    self.nInd = nInd
    self.params = params
    self.echsize = echsize if echsize is not None else nInd/2
    self.method = method
    self.pMut = pMut
    self.pCros = pCros
    self.nprocess = nprocess
    pool = Pool(self.nprocess)
    self.tb = [self]*self.nInd

    self.start_time = time.time()


    self.logfile = logfile
    if self.logfile :
      #clears eventual logfile with same name
      with open(self.logfile, 'w') as o:
        pass

    log = "##========================="+\
          "\n## "+str(datetime.datetime.now())+" : Simulation started."+\
          "\n## Parameters are the following :" +\
          "\n##      nInd = "+str(self.nInd)+"  N = "+str(N)+"  M = "+str(M) +\
          "\n##      g_th = "+str('%.2f'%self.params[0])+"  dmoy = "+str('%.2f'%self.params[1])+ "  cc = "+str('%.2f'%self.params[2])+\
          "\n##      echsize = "+str(self.echsize)+"  method = "+self.method+\
          "\n##      nprocess = "+str(nprocess)
    
    self.wlog(log)

    # Population generation
    # basically [Individu(N, M) for _ in range(self.nInd)] but in multiprocess.
    start_gen = time.time()
    self.pop = []
    # make an iterable array of parameters for every Indiv.
    pms = [(N, M, self.params)]*self.nInd 

    # get the results
    self.pop = pool.map(mk_i, pms)
    init_gen_time = time.time()-start_gen


    log = "\n## \n## "+str(datetime.datetime.now())+" : Generation of population done."+\
          "\n##      Done in "+str('%.2f'%init_gen_time)+"s\n##"
    self.wlog(log)


    # selected individuals to give next gen
    self.ech = None

    #current gen
    self.gen = 0

  def finish(self):
    log = "\n## \n## "+str(datetime.datetime.now())+"\n##     Total Simulation time = "+str('%.2f'%(time.time()-self.start_time))+"s\n" 
    self.wlog(log)

  def wlog(self, log):
    # writes log (to file if given)
    if self.logfile:
      with open(self.logfile, 'a') as o :
        o.write(log)
    else :
      print log+'\n'
     
  def generation(self):
    start_gen = time.time()
    pool = Pool(self.nprocess)

    # get the sample for this generation
    self.selection()


    # make new Indivs from the chosen
    new_gen = pool.map(evolve, self.tb)#[evolve(self) for _ in range(self.nInd)]#
    self.pop = new_gen
    self.gen += 1

    gen_time = time.time()-start_gen

    log = "\n## "+str(datetime.datetime.now())+ " : Evolved to gen "+str(self.gen)+\
          "\n##     Done in "+str('%.2f'%gen_time)+"s"+\
          "\n##     mean fatness = "+str('%.5f'%np.mean([ind.fat for ind in self.pop]))
    self.wlog(log)

    # for ind in self.pop:
    #   print "g"+str(self.gen)+"  ",ind.fat
    
  def selection(self):
  	# selects self.echsize individuals, which probability of selection is based on their fatness
  	if "roulette" == self.method:

  		sum_fat = sum([i.fat for i in self.pop])
  		probas = [i.fat/sum_fat for i in self.pop]
  		selected_ind = []
  		self.ech = []
  		ind = None

  		while len(self.ech)<self.echsize :
  			while ind in selected_ind or ind == None:
  				ind = rd.randint(0, self.nInd-1)
  				
  			if(probas[ind]<rd.random()):
  				self.ech.append(self.pop[ind])
  				selected_ind.append(ind)
  				
  		
  	if "lion" == self.method:
  		#returns the self.echsize individuals with the lowest fatness
  		rank = np.argsort([i.fat for i in self.pop])
  		self.ech = [self.pop[r] for r in rank[0:self.echsize]]

  		
  	if "random" == self.method :
  		#returns self.echsize random individuals
  		self.ech = rd.sample(self.pop, self.echsize)

  def crossing_over(self, A, B):
    # A and B are 2 Individu objects
    n = int((A.N-1)/2)#rd.randint(0, int((A.N-1)/2))
    C = A.copy()

    nodes_A = bfs(A.G, rd.randint(0, A.N-1), n)
    nodes_B = bfs(B.G, rd.randint(0, B.N-1), n)

    new_edges = []
    del_edges = []
    print n, len(nodes_B)
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


