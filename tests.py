#! usr/bin/env python
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt

from Individu import Individu
#----------------------



plt.style.use('bmh')

# Testing individus
b4 = time.time()
I = Individu(4077, 10)
after = time.time()

print "Gen time : ", after-b4, " s"

p = raw_input("<press enter to continue>")

print I.fat
I.plot_degree_hist()

