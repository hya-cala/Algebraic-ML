#包含代数机器学习图的继承+6个算法（算法需要debug）

from Graph import *

class ML_Graph(Graph):
    def __init__(self):
        super().__init__()
        self.PositiveTerm = []
        self.NegativeTerm = []
        self.zero = []
        self.zero_ = []
        self.dualgraph = Graph()

    #定义L(x)
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
    
    #定义运算
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

    #把constants和v构建出来
    def ConsituteConstants(self):
        m = 2
        n = 2
        for i in range(m):
            for j in range(n):
                C = np.zeros([m,n])
                A = np.zeros([m,n])
                C = np.matrix(C)
                A = np.matrix(A)
                C[i, j] = -1
                
                constant = Constant(C,'Constant_'+str(i+1)+','+str(j+1)+'w')
                #print(C,'Constant_'+str(i+1)+','+str(j+1)+'w')
                self.addNode(constant)
                
                A[i, j] = 1
                constant = Constant(A,'Constant_'+str(i+1)+','+str(j+1)+'b')
                #print(C,'Constant_'+str(i+1)+','+str(j+1)+'b')
                self.addNode(constant)
        
        v = Constant(None,'v')
        self.addNode(v)
        return self

    #Term为输入的项目,分类
    def TermClassify(self):
        for term in self.nodeList.values():
            if (isinstance(term,Term)):
                if (term.data[0, 0] == term.data[1, 0] == 1) or (term.data[0, 1] == term.data[1, 1] == 1):      #满足某种条件
                    self.PositiveTerm.append(term)
                else:
                    self.NegativeTerm.append(term)
        return self

    #把constant和Term连接起来
    def ConstConnTerm(self):
        for term in self.nodeList.values():
            for const in self.nodeList.values():
                if (const <= term) and (isinstance(term, Term)) and (isinstance(const, Constant)):
                    self.addEdgeByID(term.ID,const.ID)
        return self
    
    #构建0，与所有的constant连接起来
    def FundemenAtom(self):
        if (self.zero == []):
            zero = Atom('zero')
            self.zero.append(zero)
            self.addNode(zero)
        else:
            zero = self.zero[0]
            self.addNode(zero)

        for const in self.nodeList.keys():
            if (isinstance(self.getNodesByID(const),Constant)):
                self.addEdgeByID(const,'zero')
        return self

    #每个节点画对偶，构建0*
    def DualOfML_Graph(self):
        self.dualgraph = self.Dual()
        
        for term in self.PositiveTerm:
            self.dualgraph.addEdgeByID('v_dual', term.Dual().ID)
        
        if (self.zero_ == []):
            zero_ = Atom('zero_')
            self.zero_.append(zero_)
            self.dualgraph.addNode(zero_)
        else:
            zero_ = self.zero_[0]
            self.dualgraph.addNode(zero_)
        
        for term in self.nodeList.values():
            if(isinstance(term,Term)):
                term.Dual().addSon(zero_)
                zero_.addFather(term.Dual())
        return self.dualgraph
            
    #Tr
    def Tr(self,node):
        Tr = []
        gla = self.getSonsByType(node,Atom)
        inter_num = len(gla)
        #print([x.ID for x in gla])
        for i in range(inter_num):
            if i == 0:
                Tr.extend(self.dualgraph.getSonsByType(gla[i].Dual(),Atom))
            else:
                Tr = intersection(Tr, self.dualgraph.getSonsByType(gla[i].Dual(),Atom))
            
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
                            #print([x.ID for x in self.dualgraph.getAllConstants()])
                            #print([x.ID for x in self.dualgraph.getSonsByType(b.Dual(), Constant)])
                            #print([x.ID for x in self.dualgraph.getAllSons(a.Dual())])
                            H = intersection(Sub(self.dualgraph.getSonsByType(b.Dual(), Constant), self.dualgraph.getAllSons(a.Dual())), self.dualgraph.getAllConstants())
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
        for c in intersection(self.getAllSons(a), self.getAllConstants()):
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
                        for c in intersection(self.getAllSons(e), self.getAllConstants()):
                            if atom not in self.DualOfML_Graph.getAllSons(c.Dual()):
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
            delta = Sub(self.dualgraph.getAllAtoms(), self.dualgraph.getAllSons(i.Dual()))
            while True:
                sigma = rd.choice(B)  
                delta1 = intersection(sigama, self.dualgraph.getAllSons(sigma.Dual())) 
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











#-------------------------------------------------            
    #Algorithm 4: atom set reduction
    def AtomSetReduction(self):
        #initiate set Q =[] and lam = ConstantList
        Q = []
        lam = ConstantList # this the constant set of the master graph
        while lam !=[]:
            c = rd.random(lam)
            lam.remove(c)
            sc = intersection(Q,self.GetAllSons(c))
            if sc !=[]:
                wc = AtomsinDual#this is the atom set of the dual graph
            else:
                wc = self.getSonsByTypes(sc[0].Dual(),Atom)
            for fi in sc:
                wc = intersection(wc,self.getSonsByTypes(fi.Dual(),Atom))
            fc = [i.Dual() for i in self.getSonsByTypes(c,Atom)]
            while wc != self.Tt(c):
                Temp = Sub(wc,self.Tr(c))
                k = rd.random(Temp)
                Temp2 = Sub(sc,self.getAllFathers(k))
                f_dual = rd.random(Temp2)
                #here we still use the ID
                f = self.GetNodebyDual(f_dual.nodeID)
                Q.append(f)
                wc = intersection(wc,self.getSonsByTypes(f_dual,Atom))
        #delete the atoms in the set A(M)\Q
        dele_set = Sub(AtomsList,Q)
        for atoms in dele_sets:
            self.removeNodeByID(atoms.ID)
        return self
        
    # personally, i regard the negative relations as the relations between 
    #the negative terms and the constants not in the chosen terms        
    def NegativeRelation(self):
        NR = []
        for term in self.NegativeTerm:
            for constant in Sub(ConstantList,self.getSonsByType(term,Constant)):
                NR.append([term,constant])
        return NR
    
    # since the relations cannot be well expressed with the existing structure
    # the return will be a list of list(a,b), where a is a positive term and b is a constant
    def PositiveRelation(self):
        PR = []
        for term in self.PositiveTerm:
            for constant in self.getSonsByTypes(term,Constant):
                PR.append([term,constant])
        return PR
        
    #Algorithm 5: atom set reduction for the dual algebra
    def AtomReductionFordual(self):
        Q = [] #initialize the Q =[]
        s = self.NegativeRelation()
        while s !=[]:
            r=rd.random(s)
            s.remove(r)
            [b,a] = r
            dis = Sub(self.getSonsByType(b.dual,Atom),self.getAllFathers(a.Dual()))
            if dis !=[]:
                Q.append(dis[0])
        #delete all the atom in the set A(m*)\Q
        dele_set = Sub(self.Dual(self).getAllAtoms(),Q)
        for atoms in dele_set:
            self.removeNodeByID(atoms.ID)
        return self
    
    #question: how to express relations in Rp
    
    #Algorithm 6: generation of pinning terms and relations
    def GenerationOfPinning(self,Rp):
        #Rp is a new or existing set of pinning relations
        for node in self.getAllAtoms():
            H = Sub(self.getAllConstants(),self.getAllSons(node))
            T_node = None
            for constant in H:
                T_node = self.addi(T_node,constant)
            I = intersection(self.getAllConstants(),self.getAllFathers(node))
            for constant in I:
                Rp.append()
                
        return Rp
