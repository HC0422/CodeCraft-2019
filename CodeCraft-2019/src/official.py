#!/usr/bin/python3
import networkx as nx
#import matplotlib.pyplot as plt
import numpy as np
import operator
import DataProcessing
import MatrixBuilding
def readCar(filePath):
    # 这是读取车辆信息的函数
    print(filePath)
    CarId = []  # 存储路口的ID值
    StartId = []  # 存储对应的每个路口包含的道路ID编号，里面存储的也是列表
    EndID = []  # 存储生成连通图的数据，是遍历路口里面的道路编号
    CarSpeed = []# 存储路口的CarSpeed[i][0]:ID值 和CarSpeed[i][1]:车速
    PlanTime = []
    # 两轮遍历找出包如果包含相同道路编号则存储备用。
    CleanCrossRoadId = []  # 存储清洁的道路ID，就是去除-1的每个路口实际连接的道路ID
    with open(filePath, 'r', encoding='utf-8') as f:
        for line in f:
            # 注释 # 开头
            if line.startswith(r'#'):
                pass
            else:
                temp_CarSpeed = []
                temp_PlanTime = []
                line = eval(line)
                temp_CarId = line[0]
                temp_StartID = line[1]
                temp_EndID = line[2]
                temp_CarSpeed.append(line[0])
                temp_CarSpeed.append(line[3])
                temp_PlanTime.append(line[0])
                temp_PlanTime.append(line[4])
                StartId.append(temp_StartID)
                CarId.append(temp_CarId)
                EndID.append(temp_EndID)
                CarSpeed.append(temp_CarSpeed)
                PlanTime.append(temp_PlanTime)
    return CarId,StartId,EndID,CarSpeed,PlanTime


def uniformization(CarSpeed, PlanTime, sorted_carRunTime):
    # 将时间数据归一化
    sorted_carRunTime = sorted(sorted_carRunTime.items(), key=operator.itemgetter(1), reverse=False)
    #x_max = sorted_carRunTime[len(CarSpeed) - 1][1]
    sorted_carRunTime = dict(sorted_carRunTime)
    #y_max = len(set(sorted_carRunTime.values()))
    #while((y_max + 35) < x_max ):
    sorted_carRunTime = sorted(sorted_carRunTime.items(), key=operator.itemgetter(1), reverse=False)
    x_max = sorted_carRunTime[len(CarSpeed) - 1][1]
    x_min = sorted_carRunTime[0][1]
    sorted_carRunTime = dict(sorted_carRunTime)
    sorted_carRunTime_keys = sorted_carRunTime.values()
    sorted_carRunTime_item1 = set(sorted_carRunTime_keys)
    y_max = int(len(sorted_carRunTime_item1))
    y_min = 1
    for key1, item1 in sorted_carRunTime.items():
        # y = (ymax-ymin)*(x-xmin)/(xmax-xmin) + ymin
        sorted_carRunTime[key1] = int(y_min + ((y_max - y_min) / (x_max - x_min)) * (item1 - x_min)) + 1
    for key1, item1 in sorted_carRunTime.items():
        if sorted_carRunTime[key1] <= PlanTime[key1]:
            sorted_carRunTime[key1] = PlanTime[key1]
    return sorted_carRunTime

