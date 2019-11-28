from Graph import *

import numpy as np
import ML_graph as mg

Graph = mg.ML_Graph()
T1 = mg.Term(np.array([[0, 1], [0, 1]]), True, 'T1+')
T2 = mg.Term(np.array([[1, 0], [1, 0]]), True, 'T2+')
T3 = mg.Term(np.array([[0, 1], [1, 0]]), False, 'T1-')
T4 = mg.Term(np.array([[1, 0], [1, 1]]), False, 'T2-')
T5 = mg.Term(np.array([[1, 1], [1, 0]]), False, 'T3-')
'''
T6 = mg.Term(np.array([[0, 0], [1, 0]]), True, 'T4+')
T7 = mg.Term(np.array([[0, 0], [0, 1]]), True, 'T5+')
T8 = mg.Term(np.array([[1, 0], [0, 0]]), True, 'T6+')
T9 = mg.Term(np.array([[0, 0], [0, 0]]), True, 'T7+')
T10 = mg.Term(np.array([[1, 1], [1, 1]]), False, 'T4-')
T11 = mg.Term(np.array([[0, 1], [0, 0]]), True, 'T3+')
T12 = mg.Term(np.array([[0, 1], [1, 1]]), False, 'T5-')
T13 = mg.Term(np.array([[1, 1], [0, 1]]), False, 'T6-')
T14 = mg.Term(np.array([[1, 0], [0, 1]]), False, 'T7-')
T15 = mg.Term(np.array([[0, 0], [1, 1]]), False, 'T8-')
T16 = mg.Term(np.array([[1, 1], [0, 0]]), False, 'T9-')
'''
Graph.addNode(T1).addNode(T2).addNode(T3).addNode(T4).addNode(T5)#.addNode(T6).addNode(T7).addNode(T8).addNode(T9).addNode(T10).addNode(T11).addNode(T12).addNode(T13).addNode(T14).addNode(T15).addNode(T16)
Graph.initialize()

C = Graph.ConstantList
A = Graph.AtomList
T = Graph.TermList

print(Graph.getAllNodeID())
print(Graph.dualgraph.getAllNodeID())
print(Graph.dualgraph.getNodesByID('T1+_dual'))
print([x.ID for x in Graph.Tr(T1)])
'''
Graph.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)
Graph.paint2(figsize=(18,10),node_size=5000,width=2,pic_size=0.07)
'''


v = Graph.getNodesByID('v')

Graph.EnforceNegativeTrace()
#Graph.paint()


#to test whether the negative traces match the relations
for i in Graph.NegativeTerm:
    if set(Graph.Tr(i)).issubset(set(Graph.Tr(v))):
        print('The negative traces do not match the relations.')
        break
    else:
        continue
    
Graph.EnforcePositiveTrace()
#Graph.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)
Graph.test()

for term in Graph.TermList:
    Graph = Graph.SparseCrossing(term,v)
Graph.test()

 
    
Graph = Graph.AtomSetReduction()
#Graph.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)

Graph = Graph.AtomSetReductionDual()
Rp = Graph.GenerationOfPinning()
#Graph.paint()
Graph.test()
    
#Graph.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)
#Graph.AtomSetReduction()
#
#Graph.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)

#
#Graph.AtomSetReduction()
#
#Graph.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)

#Graph.EnforceNegativeTrace()