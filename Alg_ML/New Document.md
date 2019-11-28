# algebraic machine learning
## Graph
### 过程
1. 定义集合之间的加减交并运算
2. 定义node类，其下子类有MatrixNode，在MatrixNode中定义了序和对偶（看起来像是用矩阵来表示点的特征
3. 定义term，constant，atom和DualOfAtom作为MatrixNode的子类
4. 定义Graph类，内部有两个变量一个存储节点名，一个存储节点数，内部函数为添加节点，添加边，获取节点，删除节点，获取全部节点，获取全部constants，获取全部atom，定义GL函数，GU函数，Gla函数，GLc函数，以及生成对偶图，根据对偶节点的ID名来获取源节点。（根据ID找到对应的点并且给对应的点添加关系）。

### 注意
1. data是个matrix存储的是图像特征


### 问题
1. 对应的对偶使用字符类型来对应，没有建立合理的关系，而且运行时间很长
2. 不知道为什么要根据字典来存储点和点的ID，主要是不知道为什么要有ID

## ML_graph
### 过程
1. 定义ML_graph为Graph的子类（此处应该是把要训练的数据生成原始的图，然后运用一系列的算法）
2. 定义L，U函数

## 改进方案
1. 是否考虑用树结构来写整个程序，保留节点的类，定义的时候就加入序的思想，同时因为对偶图和原图基本只相差箭头方向和dualofatom，所以可以把整个关系表示在一张图上。只需要记录下每个类型的节点的信息负担


## 对于minst数据集
参考资料：[详解minst数据集][1]，[C语言读取minst数据集][2]

[1]: https://www.cnblogs.com/xianhan/p/9145966.html 
[2]: https://blog.csdn.net/baidu_40840693/article/details/82958082
