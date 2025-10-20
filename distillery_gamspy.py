# CHBE444: Design I, University of Maryland
# Prof. Ganesh Sriram, gsriram@umd.edu
# E.03 Distillery Allocation LP
# GAMSPy Solution


import gamspy as gams
import numpy as np
import pandas as pd
import sys


# For this LP: 
# z = 5 x1 + 10 x2 (x1 = weekly production of ale in gal/wk, x2 = weekly production of bourbon in gal/wk)
#                   z is in dollars/wk
# Constraints:
# 0.05 x1 + 0.10 x2 <= 150
# 0.10 x1 + 0.05 x2 <= 150
# 0.05 x1 + 0.15 x2 <= 150
#           0.20 x2 <= 150


m = gams.Container()

i = gams.Set(container=m,
             name='i',
             description='reactor')

i.setRecords(['F1','F2','F3','S4'])  # F1: fermenter 1, ..., S4: still 4 

j = gams.Set(container=m,
            name='j',
            description='drink')

j.setRecords(['A','B'])  # A: ale, B: bourbon

print(i.records)
print(j.records)
print()

cap = gams.Parameter(container=m,
                     name='cap',
                     domain=i,
                     description='weekly production capacity of reactor i in h/wk'
                    )

cap.setRecords([('F1',150),('F2',150),('F3',150),('S4',150)])

pft = gams.Parameter(container=m,
                     name='pft',
                     domain=j,
                     description='profit of drink j in dollars per 100 gal'
                    )

pft.setRecords([('A',500),('B',1000)])  # profit is per 100 gal, so prices in problem were multiplied by 100

print(cap.records)
print()
print(pft.records)
print()

hrs_matrix = pd.DataFrame(
    [
        ['F1','A',5],
        ['F1','B',10],
        ['F2','A',10],
        ['F2','B',5],
        ['F3','A',5],
        ['F3','B',15],
        ['S4','A',0],
        ['S4','B',20]
    ],columns=['reactor','drink','hours']
).set_index(['reactor','drink'])

hrs = gams.Parameter(container=m,
                     name='hrs',
                     domain=[i,j],
                     description='number of hours spent in each reactor by 100 gal of drink',
                     records=hrs_matrix.reset_index()
                    )

print(hrs.records)

x = gams.Variable(container=m,
                  name='x',
                  domain=j,
                  type='Positive',
                  description='weekly production of drink j'
                 )

cap_const = gams.Equation(container=m,
                          name='cap_const',
                          domain=i,
                          description='capacity of reactor i'
                         )

cap_const[i] = gams.Sum(j,hrs[i,j]*x[j]) <= cap[i]  # constraints

obj = gams.Sum(j,pft[j]*x[j])  # objective


problem = gams.Model(container=m,
                     name='distillery',
                     equations=[cap_const],
                     problem='LP',
                     sense=gams.Sense.MAX,
                     objective=obj
                    )

problem.solve(output=None,
              options=gams.Options(equation_listing_limit=10,variable_listing_limit=10)
             )

print(problem.getEquationListing())
print()
print('Optimal values of x:')
print(x.records)
print()
print('Optimal value of z:')
print(problem.objective_value)