# CHBE444: Design I, University of Maryland
# Prof. Ganesh Sriram, gsriram@umd.edu
# E.02 Urea Reaction Path LP
# SciPy (linprog) Solution

import scipy.optimize as opt

# Documentation for linprog is at:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html

c = [0, -0.5]  # objective function z = cT.x
               # linprog is a minimization algorithm
               # maximizing z is equivalent to minimizing -z

# See notes (on Canvas and Jupyter notebook on GitHub) for how to handle maximization and constants in z

# Inequality constraints A.x <= b

A = [[ 1,     -0.5],
     [-1/3,    0.5],
     [-1,      0]]

b = [0, 1, -1]

res = opt.linprog(
     c,
     A_ub=A,
     b_ub=b,
     A_eq=None,
     b_eq=None,
     bounds=(0,None),
     method='highs'
     )

print(res.x)
print(-res.fun)  # negate the sign since we minimized -z
print(f'The optimum was z = {-res.fun} at x = {res.x}')
print(f'Was the optimization successful? {res.success}')
