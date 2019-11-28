'''
This program realize a class to finish 6 tasks of Algebra Machine Learning.
    Developed by Yu Zhang, Yueran Yang, Sijia Chen and Danyang Chen

Developing Details
    2019.10.17  Version 0.0  By Sijia
    2019.10.24  Version 0.1  By Danyang
        Add 4 list to contain Terms, Constants, Atoms...
        Add addNode(), removeNode().
        Still need rewrite other functions.
    2019.10.24   Version 0.2
    
    By Sijia 
        Rewrite the fundamental functions.
        Still need the Alogrithm Functions.
    2019.10.24  Version 0.3 By ZhangYu
        Add painting graph functions
    2019.10.24  Version 0.3 By ZhangYu
        Fix some bugs
        Parameters for painting are available now.
    2019.11.08  Version 0.4 By Yueran
        Change the type of .dual as Node instead of list
        Move Dualgraph generate function here
        Rewrite the Algorithms (Algorithms still needs improving)
        Add function PostitiveRelation, NegativeRelation and AddAtomToDualgraph
        -Remark: edges must be added in master and dual graph separately
        -Some bugs: graphs generated by the algorithms are always different due 
                    to the random choices
    2019.11.08 Version 0.4.1 by Yueran
        Fix some bugs
        Some instruction:
            1. Just change the constant choices in the algorithm2 to enforce that 
            the constant which will be added a atom to is a b-type constant. It 
            seems right for the time being.
            *** this needs proof
    2019.11.24 Version 0.4.2 by ZhangYu
        Fix bugs in getAllFathers
        Remove paint2(), while you can use the parameter 'enable_im' in paint().
        Add paint_dual()
Copyright reserved 2019
'''


#包含代数机器学习图的继承+6个算法（算法需要debug）
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx 
from Graph import *


class ML_Graph(Graph):
    def __init__(self):
        super().__init__()
        self.TermList = []
        self.PositiveTerm = []
        self.NegativeTerm = []
        self.ConstantList = []
        self.AtomList = []
        self.DualOfAtomList = []
        self.dualgraph = Graph()

        
###      
    def Dual(self):
        self.dualgraph = ML_Graph()
        for node in self.nodeList.values():
            dual = node.Dual()
            self.dualgraph.addNode(dual)
            
            for son in node.son:
                dual.addFather(son.Dual())
            for father in node.father:
                dual.addSon(father.Dual())
        return self.dualgraph
    
    def AddAtomsToDualgraph(self):
        for term in self.NegativeTerm:
            zeta = Atom(ID = 'Atom_to_[%s]'%term.ID)
            self.dualgraph.addNode(zeta)
            self.dualgraph.addEdge(term.dual,zeta)
            #print(term.ID,zeta.ID)
    
    def GetNodebyDual(self, node):
        for a in self.nodeList.values():
            if (a.Dual() == node):
                break
        return a