def createStarttime(CarSpeed, PlanTime, RoadSpeed, RoadChanel, RoadLength, path):
    RoadChanel = dict(RoadChanel)
    # sorted_carRunTime列表套元组  车的近似运行时间
    # 排序之后的数据，转化成字典之后排序被破坏
    sorted_carRunTime = computeCarRunAllTime(CarSpeed, RoadSpeed, RoadLength, path, RoadChanel)
    sorted_carRunTime = dict(sorted_carRunTime)
    sorted_carRunTime_sorted = sorted(sorted_carRunTime.items(), key=operator.itemgetter(1), reverse=False)
    PlanTime = dict(PlanTime)
    PlanTime_sorted = sorted(PlanTime.items(), key=operator.itemgetter(1), reverse=False)
    New_time = []
    temp_plan_time = []
    temp_car_run_time = []
    temp_car_run_id = []
    flag = 0
    Stop_bit = 0
    temp_max_run_time = 0
    max_plan_time = np.max(PlanTime.values())# 计算计划时间里最长的
    while(len(PlanTime) != flag+1):
        for i in range(flag + 1,len(PlanTime)):
            j = i + 1
            try:
                plan_i_time_judge = PlanTime_sorted[j][1]
            except:
                plan_i_time_judge = 1
            plan_i_time = PlanTime_sorted[i][1]
            flag = i
            if plan_i_time == plan_i_time_judge:
                temp_car_run_time = []
                temp_car_run_id = []
                temp_plan_time.append(PlanTime_sorted[i])
            else:
                for k in range(len(temp_plan_time)):
                    temp_car_run_time.append(sorted_carRunTime[temp_plan_time[k][0]])# temp_plan_time[k][0]:这是道路的ID号码
                    temp_car_run_id.append(temp_plan_time[k][0])
                temp_plan_time = []
                if not temp_max_run_time:
                    temp_max_run_time_fist = np.max(temp_car_run_time)
                temp_max_run_time = temp_max_run_time + np.max(temp_car_run_time)# 找出最大的

                #print(temp_max_run_time)
                # 将本次求得的运行的时间加上上次的计划时间，就是本次的实际时间存入字典
                for fg in range(len(temp_car_run_time)):
                    #print(temp_car_run_id[fg])
                    PlanTime[temp_car_run_id[fg]] = PlanTime[temp_car_run_id[fg]] + temp_max_run_time - temp_max_run_time_fist
                break
            Stop_bit = Stop_bit + 1


    #Starttime = uniformization(CarSpeed, PlanTime, dict(New_time))
    # Starttime存入列表的形式是:{'车的ID值':'这辆车的出发时间'}
    return PlanTime

def computeCarRunAllTime(CarSpeed, RoadSpeed, RoadLength, path, RoadChanel):
    RoadChanel = dict(RoadChanel)
    # path[-1] =[20239, 5129, [5092], [5079], [5064], [5050]]
    # 我们需要存入字典cartime = {'车的ID值':'这辆车的模糊运行时间'}
    # 按照字典的键sorted(cartime.items(),key=operator.itemgetter(0),reverse=False)默认False升序
    # 按照字典的值sorted(cartime.items(),key=operator.itemgetter(1),reverse=False)默认False升序
    # 遍历字典：for key, item in grade.items():  key：字典的键   item：字典的值
    # 通过list()方法将字典先转化为列表,再进行取值
    carRunTime = {}# cartime = {'车的ID值':'这辆车的模糊运行时间'} 存放车的模糊运行时间
    carRunningState = {}
    path_fromto_path = {}
    for i in range(len(CarSpeed)):
        temp_road_path = []
        j = 2
        try:
            while (path[i][j][0]):
                temp_road_path.append(path[i][j][0])
                j = j + 1
        except:
            pass
        temp_times_time_sum = 0
        temp_length = 0
        for k in range(len(temp_road_path)):#temp_road_path[k]
            for p in range(len(RoadSpeed)):
                if RoadSpeed[p][0] == temp_road_path[k]:# temp_road_path[k]标记得是路的ID
                    #此处应该保存的数据有车辆的每个运行时间片 { 时间片1:道路ID1，时间片2：道路ID2，... }
                    v_temp_road_speed = RoadSpeed[p][1]
                    v = min(CarSpeed[i][1],v_temp_road_speed)
                    temp_times_time = int((RoadLength[p] + v - 1 - temp_length) / v)# 这是这辆这在本条道路上的运行时间
                    # 并且在下一条路上也行驶了部分距离
                    temp_length = RoadLength[p] % v# 这是这辆车在本道路的部分行驶距离，下一条路上的行驶时间为
                    if temp_road_path[k]==temp_road_path[-1]:# 首先应该判断车辆是否到达，如果到达判断路口继续运行的距离是否大于1，
                        # 如果大于1说明车辆能够在此时间片到达路口，否则将对应的时间片加一，表示得等到下一个时间片才能到达
                        if temp_length < 1:
                            temp_times_time = temp_times_time + 1#RoadFromD, RoadToD
                    temp_times_time_sum = int(temp_times_time_sum + temp_times_time)
        carRunTime[CarSpeed[i][0]] = int(temp_times_time_sum)# temp_times_time_sum:这是某辆车的一条路径的总的运行时间
    #carRunningState格式应该是：{车ID1:{路ID1:[1,2,3]，路ID2:[3,4,5],...}，车ID2: ...,...}
    sorted_carRunTime = sorted(carRunTime.items(), key=operator.itemgetter(1), reverse=False)
    # sorted_carRunTime  这里得到的时间是没有经过优化的，直接使用plantime+本次运行的最长时间=下次运行的开始时间
    # 进行跑的时间，实现路线时应该使用的是相同路线的问题统一进行处理
    # [[CarId, From, To, PlanTime, RunTime, StartTime, [路径]],[],[]...]
    #print(carRunningState) # {10240: {5025: [0, 1, 2, 3], 5042: [7, 8, 9, 10, 11], 5053: [12, 13, 14], 5031: [4, 5, 6]},10241:...}
    #print(path_fromto_path)
    return sorted_carRunTime


