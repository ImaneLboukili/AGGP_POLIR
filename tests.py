#! usr/bin/env python
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt

from Individu import Individu
from Population import Population
#----------------------



plt.style.use('bmh')


def indiv_gentime_test():
  N = 5
  m = 3
  b4 = time.time()
  I = Individu(N, m)
  after = time.time()

  print "Gen time for N="+str(N)+" and m="+str(m)+" : ", after-b4, " s"

  print I.fat
  I.plot_degree_hist()

def copy_indiv_test():
  I = Individu(150, 2500)
  #I.plot_graph()

  J = I.copy()
  I.G.remove_node(2)

  # J.plot_graph()

def basic_mut_test():
  I = Individu(250,3)
  I.plot_graph()

  b4 = time.time()
  for _ in range(100):
    I.basic_mut()
  after = time.time()
  print "Time for 100 mutations : ", after-b4, " s"

  I.plot_graph()

def pop_sampling_test():
  Pop = Population(20, 40, 2)
  print "fatness of initial pop : ",[i.fat for i in Pop.pop]
    
  Pop.selection(3, method="roulette")
  print "fatness of selected individuals : ",[i.fat for i in Pop.ech]


def pop_crossing_over_test():
  Pop = Population(2, 50, 1)

  Pop.pop[0].plot_graph(w_labels=True)
  Pop.pop[1].plot_graph(w_labels=True)
  

  c = Pop.crossing_over(Pop.pop[0], Pop.pop[1])
  c.plot_graph(w_labels=True)

def pop_log_test():
  Pop = Population(20, 40, 2)
  Pop = Population(20, 400, 3, logfile='log.log')

def pop_multiprocess_test():
  Pop = Population(100, 250, 3, nprocess = 1, logfile='log1.log')
  Pop = Population(100, 250, 3, nprocess = 3, logfile='log3.log')

def no_warnings_test():
  Pop = Population(10, 250, 3, nprocess = 1, logfile='logz.log')

def generation_test():
  Pop = Population(50, 150, 2500, params=(1.0,1.7,2.5), echsize=20,  method="roulette", pMut=0.01, pCros=0.5, nprocess = 2, logfile='loggen3.log')
  for i in range(15):
    Pop.generation()

  Pop.finish()
  for ind in Pop.pop:
    print ind.fat

def fit_edges_test():
  
  b4 = time.time()
  I = Individu(150,2500) 
  after = time.time()

  print "Gen time for N="+str(150)+" and m="+str(2500)+" : ", after-b4, " s"

  print I.fat

  # n = len(I.G.edges())

  # print "initial number of edges :"
  # print len(I.G.edges())
  
  # I.fit_edges(n)
  # print " number of e. after fit with a good number of edges :"
  # print len(I.G.edges())

  # I.fit_edges(n+2)
  # print "nb of e. after we say we need two more edges :"
  # print len(I.G.edges())

  # I.fit_edges(n)
  # print "nb of e. after we say we need two edges less :"
  # print len(I.G.edges())



if __name__ == '__main__':
  # indiv_gentime_test()
  # basic_mut_test()
  # copy_indiv_test() 
  # pop_crossing_over_test()
  # pop_log_test()
  # pop_multiprocess_test()
  #no_warnings_test()
  generation_test()
  # fit_edges_test()