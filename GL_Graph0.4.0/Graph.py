'''
This program realize a general description of graph.
    Developed by Yu Zhang, Yueran Yang, Sijia Chen and Danyang Chen.

Developing details:
    2019.10.17  Version 0.0  By Sijia
    2019.10.24  Version 0.1  By Danyang
    2019.10.24  Version 0.2  By Sijia
Copyright reserved 2019
'''


#包含节点类和图类

import numpy as np 
import random as rd
#定义运算

#定义并
def Add(A, B):
    C = A
    for b in B:
        if b not in A:
            C.append(b)
    return C
#定义交
def Intersection(A,B):
    C = []
    for b in A:
        if b in B:
            C.append(b)
    return C

#定义集合的减法
def Sub(A, B):
    C = []
    for b in A:
        if b not in B:
            C.append(b)
    return C

# Node类
class Node:
    stc_count = 0
    def __init__(self, ID=None):
        Node.stc_count += 1 
        if ID == None: 
            ID = "Node_"+str(self.stc_count)
        self.ID = ID
        self.son = [] 
        self.father = [] 
        # print("Creating a node with name " + ID)
        self.dual = []

    # 加父子关系
    def addSon(self, son):
        if son not in self.son:
            self.son.append(son)
    def addFather(self, father):
        if father not in self.father:
            self.father.append(father)

    # print函数方便检验
    def __str__(self):
        return 'Node     ' + str(self.ID) + '  |  fathers: ' + str([x.ID for x in self.father]) + ' sons: ' +  str([x.ID for x in self.son]) 

    # 其实不需要，因为son，father，ID都是公有的，外界可以直接访问
    def getSons(self): 
        return self.son
    def getFathers(self):
        return self.father
    def getID(self):
        return self.ID

# MatrixNode类
class MatrixNode(Node):
    def __init__(self, ID=None):
        super().__init__(ID)
        self.data = None

    #返回自己的对偶，固定只有一个dual
    def Dual(self):
        if (self.dual == []):
            dual = MatrixNode(self.ID + '_dual')
            self.dual.append(dual)
            dual.dual.append(self)
        else:
            dual = self.dual[0]
        return dual

    # 定义<=号，根据代数关系，只能比较 Const<= Term
    def __le__(self,other):  
        judge = False
        if (isinstance(self, Constant)) and (isinstance(other, Term)):
            if(self.data != None):
                if other.data[self.data[0]] == self.data[1]:
                    judge = True

        return judge

    #定义>号
    def __gt__(self,other): 
        if (isinstance(self.data, np.matrix)) and (isinstance(other.data, np.matrix)) and not((self.data == other.data).all()) and (other <= self):
            justify = True
        else :
            justify = False
        return justify

# 继承
class Term(MatrixNode): 
    def __init__(self, data, attribute, ID=None): 
        super(Term, self).__init__(ID) # super方法让子类可以直接访问基类的成员，例如下面的self.father
        self.attribute = attribute
        if isinstance(data, np.ndarray):
            self.data = np.mat(data)
        else:
            print("Please input a ndarray for data of", self.ID)

    def __str__(self):
        return 'Term     ' + str(self.ID) + '  |  fathers: ' + str([x.ID for x in self.father]) + ' sons: ' +  str([x.ID for x in self.son]) 

    # 返回自己的对偶
    def Dual(self):
        if (self.dual == []):
            dual = Constant(None, None, self.ID + '_dual')
            self.dual.append(dual)
            dual.dual.append(self)
        else:
            dual = self.dual[0]
        return dual
        
class Constant(MatrixNode): # position is a tuple and value is an integer
    def __init__(self, position, value, ID=None): 
        super(Constant, self).__init__(ID)
        if isinstance(position, tuple):
            self.data = [position, value]
        else:
            if(position != None):
                print("Please input a <tuple> for position of ", self.ID)

    def __str__(self):
        return 'Constant ' + str(self.ID) + '  |  fathers: ' + str([x.ID for x in self.father]) + ' sons: ' +  str([x.ID for x in self.son]) 

    # 返回自己的对偶
    def Dual(self):
        if (self.dual == []):
            dual = Constant(None, None, self.ID + '_dual')
            self.dual.append(dual)
            dual.dual.append(self)
        else:
            dual = self.dual[0]
        return dual

