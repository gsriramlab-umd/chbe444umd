# CHBE444: Design I, University of Maryland
# Prof. Ganesh Sriram, gsriram@umd.edu
# E.06 NLP: Sum of Squared Residuals Function
# SciPy/Solution with Nelder-Mead Method

import numpy as np
import scipy as sci
import matplotlib.pyplot as plt


def ssr(x, C_exp):
    # SSR function

    x1 = x[0]
    x2 = x[1]
    sig = 1

    C = np.zeros(4)
    C1 = 1 - 2 * x1 / (2 - x1) * (1 - x1 * x2)/(1 + 2 * x1 * x2)
    C2 = 1 / (1 + 2 * x1 * x2)
    C3 = (
        (
            1 - 2 * x1 / (2 - x1) * (1 - x1 * x2) / (1 + 2 * x1 * x2) +
            1 / (1 + 2 * x1 * x2)) *
        (x1 * x2)/(1 + x1 * x2))
    C4 = (
        (
            1 - 2 * x1 / (2 - x1) * (1 - x1 * x2)/(1 + 2 * x1 * x2) +
            1 / (1 + 2 * x1 * x2)
        ) *
        (x1 * x2)/(1 + x1 * x2) + 1/(1 + 2 * x1 * x2))

    C = [C1, C2, C3, C4]

    ssr = 0
    for i in range(0, 4):
        ssr += (C[i] - C_exp[i])**2 / sig**2

    return ssr

# Minimization with Nelder-Mead (Amoeba) Algorithm

C_exp = [0.84, 0.80, 0.16, 0.88]

# Documentation for scipy.optimize.minimize is at:
# https://docs.scipy.org/doc/scipy/tutorial/optimize.html#nelder-mead-simplex-algorithm-method-nelder-mead

res = sci.optimize.minimize(
    ssr,
    [0, 1],
    args=(C_exp),
    method='nelder-mead',
    options={'xatol': 1e-8, 'disp': True}
    )

print('Optimal x:', res.x)
print('Optimal z:', res.fun)

# Matplotlib Plot of Function Contours

x1 = np.linspace(0, 0.5, 101)
x2 = np.linspace(0, 1, 201)
X1, X2 = np.meshgrid(x1, x2)

S = np.zeros_like(X1)
for i in range(0, np.size(S, 0)):
    for j in range(0, np.size(S, 1)):
        S[i, j] = ssr([X1[i, j], X2[i, j]], C_exp)

p = plt.contourf(X1, X2, S, levels=25, cmap='YlOrRd')
plt.xlabel('x1')
plt.ylabel('x2')
plt.colorbar()
plt.show()
