# CHBE444: Design I, University of Maryland
# Prof. Ganesh Sriram, gsriram@umd.edu
# E.02 Urea Reaction Path LP
# CHBE444UMD/Simplex Tableaux Examples


# c = [0,-1/2]  # urea reaction path LP without CO constraint
# A = [[1,-1/2],[-1/3,1/2]]
# b = [0,1]
# var_names = ['x1','x3']
# slack_names = ['x4','x5']


c = [0,-1/2]  # urea reaction path LP with CO constraint
A = [[1,-1/2],[-1/3,1/2],[-1,0]]
b = [0,1,-1]
var_names = ['x1','x3']
slack_names = ['x4','x5','x6']


import chbe444umd as des

Tlist = des.simplex_tableaux(c,A_ub=A,b_ub=b,var_names=var_names,slack_names=slack_names,
	                         tol=1e-6,dec=3,colormap='YlGn')

# var_names and slack_names are optional; the function creates variables if they are not specified
