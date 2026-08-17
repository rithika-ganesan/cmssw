import numpy as np
import matplotlib.pyplot as plt

path='iterationsIR.txt'
its = np.loadtxt(path)

print(its.shape)

fig, ax = plt.subplots()
ax.hist(its, bins=20)
fig.dpi=200
plt.savefig('iterationsIR.pdf')
