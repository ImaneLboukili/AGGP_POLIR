#! usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import time
import powerlaw
import sys
import warnings
import matplotlib.pyplot as plt
import numpy as np
import random as rd
from scipy.optimize import curve_fit

#----------------------

class Individu(object):
  """docstring for Individu"""
  def __init__(self, N, M, param=(1,1,1), copy = False, G = None, fat = None):
    self.N = N
    self.M = M
    self.param = param

    

    if not copy :
      m = int(min([(self.N-0.5)+np.sqrt((self.N-0.5)**2 - 2*self.M),((self.N-0.5)-np.sqrt((self.N-0.5)**2 - 2*self.M))]))
      #print [(self.N-0.5)+np.sqrt((self.N-0.5)**2 - 2*self.M),((self.N-0.5)-np.sqrt((self.N-0.5)**2 - 2*self.M))]
      #int(min([(-1-self.N-np.sqrt((1+self.N)**2-4*self.M))/(-2.0), (-1-self.N+np.sqrt((1+self.N)**2-4*self.M))/(-2.0)]))
      self.G = nx.barabasi_albert_graph(self.N, m)
      
      self.fit_edges(self.M)
      self.fat = self.fatness()
    else :
      self.G = G
      self.fat = fat

  def copy(self):
    return Individu(self.N, self.M, param=self.param, copy=True, G = self.G.copy(), fat = self.fat)

  def fatness(self):
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      self.g_obs = powerlaw.Fit(nx.degree_histogram(self.G), verbose=False).alpha
    self.cc = nx.average_clustering(self.G)
    self.dmoy = nx.average_shortest_path_length(self.G)
    fatness = sum([(1-self.g_obs/self.param[0])**2, (self.dmoy/self.param[1])*2,(self.cc/self.param[2])**2])

    return fatness

  def plot_degree_hist(self):
    dh = nx.degree_histogram(self.G)
    s = sum(dh)
    # To slide powerlaw past the 0 values.
    count=0
    while 0 == dh[count]:
      count+=1

    dhf = [(1.0*dhi)/s for dhi in dh] # get the frequencies

    fit = powerlaw.Fit(dh)
    gam = fit.alpha # get gamma coef

    x = np.array(range(len(dh)))
    pl = [xi**(-1.0*gam) for xi in x]
    plt.bar(x, dhf, color='royalblue')
    plt.plot(x+count, pl, '--', linewidth=3, color='firebrick')
    plt.text(x[len(x)/2], 0.90, "y = x^(-"+str('%.3f'%gam)+')', fontsize=12)
    plt.show()

  def plot_graph(self, w_labels=False):
    #Plot graph
    options = {
        'node_color': 'blue',
        'edge_color': 'black',
        'node_size': 50,
        'width': 2,
        }
    plt.subplot(111)
    nx.draw(self.G, with_labels = w_labels, **options)
    plt.show()

  def basic_mut(self): 	
    re = list(self.G.edges)[rd.randint(0,self.N-1)]
    self.G.remove_edge(re[0], re[1])

    x1 = rd.randint(0,self.N-1) 
    x2 = rd.randint(0,self.N-1) 
    new_edge = (x1,x2)

    while new_edge in self.G.edges:
      x1 = rd.randint(0,self.N-1) 
      x2 = rd.randint(0,self.N-1)
      new_edge = (x1,x2)

    self.G.add_edge(x1, x2)

  def fit_edges(self, n_fit):

    n_G = len(self.G.edges())

    diff = n_fit - n_G

    if (diff > 0) :

      for i in range(diff) :
        x1 = rd.randint(0,self.N) 
        x2 = rd.randint(0,self.N) 
        new_edge = (x1,x2)

        while new_edge in self.G.edges():
          x1 = rd.randint(0,self.N) 
          x2 = rd.randint(0,self.N)
          new_edge = (x1,x2)

        self.G.add_edge(x1, x2)

    if (diff < 0) :

      for i in range(diff) :
        re = list(self.G.edges)[rd.randint(0,n_fit)]
        self.G.remove_edge(re[0], re[1])



