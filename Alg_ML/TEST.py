#一个和图无关的python试验板
import Graph

G_ML = Graph.ML_Graph()
print(id(G_ML.DualOfML_Graph()))
print(id(G_ML.DualOfML_Graph()))
print(id(G_ML.DualOfML_Graph()))

'''
a = 1
b = 2
c = 3

x = [a,b,c]
y = [b,c]
for t in y:
    if t not in x:
        x.append(t)     
print(x)


class base:
    def __init__(self):
        self.data = None
        
    def __lt__(self, other):
        return self.data > other.data



class NewClass(base):
    def __init__(self, data=None):
        super().__init__
        self.data = data

a = NewClass(3)
b = NewClass(4)
print(not(a < b) )

import random
b = [1,2,3,4,2]
a = random.choice(b)
print(a)
'''
# list1 = ["a","d","c"]

# list2 = ["a","c","d","c","a"]

# print(set(list1).issubset(set(list2)))




