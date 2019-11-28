'''
This program realize a class to finish 6 tasks of Algebra Machine Learning.
    Developed by Yu Zhang, Yueran Yang, Sijia Chen and Danyang Chen

Developing Details
    2019.10.17  Version 0.0  By Sijia
    2019.10.24  Version 0.1  By Danyang
        Add 4 list to contain Terms, Constants, Atoms...
        Add addNode(), removeNode().
        Still need rewrite other functions.
    2019.10.24   Version 0.2 By Sijia 
        Rewrite the fundamental functions.
        Still need the Alogrithm Functions.
    2019.10.24  Version 0.3 By ZhangYu
        Add painting graph functions
    2019.10.24  Version 0.3 By ZhangYu
        Fix some bugs
        Parameters for painting are available now.
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
        elif isinstance(node, Constant):
            self.ConstantList.append(node)
        elif isinstance(node, Atom):
            self.AtomList.append(node)
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
            self.ConstantList.remove(node)
        elif isinstance(node, Atom):
            self.AtomList.remove(node)
        elif isinstance(node, DualOfAtom):
            self.DualOfAtomList.remove(node)
        return self 
    
    def paint(self,figsize=(18,10),node_size=5000,width=2,font_size=12,cmap=plt.cm.tab20):#Fast
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
                labels = dict(zip(all_nodes,[i.data for i in all_nodes])),
                width=width, 
                cmap=cmap,
                font_size=font_size
               )
        plt.show()
        
    def paint2(self,figsize=(18,10),node_size=5000,width=2,pic_size=0.07,cmap=plt.cm.tab20): #Extremely slow       
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
                width=width, 
                cmap=cmap
               )
        ax=plt.gca()
        fig=plt.gcf()
        trans=ax.transData.transform
        trans2=fig.transFigure.inverted().transform
        
        picsize=0.07 # this is the image size
        p2=picsize/2.0
        for n in G:
            if isinstance(n,Term):
                xx,yy=trans(pos[n]) # figure coordinates
                xa,ya=trans2((xx,yy)) # axes coordinates
                a = plt.axes([xa-p2,ya-p2, picsize, picsize])
                a.set_aspect('equal')
                a.imshow(n.data,cmap='gray')
                a.axis('off')
            if isinstance(n,Constant):
                if n.data is None:
                    continue
                if n.data[1]==0:
                    temp = np.zeros(self.TermList[0].data.shape,dtype='int8')
                    temp[n.data[0]] = 1
                else:
                    temp = np.ones(self.TermList[0].data.shape,dtype='int8')
                    temp[n.data[0]] = 0
                xx,yy=trans(pos[n]) # figure coordinates
                xa,ya=trans2((xx,yy)) # axes coordinates
                a = plt.axes([xa-p2,ya-p2, picsize, picsize])
                a.set_aspect('equal')
                a.imshow(temp,cmap='gray')
                a.axis('off')
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
        self.dualgraph = super().Dual()
        
        for term in self.PositiveTerm:
            self.dualgraph.addEdge(v.Dual(), term.Dual())
        
        zero_ = Atom('0*')
        self.dualgraph.addNode(zero_)
    
        for term in self.TermList:
                self.dualgraph.addEdge(term.Dual(), zero_)
        return self
         
    #Tr
    def Tr(self,node):
        Tr = []
        gla = self.getSonsByType(node, Atom)
        inter_num = len(gla)
        #print([x.ID for x in gla])
        for i in range(inter_num):
            if i == 0:
                Tr.extend(self.dualgraph.getSonsByType(gla[i].Dual(), Atom))
            else:
                Tr = Intersection(Tr, self.dualgraph.getSonsByType(gla[i].Dual(), Atom))
            
        return Tr

    #由GL定义<
    def compare(self, a, b):
        justify = set(self.getSonsByType(a, Atom)).issubset(set(self.getSonsByType(b, Atom)))
        return justify

    
#算法部分，除了算法一基本没有debug，基本代码要debug
    #Alogrithm1: enforce negetive trace constraints:
    def EnforceNegativeTrace(self):
        for i in range(len(self.NegativeTerm)):
            #print(a.ID)
            for j in range(len(self.NegativeTerm)):
                #print(b.ID)
                a = self.NegativeTerm[i]
                b = self.NegativeTerm[j]
                if (not(self.compare(a, b))) and (set(self.Tr(b)).issubset(set(self.Tr(a)))):
                    k = 1
                    print(a, b)
                    while (k<=8):
                        c = self.findStronglyDiscriminant(a,b) 
                        print(c)
                        if (c == None):
                            #print([x.ID for x in self.dualgraph.ConstantList])
                            #print([x.ID for x in self.dualgraph.getSonsByType(b.Dual(), Constant)])
                            #print([x.ID for x in self.dualgraph.getAllSons(a.Dual())])
                            H = Intersection(Sub(self.dualgraph.getSonsByType(b.Dual(), Constant), self.dualgraph.getAllSons(a.Dual())), self.dualgraph.ConstantList)
                            #print('H', [x.ID for x in H])
                            h = rd.choice(H)
                            #print('h', h)
                            a = Atom('atomnew1' + str(i+1) + str (j+1) +str(k))
                            self.dualgraph.addNode(a)
                            k += 1
                            self.dualgraph.addEdgeByID(h.ID, a.ID)
                            print(self.dualgraph.getAllNodeID()) # 这两张dual graph是同一张吗，是的把。。，你做了什么，让他们是同一张。。。
                            #self.dualgraph.addEdgeByID(h.ID, a.ID) 怪不得，你用addbyid找不到节点，横
                        else:
                            break
                    a = Atom('atomnew_1' + str(i+1) + str (j+1))
                    self.addNode(a)
                    a.addFather(c)
                    c.addSon(a)
                    #self.addEdgeByID(c.ID, a.ID)
        return self
   
    def findStronglyDiscriminant(self,a,b):
        W = []
        for c in Intersection(self.getAllSons(a), self.ConstantList):
            #print("     ", c.Dual().ID) # 那就不是这里的问题，为什么这里输出是空    设置断点，他就会停下来，你可以从左边窗口知道哥哥变量的信息，各个
            W.append(c.Dual()) # 他根本不进入我这个断点，就说名这个for一次也没有运行
        #print([x.ID for x in W]) # 监视，输入变量名，他会给你把这个变量的信息放在这里
        U = self.Tr(b)
        #print('u:', [x.ID for x in U])
        while (U != []):
            atom = rd.choice(U)
            print(atom)
            U.remove(atom)
            print(U)
            A = Sub(W, self.dualgraph.getAllFathers(atom))  #  我看不董，你去检查算法，看看每一步问题
            print('A', [x.ID for x in A])#这里的问题，哪个变量你最关心？
            if (A != []):
                B = []
                for a in A:
                    B.append(self.GetNodebyDual(a.ID))
                c = rd.choice(B)
                print('我是', c)
                return c
        return None

    #Alogrithm2: enforce positive trace constraints:
    def EnforcePosTrace(self):
        for d in self.TermClassify().PositiveTerm:
            for e in self.TermClassify().PositiveTerm:
                if (self.compare(d,e)):
                    k = 1
                    while not(set(self.Tr(e)).issubset(set(self.Tr(d)))):
                        A = Sub(self.Tr(e), self.Tr(d))
                        atom = rd.choice(A)
                        T = []
                        for c in Intersection(self.getAllSons(e), self.ConstantList):
                            if atom not in self.Dual.getAllSons(c.Dual()):
                                T.append(c)
                        if (T == []):
                            self.dualgraph.addEdgeByID(d.Dual(), atom.ID)
                        else:
                            c = rd.choice(T)
                            new_atom = Atom('atom_new2' + str(k) + str(d) + str(e))
                            self.addNode(new_atom)
                            self.addEdgeByID(c.ID, new_atom.ID)
                        k += 1
        return self

    #Algorithm 3 Sparse Crossing of a into b
    def SparseCrossing(self, a, b):
        A = Sub(self.getSonsByType(a), self.getAllSons(b))
        k = 0
        for i in A:
            U = []
            B = self.getSonsByType(b, Atom)      
            delta = Sub(self.dualgraph.AtomList, self.dualgraph.getAllSons(i.Dual()))
            while True:
                sigma = rd.choice(B)  
                delta1 = Intersection(sigama, self.dualgraph.getAllSons(sigma.Dual())) 
                if (delta1 != delta) or (delta is None):
                    fai = Atom('atom_new3' + str(k))
                    k += 1
                    self.addNode(fai)
                    self.addEdgeByID(i.ID, fai.ID)
                    self.addEdgeByID(sigama.ID, fai.ID)
                    delta = delta1
                    U.append(sigama) 
                B.remove(sigma)
                if (delta is None):
                    break

            k = 0
            for sigama in U:
                sigma1 = Atom('atom_new_3' + str(k))
                k += 1
                self.addNode(sigama1)
                self.addEdgeByID(sigma.ID, sigma1.ID)
            
            for atom in Add(U, A):
                if isinstance(atom, Atom):
                    self.removeNodeByID(atom.ID)
        return self
            
    #Algorithm 4: atom set reduction
    def AtomSetReduction(self):
        Q = [] 
        R = self.ConstantList
        while True:
            c = rd.choice(R)
            self.removeNodeByID(c.ID)
            Sc = Intersection(Q, self.getAllSons(c))
            if (Sc == []):
                Wc = self.dualgraph.AtomList
            else:
                for i in range(len(Sc)):
                    if (i == 0):
                        Wc = self.dualgraph.getSonsByType(Sc[i].Dual)
                    else:
                        Wc = Intersection(Wc, self.dualgraph.getSonsByType(Sc[i].Dual))
            Faic = []
            for i in self.getSonsByType(c, Atom):
                Faic.append(i.Dual())
            while (Wc != self.Tr(c)):
                atom = rd.choice(Sub(Wc, self.Tr(c)))
                Random = []
                for i in Sub(Faic, self.getAllFathers(atom)):
                    Random.append(self.GetNodebyDual(i))
                sigma = rd.choice(Random)
                Q.append(sigma)
                Wc = Intersection(Wc, self.dualgraph.getSonsByType(sigma.Dual(), Atom))
            if R == []:
                break

        for atom in Sub(self.AtomList, Q):
            self.removeNodeByID(atom.ID)
        return self

    #Algorithm 5: atom set reduction for the dual algebra
    def AtomReductionFordual(self):
        Q = []
        S = self.TermClassify().NegativeTerm
        while (S is not None):
            r = rd.choice(S)
            S.remove(r)
            r = not(self.compare(a,b)) #假命题
            inter = Sub(self.dualgraph.getSonsByType(b, Atom), self.dualgraph.getSonsByType(a, Atom))
            if (Intersection(inter, Q) == []):
                atom = rd.choice(inter)
                self.addNode(atom)
        for atom in Sub(self.dualgraph.AtomList, Q):
            self.dualgraph.removeNodeByID(atom.ID)
        return self
    
    #Algorithm 6: generation of pinning terms and relations
    def GenerationOfPinning(self):
        #Rp是一列存在的关系式
        for fai in self.nodeList.values():
            H = Sub(self.ConstantList, self.U(fai))
            for i in range(len(H)):
                if (i == 0):
                    data = H[i].data
                else:
                    data = self.addi(data, H[i].data)
            T = Term(data,'T'+str(fai))
            for c in Intersection(self.ConstantList, self.U(fai)):
                Rp.append()  #加关系

