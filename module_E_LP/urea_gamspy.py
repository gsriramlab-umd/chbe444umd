# CHBE444: Design I, University of Maryland
# Prof. Ganesh Sriram, gsriram@umd.edu
# E.02 Urea Reaction Path LP
# GAMSPy Solution

import gamspy as gams
import pandas as pd

m = gams.Container()

i = gams.Set(container=m,
             name='i',
             description='compound')

i.setRecords([
    'CH4',
    'CO',
    'CO2',
    'H2',
    'N2',
    'NH3',
    'urea'])  # index i goes over the compounds
              # no need to include H2O since
              # it imposes no constraint on the process

print(i.records)
print()

j = gams.Set(container=m,
            name='j',
            description='reaction')

j.setRecords(['rxn0', 'rxn1', 'rxn2', 'rxn3'])  # index j goes over the reactions
                                                # the reactions have been numbered 0,1,2,3
                                                # to correspond to the weights x0(=1),x1,x2,x3

print(j.records)
print()

yields = gams.Parameter(
    container=m,
    name='yields',
    domain=j,
    description='contribution of reaction weights to the yield'
    )

yields.setRecords([('rxn0', 0), ('rxn1', 0), ('rxn2', 0), ('rxn3', 0.5)])

print(yields.records)
print()

# The throughput constraints are split into two parts:
# those with throughput <= 0 and those with throughputs >= 0
# Methane has a (basis) throughput of exactly -1, so it is included in both sets of constraints

stoich_matrix_lesser = pd.DataFrame(
    [
        ['CH4', 'rxn0', -1],
        ['CO', 'rxn0', 1],
        ['CO', 'rxn1', -1],
        ['CO2', 'rxn1', 1],
        ['CO2', 'rxn3', -0.5],
        ['N2', 'rxn2', -1]
    ], columns=['compound', 'reaction', 'coefficient']
).set_index(['compound', 'reaction'])

stoich_lesser = gams.Parameter(
    container=m,
    name='stoich_lesser',
    domain=[i, j],
    description='stoichiometric coefficient of compound i in reaction j',
    records=stoich_matrix_lesser.reset_index()
    )

print(stoich_lesser.records)
print()

stoich_matrix_greater = pd.DataFrame(
    [
        ['CH4', 'rxn0', -1],
        ['H2', 'rxn0', 3],
        ['H2', 'rxn1', 1],
        ['H2', 'rxn2', -3],
        ['NH3', 'rxn2', 2],
        ['NH3', 'rxn3', -1],
        ['urea', 'rxn3', 0.5]
    ], columns=['compound', 'reaction', 'coefficient']
).set_index(['compound', 'reaction'])

stoich_greater = gams.Parameter(
    container=m,
    name='stoich_greater',
    domain=[i, j],
    description='stoichiometric coefficient of compound i in reaction j',
    records=stoich_matrix_greater.reset_index()
    )

print(stoich_greater.records)
print()

x = gams.Variable(
    container=m,
    name='x',
    domain=j,
    type='Positive',
    description='weight of reaction j in process'
    )

throughput_lesser = gams.Parameter(
    container=m,
    name='throughput_lesser',
    domain=i,
    description='throughput of compound i in process when <= 0'
    )

throughput_lesser.setRecords([('CH4', -1),
                              ('CO', 0),
                              ('CO2', 0),
                              ('N2', 0)])

print(throughput_lesser.records)
print()

throughput_greater = gams.Parameter(
    container=m,
    name='throughput_lesser',
    domain=i,
    description='throughput of compound i in process when >= 0'
    )

throughput_greater.setRecords([('CH4', -1),
                               ('H2', 0),
                               ('NH3', 0),
                               ('urea', 0)])

print(throughput_greater.records)
print()

throughput_lesser_const = gams.Equation(
    container=m,
    name='throughput_lesser_const',
    domain=i,
    description='throughput of compound i when <= 0'
    )

throughput_greater_const = gams.Equation(
    container=m,
    name='throughput_greater_const',
    domain=i,
    description='throughput of compound i when >= 0'
    )

throughput_lesser_const[i] = gams.Sum(j, stoich_lesser[i, j] * x[j]) <= throughput_lesser[i]
throughput_greater_const[i] = gams.Sum(j, stoich_greater[i, j] * x[j]) >= throughput_greater[i]

obj = gams.Sum(j, yields[j] * x[j])

problem = gams.Model(
    container=m,
    name='urea',
    equations=m.getEquations(),
    problem='LP',
    sense=gams.Sense.MAX,
    objective=obj
    )

problem.solve(
    output=None,
    options=gams.Options(
    equation_listing_limit=10,
    variable_listing_limit=10)
    )

print(problem.getEquationListing())
print()
print('Optimal values of x:')
print(x.records)
print()
print('Optimal value of z:')
print(problem.objective_value)
