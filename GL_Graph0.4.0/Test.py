import numpy as np
import ML_graph as mg

Graph = mg.ML_Graph()
T1 = mg.Term(np.array([[1, 0], [1, 0]]), True, 'T1+')
T2 = mg.Term(np.array([[0, 1], [0, 1]]), True, 'T2+')
T3 = mg.Term(np.array([[1, 0], [0, 1]]), False, 'T1-')
T4 = mg.Term(np.array([[0, 1], [0, 0]]), False, 'T2-')
T5 = mg.Term(np.array([[0, 0], [0, 1]]), False, 'T3-')
Graph.addNode(T1).addNode(T2).addNode(T3).addNode(T4).addNode(T5)
Graph.initialize()

'''
print(G.getAllNodeID())
print(G.dualgraph.getAllNodeID())
print(G.dualgraph.getNodesByID('T1+_dual'))
print([x.ID for x in G.Tr(T1)])
'''

Graph.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)
Graph.paint2(figsize=(18,10),node_size=5000,width=2,pic_size=0.07)