###        

    def addNode(self, node):
        super().addNode(node)
            # if node.ID in self.nodeList.keys(): # 如果重复添加、重名，均报错
            #     print("Fail to add the node<" + str(node.ID) + ">. There have been a node in the graph.")
            #     return self
            # self.nodeNum += 1
            # self.nodeList[node.ID] = node # 在字典里加一对 key：value       
        if isinstance(node, Term):
            if node.attribute:
                self.PositiveTerm.append(node)
                self.TermList.append(node)
            else:
                self.NegativeTerm.append(node)
                self.TermList.append(node)
            self.dualgraph.addNode(node.Dual())
        elif isinstance(node, Constant):
            self.ConstantList.append(node)
            self.dualgraph.addNode(node.Dual())
        elif isinstance(node, Atom):
            self.AtomList.append(node)
            self.dualgraph.addNode(node.Dual())
        elif isinstance(node, DualOfAtom):
            self.DualOfAtomList.append(node)
        return self 

    def removeNode(self, node):
        super().removeNode(node)
            # if node not in self.nodeList.values():
            #     print("No such a node<" + str(node.ID) + "> needed to be removed!")
            #     return
            # for x_father in ode.father: # 移除与他有关的所有关系
            #     x_father.son.remove(node) 
            # for x_son in del_node.son:
            #     x_son.father.remove(node)
            # del self.nodeList[node.ID]
            # self.nodeNum -= 1
        if isinstance(node, Term):
            if node.attribute:
                self.PositiveTerm.remove(node)
                self.TermList.remove(node)
            else:
                self.NegativeTerm.remove(node)
                self.TermList.remove(node)
        elif isinstance(node, Constant):
            if node not in self.ConstantList:
                return self
            self.ConstantList.remove(node)
        elif isinstance(node, Atom):
            if node not in self.AtomList:
                return self
            self.AtomList.remove(node)
        elif isinstance(node, DualOfAtom):
            if node not in self.DualOfAtomList:
                return self
            self.DualOfAtomList.remove(node)
        return self 

    def paint(self,enable_im = True,
              figsize=(18,10),
              node_size=5000,
              width=2,
              font_size=12,
              pic_size=0.07,
              cmap=plt.cm.tab20):
        nodes_num = [len(self.AtomList),len(self.ConstantList),len(self.TermList)]
        all_nodes= self.AtomList + self.ConstantList + self.TermList
        
        G = nx.Graph()
        h_spacing = 0.8/float(max(nodes_num))
        v_spacing = 0.8/float(len(nodes_num) - 1)
        node_count = 0
        
        #pos of points
        for i, v in enumerate(nodes_num):
            for j in range(v):
                G.add_node(all_nodes[node_count], pos=(0.1+0.5*(j+1)/(v+1), 0.1 + i*v_spacing))
                node_count += 1
                
        #links of points
        for i in all_nodes:
            for j in i.father:
                G.add_edge(i, j)

        pos=nx.get_node_attributes(G,'pos')
        fig = plt.figure(figsize=figsize)
        
        
        nx.draw(G, pos, 
                node_color=range(node_count), 
                node_size=node_size, 
                with_labels=True,
                labels = dict(zip(all_nodes,[i.ID for i in all_nodes])),
                width=width, 
                cmap=cmap,
                font_size=font_size
               )
        if enable_im == True:
            ax=plt.gca()
            fig=plt.gcf()
            trans=ax.transData.transform
            trans2=fig.transFigure.inverted().transform
            
            picsize=0.07 # this is the image size
            p2=picsize/2.0
            SIZE = self.TermList[0].data.shape
            for n in G:
                if isinstance(n,Term):
                    xx,yy=trans(pos[n]) # figure coordinates
                    xa,ya=trans2((xx,yy)) # axes coordinates
                    a = plt.axes([xa-p2,ya-p2, picsize, picsize])
                    #a.set_aspect('equal')
                    a.imshow(n.data,cmap='gray',vmin=0,vmax=1)
                    a.axis('off')
                if isinstance(n,Constant):
                    if n.data is None:
                        continue
                    temp = np.array([[[0.5,0.5,1]]])
                    temp = temp.repeat(SIZE[0],axis=0)
                    temp = temp.repeat(SIZE[1],axis=1)
                    temp[n.data[0]] = n.data[1]
                    xx,yy=trans(pos[n]) # figure coordinates
                    xa,ya=trans2((xx,yy)) # axes coordinates
                    a = plt.axes([xa-p2,ya-p2, picsize, picsize])
                    #a.set_aspect('equal')
                    a.imshow(temp,cmap='gray',vmin=0,vmax=1)
                    a.axis('off')
                if isinstance(n,Atom):
                    temp = np.array([[[0.5,0.5,1]]])
                    temp = temp.repeat(SIZE[0],axis=0)
                    temp = temp.repeat(SIZE[1],axis=1)
                    for c in n.father:
                        if isinstance(c.data,list):
                            if temp[c.data[0]][0] == 0.5:
                                temp[c.data[0]] = c.data[1]
                            else:
                                temp[c.data[0]] = 0.5
                    xx,yy=trans(pos[n]) # figure coordinates
                    xa,ya=trans2((xx,yy)) # axes coordinates
                    a = plt.axes([xa-p2,ya-p2, picsize, picsize])
                    #a.set_aspect('equal')
                    a.imshow(temp,cmap='gray',vmin=0,vmax=1)
                    a.axis('off')  
            plt.show()

    def paint_dual(self,
                   figsize=(18,10),
                   node_size=5000,
                   width=2,
                   font_size=12,
                   cmap=plt.cm.tab20):
        nodes_num = [len(self.dualgraph.AtomList),
                     len(self.dualgraph.ConstantList[0:-9]),
                     len(self.dualgraph.ConstantList[-9:]),
                     len(self.dualgraph.DualOfAtomList)]
        all_nodes=self.dualgraph.AtomList+self.dualgraph.ConstantList+self.dualgraph.DualOfAtomList
        
        G = nx.Graph()
        h_spacing = 0.8/float(max(nodes_num))
        v_spacing = 0.8/float(len(nodes_num) - 1)
        node_count = 0
        
        #pos of points
        for i, v in enumerate(nodes_num):
            for j in range(v):
                G.add_node(all_nodes[node_count], pos=(0.1+0.5*(j+1)/(v+1), 0.1 + i*v_spacing))
                node_count += 1
                
        #links of points
        for i in all_nodes:
            for j in i.father:
                G.add_edge(i, j)

        pos=nx.get_node_attributes(G,'pos')
        fig = plt.figure(figsize=figsize)
        
        
        nx.draw(G, pos, 
                node_color=range(node_count), 
                node_size=node_size, 
                with_labels=True,
                labels = dict(zip(all_nodes,[i.ID for i in all_nodes])),
                width=width, 
                cmap=cmap,
                font_size=font_size
               )
        plt.show()
        
        
