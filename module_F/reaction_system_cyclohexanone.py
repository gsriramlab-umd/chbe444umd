import numpy as np
import sympy as sym
import chbe444umd as des

# This is a gas-phase reactor, so it is best to describe the kinetics in
# terms of molar flows (ṅ in mol/s). The partial pressure expressions that
# appear in the reaction rates can be built from the molar flows. Notice
# that the axes of the rate field plot are the dimensionless flow rates of
# phenol (nP/nP0) and ketone (nK/nP0).

# Define the flow rates of phenol (nP0), hydrogen (nH0), cyclohexanone or
# ketone (nK0) and cyclohexanol or alcohol (nA0) in the reactor feed.
# - Use a convenient unit, e.g., mol/s.
# - This script only needs values (it does not process units), but you need to
#   ensure that units are consistent throughout the calculation.
# - Obtain nP0 from your production capacity of ketone and a material balance.
#   - The reaction will not perfectly convert all phenol to cyclohexanone, so
#   - overestimate nP0.
# - Obtain nH0 by studying the book chapter (Dimian and Bildea, 2008) provided
#   on Canvas.
#   - Having excess hydrogen in the feed is favorable to the production of
#     ketone.
#   - nK0 and nA0 can be set to zero since this is your first attempt at this
#     calculation. However, the feed going into the reactor is a mixed feed
#     consisting of fresh feed and recycle, so nK0 and nA0 will strictly not
#     be zero. As as aside: in my attainable region in the Unit 1 PDF, nK0 and
#     nA0 were set to the values I obtained from my final Aspen reactor.

# With this background, let us choose n['P'] and n['K'] as the axis variables
# for the rate field plot and define the reaction reactions in terms of the
# vector n = [n['P'], n['K']]. You could also try n = [n['K'], n['A']].

# Define nP0, nH0, nK0 and nA0 here
# Define P (bar) and T (K) here
# - Choose P and T them by using guidance from the book chapter (Dimian and
#   Bildea, 2008)
# - It is perfectly OK to choose constant P and T (this will keep the
#   calculations straightforward)

def kinetics(n):  # function to define kinetics in terms of n['P'] and n['K']
    # Define k1, k2, E1, E2 here. Use consistent units.
    # Define the adsorption constants KP1, KH1, etc., here.

    # To get the reaction rates at any point in the reactor, we need four flow
    # rates (nP, nH, nK, nA), but we only have two (n['P'] and n['K']) from the
    # axes variables. Let us do atomic balances (learned in CHBE101) to get the
    # remaining two flow rates.

    nP = n['P']  # nP is internal variable, n['P'] is passed to this function
    nK = n['K']  # nK is internal variable, n['K'] is passed to this function

    # Do a balance on atomic carbon to express nA in terms of nP and nK
    # The balance should look like: carbon atoms in = carbon atoms out
    # This should give you an expression like:

    # nA = some linear function of nP and nK

    # Do a balance on atomic hydrogen to express nH in terms of nP, nK and nA
    # The balance should look like: hydrogen atoms in = hydrogen atoms out
    # This should give you an expression like:

    # nA = some linear function of nP, nK and nA

    # Since we already defined nA, it is OK to express nH in terms of the axis
    # variables and nA

    # Defining a total flow rate (sum of all the four n's) here will be useful
    # to keep expressions compact.

    # Define the partial pressures pP, pH, pK, pA from the molar flow rates
    # and the total pressure P
    # - At the mild pressures recommended for this problem, the gas phase will
    #   be ideal

    # Carefully express the rates of the two reactions r1 and r2 in terms
    # of the partial pressures (pP, pH, pK, pA) and the previously defined
    # constants.

    # Divide the rates by nP0 to de-dimensionalize them.

    # Have the function return a vector of rates, i.e., [r1, r2] or
    # [r1 / nP0, r2 / nP0] depending on how you defined them

