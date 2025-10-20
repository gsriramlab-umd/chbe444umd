# CHBE444: Design I, University of Maryland
# Prof. Ganesh Sriram, gsriram@umd.edu
# E.06 NLP Example 
# SciPy/SQP Solution


# Desmos Plot

import chbe444umd as des

f = 0.05

expressions = [{'id':'x1def', 'latex':'x_0=x', 'hidden':True},
               {'id':'x2def', 'latex':'x_1=y', 'hidden':True},
               
               {'id':'const1', 'latex':'-x_0 \\\\le 0', 'color':'#ff00ff', 'fillOpacity':f},
               {'id':'const2', 'latex':'-x_1 \\\\le 0', 'color':'#ff00ff', 'fillOpacity':f},
               {'id':'const3', 'latex':'x_0 \\\\le 2', 'color':'#ff00ff', 'fillOpacity':f},
               {'id':'const4', 'latex':'x_1 \\\\le 4', 'color':'#ff00ff', 'fillOpacity':f},
               {'id':'const5', 'latex':'3x_0^2+2x_1 \\\\le 6', 'color':'#ff00ff', 'fillOpacity':f},
               {'id':'const6', 'latex':'-x_0-x_1 \\\\le -2', 'color':'#ff00ff', 'fillOpacity':f},
               
               {'id':'obj', 'latex':'5(x_0-4)^2+10(x_1-2)^2=z', 'color':'#000000', 'fillOpacity':1},]

sliders =[{'variable':'z', 'min':'0', 'max':'100', 'step':'1'}]

graph_html = des.desmos_graph(expressions,sliders,[],axlim=[-1,4,-1,4],size=[1000,650])
with open('sqp_example_graph.html',"w",encoding="utf-8") as f:
    f.write(graph_html.get_value())
 
from IPython.display import IFrame
IFrame('sqp_example_graph.html',width='100%',height=400)


# SciPy/SQP Solution

import numpy as np
import scipy as sci

# def z(x):
#     z = 5*(x[0]-4)**2+10*(x[1]-2)**2
#     return z

z = lambda x: -(5*(x[0]-4)**2+10*(x[1]-2)**2)

z([1,1])  # test function

ineq_cons = {'type': 'ineq',
             'fun' : lambda x: -np.array([-x[0],
                                         -x[1],
                                         x[0]-2,
                                         x[1]-4,
                                         -3*x[0]**2+2*x[1]-6,
                                         -x[0]-x[1]+2])}

x0 = [0,4]

# Documentation for scipy.optimize.minimize with SQP option is at:
# https://docs.scipy.org/doc/scipy/tutorial/optimize.html#sequential-least-squares-programming-slsqp-algorithm-method-slsqp

res = sci.optimize.minimize(z,x0,method='SLSQP',
                            constraints=[ineq_cons],
                            options={'ftol':1e-9,'disp':True})

print(res.x)
print(res.fun)
print(res.success)


