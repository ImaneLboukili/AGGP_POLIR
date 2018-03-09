#! usr/bin/env python
# -*- coding: utf-8 -*-

import networkx
import time

from Individu import Individu
#----------------------

class Population(object):
  """docstring for Population"""
  def __init__(self, nInd, N, M):
    
    self.nInd = nInd
    self.individus = [Individu(N, M) for _ in range(self.nInd)]
    
    