import numpy as np
import pandas as pd
import graphviz as gz

gra = graphviz.Digraph(comment='Galvanize Customer Journey')

gra.node('N', 'Nor lead nor direct')
gra.node('L', 'Current Leads')
gra.node('D', 'Direct Applicants')
gra.node('A', 'In applications')
gra.node('S', 'Take home sent')
gra.node('R', 'Take home returned')
gra.node('E', 'Enrolled')
gra.node('C', 'Closed')

gra.edges(['NL','ND','NN','LL','LA','DD','DA','AA','AS','SS','RE','SC','EE','CC','LC','SR','RC','RR'])