class Atom(MatrixNode): 
    def __init__(self, ID=None): 
        super(Atom, self).__init__(ID)
        # atoms may not need data

    def __str__(self):
        return 'Atom     ' + str(self.ID) + '  |  fathers: ' + str([x.ID for x in self.father]) + ' sons: ' +  str([x.ID for x in self.son]) 

    def Dual(self):
        if (self.dual == []):
            dual = DualOfAtom(self.ID + '_dual')
            self.dual.append(dual)
            dual.dual.append(self)
        else:
            dual = self.dual[0]
        return dual

class DualOfAtom(MatrixNode): 
    def __init__(self, ID=None): 
        super(DualOfAtom, self).__init__(ID)

    def __str__(self):
        return 'DualAtom ' + str(self.ID) + '  |  fathers: ' + str([x.ID for x in self.father]) + ' sons: ' +  str([x.ID for x in self.son]) 

    def Dual(self):
        return self.dual[0]
'''
    def dual(self):
        # 返回自己的对偶, 注意重命名的方法，以后通过这个重命名来找到dual，是DualOfAtom类的实例
        a = Atom(self.ID + '_dual')
        return a
'''

# Graph
class Graph:
    def __init__(self):
        self.nodeList = {} # 储存节点，key是节点名，value是节点地址
        self.nodeNum = 0 

    def addNode(self, node):
        if node.ID in self.nodeList.keys(): # 如果重复添加、重名，均报错
            print("Fail to add the node<" + str(node.ID) + ">. There have been a node in the graph.")
            return self
        self.nodeNum += 1
        self.nodeList[node.ID] = node # 在字典里加一对 key：value       
        return self

    # 通过ID找到node的地址
    def getNodesByID(self, ID):
        if ID in self.nodeList.keys():
            return self.nodeList[ID] 
        else:
            return None

    def addEdge(self, father, son): 
        if father not in self.nodeList.values(): 
            print("No such a father node<" + str(father.ID) + "> in the garph!")
            return
        if son not in self.nodeList.values():
            print("No such a son node<" + str(son.ID) + "> in the garph!")
            return
        father.addSon(son)
        son.addFather(father)

    def addEdgeByID(self, fatherID, sonID): 
        if fatherID not in self.nodeList.keys(): 
            print("No such a father node<" + str(fatherID) + "> in the garph!")
            return
        if sonID not in self.nodeList.keys():
            print("No such a son node<" + str(sonID) + "> in the garph!")
            return
        father = self.nodeList[fatherID]
        son = self.nodeList[sonID]
        father.addSon(son)
        son.addFather(father)

    def removeNode(self, node):
        if node not in self.nodeList.values():
            print("No such a node<" + str(node.ID) + "> needed to be removed!")
            return
        for x_father in node.father: # 移除与他有关的所有关系
            x_father.son.remove(node) 
        for x_son in node.son:
            x_son.father.remove(node)
        del self.nodeList[node.ID]
        self.nodeNum -= 1 

    def removeNodeByID(self, ID):
        if ID not in self.nodeList.keys():
            print("No such a node<" + str(ID) + "> needed to be removed!")
            return
        self.removeNode(self.nodeList[ID])

    def getAllNodeID(self):
        return self.nodeList.keys()

    def __iter__(self):
        return iter(self.nodeList.values())

    #为定义GL做铺垫
    def getAllSon(self, node): 
        #print("in GetAllSon")
        AllSon = []
        AllSon.extend(node.son)
        if AllSon == []:
            return []

        for son in AllSon:
            Add(AllSon, self.getAllSon(son))
        
        return AllSon
    
    #定义GL函数
    def getAllSons(self, node):
        AllSons = self.getAllSon(node)
        AllSons.append(node)
        return AllSons
    
    #定义GU函数
    def getAllFathers(self,node):
        AllFathers = node.father
        if AllFathers == []:
            return []

        for father in AllFathers:
            Add(AllFathers, self.getAllFathers(father))
        return AllFathers
    
    #定义GLa,GLc函数
    def getSonsByType(self, node, type):
        getSonsByType = []
        sons = self.getAllSons(node)
        # print(sons)
        for son in sons:
            if isinstance(son,type):
                getSonsByType.append(son)
        return getSonsByType

    #画对偶图
    def Dual(self):
        self.dualgraph = Graph()
        
        for node in self.nodeList.values():
            dual = node.Dual()
            self.dualgraph.addNode(dual)
            
            for son in node.son:
                #print(son.Dual())
                dual.addFather(son.Dual())
            
            for father in node.father:
                dual.addSon(father.Dual())
        # print(self.dualgraph.getAllNodeID())
        return self.dualgraph
    
    #通过对偶节点的ID名获取原节点
    def GetNodebyDual(self, node):
        for a in self.nodeList.values():
            if (a.Dual() == node):
                break
        return a

