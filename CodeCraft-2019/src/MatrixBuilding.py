#!/usr/bin/python3
# --*--encoding:utf-8--*--
# 此程序的作用是输入一个文本文件一行两个数据以空格隔开，每行两个数都表示的是行列是否存在边，
# 不存在的边不用标注在文本中，第一个数是行第二个数是列
# 此程序的任务基本完成
import re
#-*-coding:utf-8-*-


class DenseGraph:
    def __init__(self,n,directed = False):
        self.n = n # number of vertex
        self.m = 0 #number of edge
        self.directed = directed
        self.matrix = [[0 for i in  range(n)] for i in range(n)] # 构建一个n行n列的矩阵


    def __str__(self):
        for line in self.matrix:
            print(str(line))
        return '' # must return string

    def getNumberOfEdge(self):
        return self.m

    def getNumberOfVertex(self):
        return self.n

    def hasEdge(self,v,w):
        if 0 <= v <= self.n and 0 <= w <= self.n:
            return self.matrix[v][w]
        else:
            raise Exception("vertex not in the Graph")

    def addEdge(self,v,w):
        if 0 <= v <= self.n and 0 <= w <= self.n:
            if self.hasEdge(v,w):
                return self.matrix
            self.matrix[v][w]= 1
            if self.directed is False:
                self.matrix[w][v] = 1
            self.m += 1
        else:
            raise Exception("vertex not in the Graph")

    def returndata(self):
        return self.matrix

def buildGraphFromFile(n,data):
    aGraph = DenseGraph(n, directed=1)  # 必须填入正确的结点个数。。。我真的觉得邻接矩阵不好用
    graphList=[]
    a_list_len = 2
    for jj in range(len(data)):
        temp_data = data[jj]
        graphList.append([temp_data[i:i + a_list_len] for i in range(0, len(temp_data), a_list_len)])
    for i in range(len(graphList)):
        for j in range(len(graphList[i])):
            for k in range(len(graphList[i][j])):
                aGraph.addEdge(graphList[i][j][0],graphList[i][j][1])
                # 这里是生成对应的矩阵，但是没有考虑到是否双向这个问题，
                # 所以在后面需要对矩阵进行编辑，把单向的点对应的矩阵置0
    Matrix = aGraph.returndata()
    return Matrix
    #return aGraph#原
    #v:graphList[i][0],w:graphList[i][1]
if __name__=="__main__":
    #g1=DenseGraph(4, directed=1)  #必须填入正确的结点个数。。。我真的觉得邻接矩阵不好用
    aGraph = buildGraphFromFile(4,'E:\python\PycharmProjects\python3\PythonApplicationDevelopment\HuaweiCompetition\MatrixData')
    print(aGraph.getNumberOfVertex())
    #print(aGraph)

