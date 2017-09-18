import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv('server.csv', header=None)


plt.figure(1)
plt.subplot(411)
plt.plot(df.iloc[0:2000,2])
n=len(df.iloc[0:2000,2])
rmse = np.linalg.norm(df.iloc[0:2000,2] - 85) / np.sqrt(n)

print("Mean: ",np.mean(df.iloc[11:1648,2]))
print("Median:  ",np.median(df.iloc[11:1648,2]))
print("STD: ",np.std(df.iloc[11:1648,2]))

plt.xlabel("Iteration")
plt.ylabel("Memory Usage %")
plt.subplot(412)
plt.plot(df.iloc[0:2000,-1])

print("Server 1: ",len(df.iloc[0:2000,-1][df.iloc[0:2000,-1]==1].dropna(axis=0)))
tmp=1
list_values=[]
num=0
flag=0
for value in df.iloc[0:2000,-1]:

	if tmp==2 and value==1:
		flag=1
		num=0
	elif tmp==1 and value==2 and flag==1:
		list_values.append(num)
		num=0
		flag=0
	elif tmp==1 and value==1:
		num+=1

	tmp=value

print("Fluctuaciones:", list_values)
print("Mean fluctuations: ",np.mean(list_values))
print("Median fluctuations: ",np.median(list_values))

plt.xlabel("Iteration")
plt.ylabel("Servers")
plt.subplot(413)
plt.plot(df.iloc[0:2000,-2])
plt.xlabel("Iteration")
plt.ylabel("RAM State")
plt.subplot(414)
plt.plot(df.iloc[0:2000,5],'orange')
plt.xlabel("Iteration")
plt.ylabel("Connections")

dff = pd.read_csv('fuzzyevolution.csv', header=None)
y=range(len(dff.iloc[:,1]))
x=range(len(dff.iloc[1,:]))
print(x)
print(y)
dff=np.array(dff.iloc[:,:])
hf = plt.figure()
ha = hf.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x, y) 
ha.plot_surface(X, Y, dff, edgecolors='r')
ha.set_xlabel('Parameter Membership Function a, b and c')
ha.set_ylabel('Iteration')
ha.set_zlabel('RAM')
plt.show()