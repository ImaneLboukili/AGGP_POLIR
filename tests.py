#! usr/bin/env python
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt

from Individu import Individu
from Population import Population
#----------------------



plt.style.use('bmh')

TEST_INDIVIDU = False
TEST_POPULATION = False
TEST_MUTATION = True



if TEST_INDIVIDU :
  # Testing individus
  print "\n\n Tests for Individus"
  
  N = 5
  m = 3
  b4 = time.time()
  I = Individu(N, m)
  after = time.time()

  print "Gen time for N="+str(N)+" and m="+str(m)+" : ", after-b4, " s"

  print I.fat
  I.plot_degree_hist()
  I.plot_graph()
  #I.basic_mut() #Basic mutation : one edge of the graph is removed, an other one is added


if TEST_MUTATION:
  I = Individu(250,3)
  I.plot_graph()

  b4 = time.time()
  for _ in range(100):
    I.basic_mut()
  after = time.time()
  print "Time for 100 mutations : ", after-b4, " s"

  I.plot_graph()


if TEST_POPULATION :

  Pop = Population(20, 40, 2)
  print "fatness of initial pop : ",[i.fat for i in Pop.pop]
    
  Pop.selection(3, method="roulette")
  print "fatness of selected individuals : ",[i.fat for i in Pop.ech]


if not TEST_POPULATION and not TEST_INDIVIDU and not TEST_MUTATION:
  print "\n\nA least put ONE of the test variables to True...\n\n"