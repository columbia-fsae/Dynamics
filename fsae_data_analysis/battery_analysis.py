#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helpers.graph import *
from helpers.data import *
import sys

# total arguments
n = len(sys.argv)
if n > 2:
    print("Too many arguments, this script takes 1 filepath.")

df = process_battery_data(sys.argv[1])
graph_battery_temps(df)
graph_battery_volts(df)

plt.show()