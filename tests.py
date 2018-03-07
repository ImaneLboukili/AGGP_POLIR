#! usr/bin/env python
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt

from Individu import Individu
#----------------------



plt.style.use('bmh')

# Testing individus

I = Individu(1000, 2)
print I.fat
I.plot_degree_hist()

