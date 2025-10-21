# CHBE444: Design I, University of Maryland
# Prof. Ganesh Sriram, gsriram@umd.edu
# E.02 Urea Reaction Path LP
# SymPy Throughput Analysis


# Intro to SymPy

import sympy as sym

x,y = sym.symbols('x y')

y = (x-4)**3

print(y)

print(sym.expand(y))


# Throughput analysis for urea EP

import sympy as sym

S,x1,x2,x3,x = sym.symbols('S x1 x2 x3 x')

S = sym.Matrix([[-1,  0,  0,  0],    # CH4
                [ 1, -1,  0,  0],    # CO
                [ 0,  1,  0, -0.5],  # CO2
                [-1, -1,  0,  0.5],  # H2O
                [ 3,  1, -3,  0],    # H2
                [ 0,  0, -1,  0],    # N2
                [ 0,  0,  2, -1],    # NH3
                [ 0,  0,  0,  0.5]]) # urea

x = sym.Matrix([[1],
                [x1],
                [x2],
                [x3]])

# Different ways of printing the matrix product

print(S*x)

sym.init_printing()
sym.pprint(S*x)

S*x
