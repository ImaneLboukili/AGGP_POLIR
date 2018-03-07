#! usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import time
import powerlaw
import matplotlib.pyplot as plt

#----------------------


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
    plt.hist(dh, bins=range(len(dh)), color='royalblue')
    plt.show()



