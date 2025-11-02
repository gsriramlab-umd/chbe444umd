# CHBE444: Design I, University of Maryland
# Prof. Ganesh Sriram, gsriram@umd.edu
# E.03 Distillery Allocation LPP
# Desmos Plot

import chbe444umd as des
from IPython.display import IFrame

expressions = [{'latex': '0.05x + 0.10y <= 150', 'fillOpacity': 0.1, 'color': '#ff00ff', 'id': 'const1'},
               {'latex': '0.10x + 0.05y <= 150', 'fillOpacity': 0.1, 'color': '#ff00ff'},
               {'latex': '0.05x + 0.15y <= 150', 'fillOpacity': 0.1, 'color': '#ff00ff'},
               {'latex': '0.20y <= 150',         'fillOpacity': 0.1, 'color': '#ff00ff'},
               {'latex': '5x + 10y = z',         'fillOpacity': 0.1, 'color': '#000000'}]

sliders = [{'variable': 'z', 'min': '0', 'max': '15000', 'step': '1000'}]

points = [{'latex': '(1200,600)', 'label': 'optimum', 'showLabel': True}]

# While calling the function, indicate blank expressions, sliders or points as empty arrays, e.g., sliders=[]

graph_html = des.desmos_graph(
    expressions=expressions,
    sliders=sliders,
    points=points,
    axlim=[-100, 2000, -100, 2000],
    size=[1000, 400])

# The following lines enable the graph to be permanently saved in the Jupyter notebook
# This is done by writing an html file (in this case, 'distillery_graph.html) to the folder

with open('distillery_graph.html', 'w', encoding='utf-8') as f:
    f.write(graph_html.get_value())

IFrame('distillery_graph.html', width='100%', height=400)

# To save the graph in the online Desmos graphing calculator (https://www.desmos.com/calculator),
# Use the following version of the command (note the javascript=True option at the end):

graph_html, expr_java = des.desmos_graph(
    expressions=expressions,
    sliders=sliders,
    points=points,
    axlim=[-100, 2000, -100, 2000],
    size=[1000, 400],
    javascript=True)

# Print the list of expressions (expr_java) returned by the function:

print(expr_java)

# Open the Desmos graphing calculator (https://www.desmos.com/calculator)
# Open the Desmos console by pressing Ctrl+Shft+J (Windows) or Cmd+Shft+J (Mac)
# Paste the list of expressions into the console and press Enter
# Some browsers or computers may ask you to explicitly type 'allow paste' before
# you paste expressions into the console