#目前看似不需要
    '''
    #定义L(x)，仅用于连线
    def L(self, node): 
        L = []
        for nodes in self.nodeList.values():
            if (nodes <= node):
                L.append(nodes)
        return L
        
    #定义U(x)
    def U(self, node):
        U = []
        for nodes in self.nodeList.values():
            if (nodes > node):
                U.append(nodes)
        return U
        '''
    
    # 定义运算 
    def addi(self, data1, data2):  
        value = None
        if (isinstance(data1,np.matrix)) and (isinstance(data2,np.matrix)):
            m = data1.shape[0]
            n = data1.shape[1]
            value = np.zeros(m,n)
            for i in range(m):
                for j in range(n):
                    if (data1[i, j] == 0) or (data2[i, j] == 0):
                        value[i, j] = data1[i, j] + data2[i, j]
                    elif (data1[i, j] == data2[i, j]):
                        value[i, j] = data1[i, j]
                    else:
                        value[i, j] = float('inf') 
        return value

    #初始化画图
    def initialize(self):
        #把constants和v构建出来
        m = 2 
        n = 2
        for i in range(m):
            for j in range(n):
                c1 = Constant((i, j), 0, 'c_'+ str(i) + str(j) + 'b')
                self.addNode(c1)
                c2 = Constant((i, j), 1, 'c_'+ str(i) + str(j) + 'w')
                self.addNode(c2)
        
        v = Constant(None, None, 'v')
        self.addNode(v)

    #把constant和Term连接起来
    #def ConstConnTerm(self):
        for term in self.TermList:
            for const in self.ConstantList:
                if (const <= term) :
                    self.addEdge(term,const)

    #构建0，与所有的constant连接起来
    #def FundemenAtom(self):
        zero = Atom('0')
        self.addNode(zero)

        for const in self.ConstantList:
            self.addEdge(const, zero)

    # 每个节点画对偶，构建0*
    #def Dual(self):
        self.dualgraph = self.Dual()
        
        for term in self.PositiveTerm:
            self.dualgraph.addEdge(v.Dual(), term.Dual())
        
        zero_ = Atom('0*')
        self.dualgraph.addNode(zero_)
        
        #prepare for the algorithm 1: add initial atoms to duals of negative terms 
        self.AddAtomsToDualgraph()
    
        for term in self.TermList:
                self.dualgraph.addEdge(term.Dual(), zero_)
        return self
         
    #Trace
    def Tr(self,node):
        Tr = []
        gla = self.getSonsByType(node, Atom)
        #print([x.ID for x in gla])
        Tr = self.dualgraph.getSonsByType(gla[0].dual,Atom)
        for i in gla:
            Tr = Intersection(Tr,self.dualgraph.getSonsByType(i.dual,Atom))
        return Tr

    #由GL定义<
    def compare(self, a, b):
        justify = set(self.getSonsByType(a, Atom)).issubset(set(self.getSonsByType(b, Atom)))
        return justify
























