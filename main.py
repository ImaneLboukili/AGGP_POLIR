#! usr/bin/env python
# -*- coding: utf-8 -*-

import time
from Individu import Individu
import matplotlib.pyplot as plt
#----------------------



plt.style.use('bmh')


I = Individu(1000, 2)
print I.fat
I.plot_degree_hist()