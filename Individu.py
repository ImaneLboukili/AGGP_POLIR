#! usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import time
import powerlaw
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#----------------------

def powlaw(x, g):
  return x**(-g)

class Individu(object):
  """docstring for Individu"""
  def __init__(self, N, M, param=(1,1,1)):
    self.N = N
    self.M = M
    self.param = param

    self.G = nx.barabasi_albert_graph(self.N, self.M)

    self.fat = self.fatness()

  def fatness(self):
    g_obs = powerlaw.Fit(nx.degree_histogram(self.G)).alpha
    cc = nx.average_clustering(self.G)
    dmoy = nx.average_shortest_path_length(self.G)
    fatness = sum([(1-g_obs/self.param[0])**2, (dmoy/self.param[1])*2,(cc/self.param[2])**2])

    return  fatness

  def plot_degree_hist(self):
    dh = nx.degree_histogram(self.G)
    s = sum(dh)
    dhf = [(1.0*dhi)/s for dhi in dh] # get the frequencies

    fit = powerlaw.Fit(dh, sigma_threshold=1)
    gam = fit.alpha # get gamma coef

    x = range(len(dh))
    pl = [xi**(-1.0*gam) for xi in x]
    plt.bar(x, dhf, color='royalblue')
    plt.plot(x, pl, '--', linewidth=3, color='firebrick')
    plt.show()

