import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

data_de=pd.read_csv('de_wikipedia-de-1000s-sorted.csv', delimiter=" ",header=None)
data_en=pd.read_csv('en_wikipedia-de-1000s-sorted.csv', delimiter=" ",header=None)
data_es=pd.read_csv('es_wikipedia-de-1000s-sorted.csv', delimiter=" ",header=None)
data_ca=pd.read_csv('ca_wikipedia-de-1000s-sorted.csv', delimiter=" ",header=None)

plt.figure(1)
plt.subplot(141)
plt.plot(data_de.iloc[0:,2])
plt.xlabel(".de")
plt.subplot(142)
plt.plot(data_en.iloc[0:,2])
plt.xlabel(".com")
plt.subplot(143)
plt.plot(data_es.iloc[0:,2])
plt.xlabel(".es")
plt.subplot(144)
plt.plot(data_ca.iloc[0:,2])
plt.xlabel(".ca")
plt.show()
