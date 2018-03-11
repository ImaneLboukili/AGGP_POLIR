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
  I = Individu(5, 3)
  I.plot_graph()

  J = I.copy()
  I.G.remove_node(2)

  J.plot_graph()

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
  Pop = Population(2, 9, 2)

  Pop.pop[0].plot_graph(w_labels=True)
  Pop.pop[1].plot_graph(w_labels=True)
  

  c = Pop.crossing_over(Pop.pop[0], Pop.pop[1])
  c.plot_graph(w_labels=True)



if __name__ == '__main__':
  # indiv_gentime_test()
  # basic_mut_test()
  # copy_indiv_test()
  pop_crossing_over_test()

