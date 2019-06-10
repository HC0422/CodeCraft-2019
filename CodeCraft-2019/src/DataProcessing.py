#!/usr/bin/python3
# --*--encoding:utf-8--*--
import re
# 这是数据处理的程序，功能是生成矩阵所需要的构建0,1的内容
def readCross(filePath):
    print(filePath)
    CrossId = []# 存储路口的ID值
    HashCrossId = {}  # 存储路口的映射ID值 {0：24，1：56，。。。}
    CrossRoadId= []# 存储对应的每个路口包含的道路ID编号，里面存储的也是列表
    CrossLinkCross = []# 存储生成连通图的数据，是遍历路口里面的道路编号
    # 两轮遍历找出包如果包含相同道路编号则存储备用。
    CleanCrossRoadId = []# 存储清洁的道路ID，就是去除-1的每个路口实际连接的道路ID
    hash = 0
    with open(filePath, 'r', encoding='utf-8') as f:
        for line in f:
            # 注释 # 开头
            if line.startswith(r'#'):
                pass
            else:
                line=eval(line)
                temp_CrossTruthlyId = line[0]# 此处的ID值为实际的ID值所以要映射到0,1,2上面去
                temp_roadId = []
                for i in range(len(line)):
                    if i != 0:
                        temp_roadId.append(line[i])
                CrossRoadId.append(temp_roadId)
                CrossId.append(temp_CrossTruthlyId)
                CleanCrossRoadId = CrossRoadId
        # 移除路口道路编号里面的 -1
        for i in range(len(CrossRoadId)):
            try:
                CleanCrossRoadId[i].remove(-1)
                CleanCrossRoadId[i].remove(-1)
            except:
                pass
        # 遍历数据，找到含有列表中的数据的列表数据
        #print(CleanCrossRoadId)# CleanCrossRoadId是存储的道路的ID值
                #print(temp_CrossLinkCross)
        # 此处应该反馈的数据有：路口数量、路口相互之间的连接关系数据
        #print(CrossLinkCross)# 里面存储的是0-35等36个数相互的联系，表示路口的相互联系，
        # 0-1代表路口1和路口2（源数据路口为:1-36）有联系并且之间的道路ID为5000
    #print(CleanCrossRoadId)
    for i in range(len(CleanCrossRoadId)):
        temp_CrossLinkCross = []
        for j in range(len(CleanCrossRoadId)):
            # temp_CrossLinkCross 反馈的是列表中含有的相同元素
            # temp_CrossLinkCross = [x for x in CleanCrossId[j] if x in CleanCrossId[i]] #遍历
            for haha, a in enumerate(CleanCrossRoadId[i]):
                for hehe, b in enumerate(CleanCrossRoadId[j]):
                    if a == b:  # and haha!=hehe:
                        temp_CrossLinkCross.append(i)
                        temp_CrossLinkCross.append(j)
        if temp_CrossLinkCross:
            CrossLinkCross.append(temp_CrossLinkCross)

    for hashe in range(len(CrossId)):
        HashCrossId[hashe] = CrossId[hashe]
    return len(CrossId),CrossLinkCross,CleanCrossRoadId, HashCrossId
        #print(CrossId,'\n',CrossRoadId,'\n',CrossLinkCross)

if __name__=="__main__":
    filepath = []
    #filepath.append('..\HuaweiCompetition\\road.txt')
    filepath.append('..\config\cross.txt')
    #filepath.append('..\HuaweiCompetition\\car.txt')
    for i in range(len(filepath)):
        print(readCross(filepath[i]))