def createGraph(Matrix, roadID, CarId, StartId, EndID, RoadLenthMatrix_2D, HashCrossId):
    # 这是使用矩阵构建图并生成最终答案的函数
    G = nx.DiGraph()
    path = []
    Matrix = np.array(Matrix)
    for i in range(0, len(Matrix)):
        G.add_node(i)
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if Matrix[i][j] == 1:
                # G.add_edges_from([(i, j)])
                G.add_edge(i, j, weight = RoadLenthMatrix_2D[i][j])
    nx.draw(G, with_labels=True, node_color='white', edge_color='green', node_size=400, alpha=0.5)
    #plt.show()
    for i in range(len(CarId)):
        temp_starttime = 1# Starttime[i]此处与生成的StratTime时间的程序在先后运行上有冲突，
        # 所以此处的temp_starttime为错误的时间，后面进行答案存储的时候进行改进，不从此处取时间，而是从别处取时间
        start = StartId[i]
        end = EndID[i]
        for hasih in range(len(HashCrossId)):
            if start==HashCrossId[hasih]:
                start = hasih
            if end==HashCrossId[hasih]:
                end = hasih
        p = nx.shortest_path(G, source=start, target=end)
        # print('源节点为:{},终点为:{},路径为:{}'.format(start, end, p))#系统不支持
        temp_path = []
        temp_path.append(CarId[i])
        temp_path.append(temp_starttime)
        # (10000, 15, 35, 6, 1)   15和35分别代表的出发和终止的路口
        search_road_ID = []
        for j in range(len(p)):
            search_road_ID.append(roadID[p[j]])  # 找到路径列表中对应的ID编号并将ID列表存储到列表中
        for k in range(len(search_road_ID)):
            road = []
            try:
                # 遍历找出列表中相同的元素
                road = [l for l in search_road_ID[k] if l in search_road_ID[k + 1]]
                if road:
                    temp_path.append(road)
            except:
                pass
        path.append(temp_path)
        #print(temp_path)
    return path

def savePath(path, answer_path, Starttime):
    # 保存路径至answer文件夹中。
    with open(answer_path, 'w', encoding='utf-8') as ww:
        ww.write('')
    save_path = []
    for i in range(len(path)):
        trpul = str('(') + str(path[i][0]) + str(',') + str(Starttime[path[i][0]])
        # f.write(str(path[i][1]))# 写入实际调度时间，原本是在path里面的，现在因为需要所以换了存储位置
        # f.write(',')
        j = 2
        try:
            while (path[i][j][0]):
                trpul = trpul + str(',') + str(path[i][j][0])
                j = j + 1
                # f.write(',')
        except:
            pass
        trpul = trpul + str(')') + str('\n')
        save_path.append(trpul)

    with open(answer_path, 'a+', encoding='utf-8') as f:
        for i in range(len(path)):
            trpul = save_path[i]
            #trpul = (path[i][0],path[i][1],path[i][2][0],path[i][2][0],path[i][2][0],path[i][2][0])
            f.write(trpul)
    '''
    for i in range(len(path)):
        with open(answer_path, 'a+', encoding='utf-8') as f:
            #trpul = (path[i][0],path[i][1],path[i][2][0],path[i][2][0],path[i][2][0],path[i][2][0])
            f.write('(')
            f.write(str(path[i][0]))# 写入汽车的ID
            f.write(',')
            f.write(str(Starttime[path[i][0]]))
            #f.write(str(path[i][1]))# 写入实际调度时间，原本是在path里面的，现在因为需要所以换了存储位置
            #f.write(',')
            j=2
            try:
                while(path[i][j][0]):
                    f.write(',')
                    f.write(str(path[i][j][0]))# 不断写入线路
                    j = j + 1
                    #f.write(',')
            except:
                pass
            f.write(')')
            f.write('\n')
            #f.close()
    '''

