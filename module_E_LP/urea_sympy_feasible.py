# CHBE444: Design I, University of Maryland
# Prof. Ganesh Sriram, gsriram@umd.edu
# E.02 Urea Reaction Path LP
# SymPy Feasible Space Plot

import sympy as sym

x1, x3 = sym.symbols('x1 x3')

# Plot feasible space and mark points

p = sym.plot_implicit(sym.And(x1     - x3 / 2 <=  0,
                             -x1 / 3 + x3 / 2 <=  1,
                             -x1              <= -1,
                              x1              >=  0,
                                       x3     >=  0),
                              markers=[{"args": [[1.5], [3], "ko"], "markersize": 4}],
                              annotations=[{'xy': (1.5, 3), 'text': "$z_{opt}=1.5$"}],
                              show=False)


# Plot constraint lines

p1 = sym.plot_implicit(sym.Eq(x1 - x3 / 2, 0), line_color='blue', show=False)
p2 = sym.plot_implicit(sym.Eq(-x1 / 3 + x3 / 2, 1), line_color='red', show=False)
p3 = sym.plot_implicit(sym.Eq(-x1, -1), line_color='green', show=False)
p4 = sym.plot_implicit(sym.Eq(x1, 0), line_color='black',  show=False)
p5 = sym.plot_implicit(sym.Eq(x3, 0), line_color='magenta', show=False)

p.append(p1[0])
p.append(p2[0])
p.append(p3[0])
p.append(p4[0])
p.append(p5[0])

p.show()
