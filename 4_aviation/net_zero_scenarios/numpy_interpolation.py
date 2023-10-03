# %%
import numpy as np
import matplotlib.pyplot as plt

x = [50.0, 150.0, 250.0, 400.0, 600.0, 850.0, 1000.0]
y = [3.2, 10.1, 16.3, 43.7, 69.1, 45.2, 10.8]

mypol = np.polynomial.polynomial.Polynomial.fit(
    x = x,
    y = y,
    deg = 5,
)

newx = np.linspace(x[0], x[-1], 100)
newy = [mypol(xval) for xval in newx]

plt.plot(x, y)
plt.plot(newx, newy)

# %%
import scipy as sp
import scipy.interpolate as interpolate

x = [50.0, 150.0, 250.0, 400.0, 600.0, 850.0, 1000.0]
y = [3.2, 10.1, 16.3, 43.7, 69.1, 45.2, 10.8]

mypol = sp.interpolate.interp1d(
    x = x,
    y = y,
)

newx = np.linspace(x[0], x[-1], 100)
newy = [mypol(xval) for xval in newx]