def MatrixFixisDuplex(Matrix, road_path, HashCrossId):
    # 修订矩阵不能识别单双向的问题，返回有单双向属性的矩阵
    HashCrossId = dict(HashCrossId)
    isDuplex = []
    RoadSpeed = []# 二维RoadSpeed[i][0]:车辆ID。   RoadSpeed[i][1]:车辆速度。
    RoadChanel = []
    RoadLength = []
    RoadFrom = []
    RoadTo = []
    with open(road_path, 'r', encoding='utf-8') as f:
        for line in f:
            temp = []
            # 注释 # 开头
            if line.startswith(r'#'):
                pass
            else:
                temp_RoadSpeed = []
                temp_RoadChanel = []
                line = eval(line)
                temp_from = line[4]
                temp_to = line[5]
                temp_isDuplex = line[6]
                # 此处加入ID映射  key是归一化后的路口ID
                for key,value in HashCrossId.items():
                    if temp_from == value:
                        temp_from = key
                    if temp_to == value:
                        temp_to = key
                temp.append(temp_from)
                temp.append(temp_to)
                temp.append(temp_isDuplex)
                isDuplex.append(temp)# 存储的数据格式为：[[1,3,1],[3,8,1],[32,21,0],[]]
                temp_RoadSpeed.append(line[0])
                temp_RoadSpeed.append(line[2])
                temp_RoadChanel.append(line[0])
                temp_RoadChanel.append(line[3])
                temp_RoadLength = line[1]
                #temp_RoadFrom = line[4]
                #teemp_RoadTo = line[5]
                RoadSpeed.append(temp_RoadSpeed)
                RoadChanel.append(temp_RoadChanel)
                RoadLength.append(temp_RoadLength)
                RoadFrom.append(temp_from)# temp_RoadFrom
                RoadTo.append(temp_to)# teemp_RoadTo
    print(isDuplex)
    #isDuplex 存储的是归一化的[[from，to，单双向],...]  所以isDuplex[i][1]不需要减去1
    for i in range(len(isDuplex)):
        if isDuplex[i][2] == 0:
            Matrix[isDuplex[i][1]][isDuplex[i][0]] = 0
    RoadLenthMatrix_2D = np.zeros((len(Matrix), len(Matrix)))
    for k in range(len(RoadFrom)):
        RoadLenthMatrix_2D[RoadFrom[k]-1][RoadTo[k]-1] = RoadLength[k-1]
    return Matrix, RoadSpeed, RoadChanel, RoadLength, RoadLenthMatrix_2D


def createAnswer(car_path, CleanCrossRoadId, Matrix, answer_path, road_path, HashCrossId):
    # MatrixFixisDuplex编辑函数用来处理单双向的问题
    Matrix_isDuplex, RoadSpeed, RoadChanel, RoadLength, RoadLenthMatrix_2D = MatrixFixisDuplex(Matrix, road_path, HashCrossId)
    CarId, StartId, EndID, CarSpeed, PlanTime = readCar(car_path)
    # createGraph(Matrix_isDuplex, CleanCrossRoadId, CarId, StartId, EndID)
    # 此处运行时间最长
    path = createGraph(Matrix_isDuplex, CleanCrossRoadId, CarId, StartId, EndID, RoadLenthMatrix_2D, HashCrossId)
    # 此处运行时间较长
    Starttime = createStarttime(CarSpeed, PlanTime, RoadSpeed, RoadChanel,
                                RoadLength, path)  # 这个函数是用来生成车子的具体出发时间的，也就是出发时间调度优化算法
    savePath(path, answer_path, Starttime)
    return path

if __name__=="__main__":
    n, data, CleanCrossRoadId = DataProcessing.readCross("E:\python\PycharmProjects\python3\PythonApplicationDevelopment\HuaweiCompetition\config\cross.txt")
    Matrix = MatrixBuilding.buildGraphFromFile(n, data)
    answer_path = 'E:\python\PycharmProjects\python3\PythonApplicationDevelopment\HuaweiCompetition\config\\answer.txt'
    car_path = "E:\python\PycharmProjects\python3\PythonApplicationDevelopment\HuaweiCompetition\config\car.txt"
    path = createAnswer(car_path, CleanCrossRoadId, Matrix,answer_path)
    print(path)