system = des.ReactionSystem(
    component_ids=('P', 'H', 'K', 'A'),
    component_names={'P': 'phenol',
                     'H': 'hydrogen',
                     'K': 'ketone', 'A':
                     'alcohol'},
    axes={'P': 0, 'K': 1},
    h_lim=[0, 1],
    v_lim=[0, 1],
    reactions=('r1', 'r2'),
    stoich= {},  # enter stoichiometry here
    kinetics={'r1': lambda n: kinetics(n)[0],  # 1st element of vector returned
              'r2': lambda n: kinetics(n)[1]},  # 2nd element
    inequality=lambda n: []
    # inequality should contain two rows that should both be < 0:
    # - one row: an expression for -nA from the function above
    # - other row: an expression for -nH from the function above
    # - We need these constraints because nP and nK are valid only
    #   when they result in nonnegative flow rates nA, nH
    # - Make sure to express the rows solely in terms of n['P'],
    #   n['K'] and constants defined outside the kinetics function
    #   above
)

%config InlineBackend.figure_format='svg'
%matplotlib inline

# Rate Field
fig, ax, _ = system.plot_rate_field(fsize=6, n_vec=41, arrow_scale=41)

# Reactors
# You will need a huge tau, since "tau" for a catalytic reactor is:
# tau = mass of catalyst up to that point in the reactor / nP0
# Verify this definition is consistent with the kinetic expressions
pfr = des.Reactor(name='PFR', flow_type='plug', feed=[1, 0])
pfr.simulate(system=system, ax=ax, n_points=2000, time_limit=1e+6)
cstr = des.Reactor(name='CSTR', flow_type='mixed', feed=[1, 0])
cstr.simulate(system=system, ax=ax, time_limit=1e+9)

# Points
pfr.plot_point(ax, x=0.4, annotation='xy')
pfr.plot_point(ax, tau=100000, annotation='tau')
cstr.plot_point(ax, tau=100000, annotation='tau')
ax, point, text = cstr.plot_point(ax, y=0.2, annotate='all')

# AR
des.convexify(ax, boundaries=[pfr, cstr],
              lw=0, color='#80ff00', alpha=0.1)

# Draw the rate field boundaries
# These boundaries are inequality lines (contours) for nA = 0 and nH = 0
f = lambda n:  # LHS of f(n['P'], n['K'] constants) reflecting that nA = 0
g = lambda n:  # LHS of g(n['P'], n['K'] constants) reflecting that nH = 0

X = np.linspace(0, 1, 11)  # calculate contours at 0, 0.1, ..., 1 on each axis

# Make 2 matrices xx and yy, each having X along both dimensions
xx, yy = np.meshgrid(X, X)

ff = np.zeros_like(xx)  # initialize to zero, same shape as xx
gg = np.zeros_like(xx)  # initialize to zero, same shape as xx

# This double for loop is a tad inefficient and can be made efficient
# by vectorizing or 'broadcasting', but it is used here as its logic
# is very easy to understand
for i in range(len(X)):
    for j in range(len(X)):
        n = {'P': xx[i, j], 'K': yy[i, j]}  # define n = [n['P'], n['K']]
        ff[i, j] = f(n)  # pass to function that computes nA or nH constraint
        gg[i, j] = g(n)  # pass to function that computes nA or nH constraint

# Plot contours
ax.contour(xx, yy, ff, 'k-', levels=[0])
ax.contour(xx, yy, gg, 'k-', levels=[0])

# Draw contours of the objective function representing economic potential
# (EP) adjusted for catalyst cost:

# EP_adjusted = EP - i * catalyst cost

# Note that all terms in this equation have units of $/time
# i is an interest rate (10% is a typical interest rate for such calculations
# i (1/time) * catalyst cost ($) is the cost of investing money in the catalyst
# Subtract this cost from the EP to get the adjusted EP

# Define EP function and draw contours yourself; use an array for levels
