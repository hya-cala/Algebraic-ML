#创立图时的试验板和ToyModel试验板
import numpy as np 
import random as rd
from Graph import *


G = ML_Graph()
'''
创立图时的试验板
node1 = Node()
t1 = Term(np.random.randint(0, 1, (2,2)), "t1")
c1 = Constant(np.random.randint(0, 1, (2,2)), "c1")
a1 = Atom("a1")

print(a1)
G.addNode(t1).addNode(node1).addNode(c1).addNode(a1)
print(G.getAllNodeID())
G.addEdgeByID("t1", "c1")
print(c1)
G.addEdgeByID("c1", "a1")
print(c1)
G.addEdgeByID("a1", "Node_1")
print(a1)
G.removeNodeByID("Node_1")
print(G.getAllNodeID())
print(t1)
print(a1)


print([x.ID for x in G.getAllSons(t1)])
print([x.ID for x in G.getSonsByType(t1, Atom)])
print(t1)
print(G.getNodesByID('t1').Dual())

print(G.GetNodebyDual('c1_dual'))

print([x.ID for x in G.getAllSons(c1)])

print(G.Dual().getNodesByID('t1_dual'))
'''


#Toy Model
G.ConsituteConstants()
#print(G.getNodesByID('Constant_1,1w').data)
#print(G.getAllNodeID())
T1 = Term(np.matrix([[1, -1], [1, -1]]), 'T1+')
T2 = Term(np.matrix([[-1, 1], [-1, 1]]), 'T2+')
T3 = Term(np.matrix([[1, -1], [-1, 1]]), 'T1-')
T4 = Term(np.matrix([[-1, 1], [-1, -1]]), 'T2-')
T5 = Term(np.matrix([[-1, -1], [-1, 1]]), 'T3-')
G.addNode(T1).addNode(T2).addNode(T3).addNode(T4).addNode(T5)
G.TermClassify()
#print([x.ID for x in G.PositiveTerm])
G.ConstConnTerm()
#print(T4)
#print(G.getNodesByID('Constant_1,1w'))
G.FundemenAtom()
#print(G.getNodesByID('Constant_1,1w'))
G.DualOfML_Graph()
#G.DualOfML_Graph()
#print(G.DualOfML_Graph().getNodesByID('zero_'))
#print(G.DualOfML_Graph().getNodesByID('Constant_1,2w_dual'))
#print(G.DualOfML_Graph().getAllNodeID())
#print([x.ID for x in G.DualOfML_Graph().getAllSons(G.DualOfML_Graph().getNodesByID('v_dual'))])
#print([x.ID for x in G.Tr(T1)]) 
#print(G.compare(T1, T2))
G.EnforceNegativeTrace() #问题
print(G.compare(T1,T2))