#-------------------------
    #def the positive relations (which means a constant connecting to a positive term)
    #since there is no clear definition in the paper, we will temporarily use the def
    #until we find inconsistencies. 
    #we will use the list to construct the relation sets with 2-element lists as notations
    #of the relations
    def PositiveRelation(self):
        PR = []
        for term in self.PositiveTerm:
            PR.append([self.getNodesByID('v'),term])
        return PR
        
    #we've let the positive relation constant->term+ be noted as [constant,term]
    #this function will note the negative relations constant-\->term- as [term,constant]
    #as later we need to define the pinning relations set which contains both positve 
    #and negative raltions, we will just combine those two sets(this will only be used 
    #in algorithm6) !!!the constructure is not optimal and needs improving
    #based on page 14 of the paper, negative relations are most likely defined as v/<T-
    def NegativeRelation(self):
        NR = []
        for term in self.NegativeTerm:
            NR.append([term,self.getNodesByID('v')])
        return NR
    

    def findStronglyDiscriminantConstant(self,nodea,termb):
        Omega = [a.dual for a in self.getSonsByType(nodea,Constant)]
        
        U = self.Tr(termb).copy()
        while U !=[]:
            zeta = U[0]
            U.pop(0)
            if Sub(Omega,self.getAllFathers(zeta).copy()) != []:
                c = Sub(Omega,self.getAllFathers(zeta))[0]
                c = c.dual
                return c
        return None          
                
        
    
    #Alogrithm1: enforce negetive trace constraints:
    def EnforceNegativeTrace(self):
        NegativeRelation = self.NegativeRelation().copy()
        i = 0
        for relation in NegativeRelation:
            b = relation[0]#term
            a = relation[1]#constant
            #print(relation)
            
            if set(self.Tr(b)).issubset(set(self.Tr(a))):
                c = None
                while c == None:
                    c =self.findStronglyDiscriminantConstant(a,b)
                    if c is None:
                        #print(Sub(self.getSonsByType(b.Dual(),Constant),self.getAllSons(a.Dual()))[0].ID)
                        h = rd.choice(Sub(self.getSonsByType(b.Dual(),Constant),
                                                       self.getAllSons(a.Dual())))
                        zeta = Atom()
                        #print(zeta,h)
                        self.dualgraph.addNode(zeta)
                        self.dualgraph.addEdge(h,zeta)
                fi = Atom(ID = 'fi%d'%i)
                i+=1
                #print('finished',i,c.ID)
                self.addNode(fi)
                #print(fi.ID)
                self.addEdge(c,fi)
                self.dualgraph.addEdge(fi.dual,c.dual)
                #print('edge')
                #break
        return self


    #Alogrithm2: enforce positive trace constraints:
    def EnforcePositiveTrace(self):
        for relation in self.PositiveRelation().copy():
            d = relation[0]#constant v
            e = relation[1]#positive term
            
            while not set(self.Tr(e)).issubset(set(self.Tr(d))):
                #print(e.ID,d.ID)
                #input()
                zeta = rd.choice(Sub(self.Tr(e),self.Tr(d)))
                ga = Sub(self.getSonsByType(e,Constant),
                         [f.dual for f in self.dualgraph.getAllFathers(zeta).copy()]).copy()
                if ga == []:
                    self.dualgraph.addEdge(zeta,d.dual)
                else:
                    c = rd.choice(ga)
                    #print(c.ID)
                    #print(c.data[1])
                    #input()
                    #print('finished')
                    fi = Atom(ID = 'Atom_to_%s'%c.ID)
                    #print('add',c.ID,fi.ID)
                    self.addNode(fi)
                    self.addEdge(c,fi)
                    self.dualgraph.addEdge(fi.dual,c.dual)
        return self

    #Algorithm 3 Sparse Crossing of a into b
    #We only need to consider a as terms and b as discriminant(in toy example is v), 
    #the other relations is forced when constructing the graph
    def SparseCrossing(self,terma,disb):
        A = Sub(self.getSonsByType(terma,Atom), self.getAllSons(disb))
        U=[]
        for atom in A:
            #print(atom.ID)
            U = []
            B = self.getSonsByType(disb,Atom).copy()
            #print([i.ID for i in B])
            delta = Sub(self.dualgraph.AtomList.copy(),self.dualgraph.getAllSons(atom.dual)).copy()
            i = 0
            while True:
                eps = rd.choice(B)
                #print([j.ID for j in B])
                delta0 = Intersection(delta,self.dualgraph.getAllSons(eps.dual)).copy()
                
                if (set(delta0) != set(delta)) or (delta == []):
                    i+=1
                    fi = Atom("add%d"%i+atom.ID)
                    self.addNode(fi)
                    self.addEdge(atom,fi)
                    self.dualgraph.addEdge(fi.dual,atom.dual)
                    self.addEdge(eps,fi)
                    #print([eps.ID,atom.ID,fi.ID])
                    self.dualgraph.addEdge(fi.dual,eps.dual)
                    delta = delta0.copy()
                    U.append(eps)
                    #print('u',U)
                B.remove(eps)
                if delta == []:
                    break
                #input()
                #self.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)
            #self.paint()
        
        for eps in U:
            #print([i.ID for i in U])
            eps0 = Atom()
            self.addNode(eps0)
            self.addEdge(eps,eps0)
            self.dualgraph.addEdge(eps0.dual,eps.dual)
        
        #input()
        #self.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)
            
        union = Add(U,A).copy()
        for atom in union:
            
            for son in atom.son.copy():
                for father in atom.father.copy():
                    #print(son.ID,father.ID)
                    self.addEdge(father,son)
                    self.dualgraph.addEdge(son.dual,father.dual)
                    #self.paint()
                    #input()
            #print(atom.ID)
            
            self.removeNode(atom)
            self.dualgraph.removeNode(atom.dual)
            #self.paint(figsize=(18,10),node_size=5000,width=2,font_size=12)
        return self
   
    #Algorithm 4: atom set reduction
    def AtomSetReduction(self):
        Q = []
        V = self.ConstantList.copy()
        while True:
            c = rd.choice(V)
            V.remove(c)
            Sc = Intersection(Q,self.getAllSons(c).copy())
            
            if Sc ==[]:
                Wc = self.dualgraph.AtomList.copy()
            else:
                Wc = self.dualgraph.getSonsByType(Sc[0].dual,Atom).copy()
                for atom in Sc:
                    Wc = Intersection(Wc,self.dualgraph.getSonsByType(atom.dual,Atom).copy())
            Fc = [f.dual for f in self.getSonsByType(c,Atom)]
            while set(Wc) != set(self.Tr(c)):
                E = rd.choice(Sub(Wc.copy(),self.Tr(c)))
                fi = rd.choice([f.dual for f in Sub(Fc.copy(),self.dualgraph.getAllFathers(E)).copy()])
                Q.append(fi)
                Wc =Intersection(Wc,self.dualgraph.getSonsByType(fi.dual,Atom))
            if V == []:
                break
        Am = self.AtomList.copy()
        #print([f.ID for f in Q])
        #print([i.ID for i in Sub(Am,Q)])
        for atom in Sub(Sub(Am,Q),[self.getNodesByID('0')]):
            for son in atom.son:
                for father in atom.father:
                    self.addEdge(father,son)
                    self.dualgraph.addEdge(son.dual,father.dual)
            self.removeNode(atom)
            self.dualgraph.removeNode(atom.dual)
        return self
    
    #Algorithm 5: atom set reduction for the dual algebra
    def AtomSetReductionDual(self):
        Q = []
        S = self.NegativeRelation().copy()
        while S != []:
            r = rd.choice(S)# r = [term, constant]
            S.remove(r)
            [b,a] = r
            dis = Sub(self.dualgraph.getSonsByType(b.dual,Atom),
                      self.dualgraph.getAllSons(a.dual))
            if Intersection(dis,Q) == []:
                Q.append(dis[0])
        for atom in Sub(self.dualgraph.AtomList,Q):
            for son in atom.son:
                for father in atom.father:
                    self.dualgraph.addEdge(son,father)
            self.dualgraph.removeNode(atom)
            #self.paint()
        return self
    
    #Algorithm 6: generation of pinning terms and relations
    def GenerationOfPinning(self,Rp = []):
        for fai in self.AtomList:
            #print(fai.ID)
            H = Sub(self.ConstantList, self.getAllFathers(fai))
            d = None
            #self.paint()
            for i in H:
                if d is not None:
                    d = self.addi(d,i.data)
                else:
                    d = i.data
            #self.paint()
            T = Term(np.array(d),'T'+str(fai))
            for c in Intersection(self.ConstantList, self.getAllFathers(fai)):
                Rp.append([T,c])#those are negative relations, thus stored as [term,constant] 
            #self.paint()
        return Rp
    
    def tes(self):
        v = self.getNodesByID('v')
        fr = []
        for term in self.PositiveTerm:
            if not set(self.Tr(term)).issubset(set(self.Tr(v))):
                fr.append([v.ID,term.ID])
        for term in self.NegativeTerm:
            if set(self.Tr(term)).issubset(set(self.Tr(v))):
                fr.append([v.ID,term.ID])
        if fr == []:
            return True
        else:
            return fr
        
    def test(self):
        if self.tes() == True:
            print('The graph fits in the relations.')
        else:
            print('The graph is not right due to the wrong relation between the following pairs.')
            print(self.tes())