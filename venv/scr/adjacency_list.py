import copy
from data_store import toDictV2, toDictV3, toDictV4
from environment_variable import ruiboshi_excel
from collections import deque, defaultdict
# -*- coding: utf-8 -*-
PageName = 'page_element'


class Page:
    def __init__(self, name, excel_path=ruiboshi_excel, sheet=PageName):
        # 初始化时，将excel中每页对应的元素上传到self.neighbor
        self.excel_path = excel_path
        self.sheet = sheet
        self.pageName = name
        self.neighbor = self.__get_adjacency_list()

    def add_neighbor(self, neighbor, list_elem):
        if not self.neighbor[neighbor]:
            self.neighbor[neighbor] = [list_elem]
        else:
            self.neighbor[neighbor].append(list_elem)

    def __get_adjacency_list(self):  # 将self.excel_path文件中的页面跳转元素上传到类中
        return toDictV2(self.excel_path, self.pageName, self.sheet)

    def __str__(self):  # 将self.pageName设置为类的打印
        return self.pageName

    def __getitem__(self, item):  # 将self.neighbor设置为类的迭代对象
        return self.neighbor[item]


class Vertex(Page):
    def __init__(self, name, sheet):
        super().__init__(name, sheet=sheet)
        self.firstEdge = None


class Edge(object):
    def __init__(self, adjVex):
        self.adjVex = adjVex
        self.next = None


class LinkedGraph(object):
    # 实现输入图的顶点和边，能够得到邻接表
    def __init__(self, excel_path=ruiboshi_excel, sheet=PageName):
        # 存储节点信息的excel文件的绝对路径
        self.excel_path = excel_path
        self.sheet = sheet
        # 图的顶点
        self.vers = self.__get_pageName()
        # print(self.vers)
        # 图的边
        self.edges = self.__get_edges()
        # print(self.edges)
        # vexLen 图的顶点个数
        self.vexLen = len(self.vers)
        # 存放顶点的列表
        self.listVex = [Vertex for i in range(self.vexLen)]
        for i in range(self.vexLen):
            self.listVex[i] = Vertex(self.vers[i], sheet=self.sheet)
        # 表示图的表
        for edge in self.edges:
            # print(edge)
            c1 = edge[0]
            c2 = edge[1]
            # print(c1, c2)
            # print(c1 in self.vers, c2 in self.vers)
            self.__addEdge(c1, c2)
        self.adjacencyList = self.get_relation()

    def __addEdge(self, c1, c2):
        # 找到c1,c2的下标值
        p1 = self.__getPosition(c1)
        p2 = self.__getPosition(c2)
        edge1 = Edge(p1)
        edge2 = Edge(p2)
        if self.listVex[p1].firstEdge is None:
            self.listVex[p1].firstEdge = edge2
        else:
            self.__LinkLast(self.listVex[p1], edge2)

        # if self.listVex[p2].firstEdge is None:
        #     self.listVex[p2].firstEdge = edge1
        # else:
        #     self.__LinkLast(self.listVex[p2], edge1)

    def __getPosition(self, key):
        for i in range(self.vexLen):
            if self.vers[i] == key:
                return i

    def __LinkLast(self, list, edge):
        p = list.firstEdge
        while p.next:
            p = p.next
        p.next = edge

    # 读取self.excel_path文件的顶点
    def __get_pageName(self):
        return toDictV3(self.excel_path, self.sheet)

    def __get_edges(self):  # 将self.excel_path文件中的页面名称上传到类中
        return toDictV4(self.excel_path, sheet=self.sheet)

    def getAllElem(self):
        # 获取所有页面元素，返回dict
        vertexList = self.listVex
        allPageElemDict = dict()
        for v in vertexList:
            allElem = []
            for vel in v.neighbor.values():
                allElem += vel
            allPageElemDict[v.pageName] = allElem
        return allPageElemDict

    def get_relation(self):
        '''
        生成邻接表 {顶点:[各邻接点]}
        :return:    dict
        '''
        result = dict()
        for i in range(self.vexLen):
            # print(self.listVex[i].pageName, end="->")
            edge = self.listVex[i].firstEdge
            result[self.listVex[i].pageName] = []
            while edge:
                # print(self.listVex[edge.adjVex].pageName, end=" ")
                result[self.listVex[i].pageName].append(self.listVex[edge.adjVex].pageName)
                edge = edge.next
            # print()
        # print(result)
        return result

    def bfs(self, _dict, initial, destination):
        # 广度优先搜索 ，这个没有用处
        search_queue = deque()  # 创建一个队列
        search_queue += _dict[initial]  # 将起始点的相邻点都加入到这个搜索队列中
        searched = []  # 这个数组用于记录检查过的点
        while search_queue:
            node = search_queue.popleft()
            if node not in searched:  # 仅当该点没检查过时才检查
                if node == destination:
                    print("找到目的地")
                    return True
                else:
                    search_queue += _dict[node]
                    searched.append(node)  # 将这个人标记为检查过
        return False

    def dfs_old(self, initial, destination, searched=None, way=None, result=None):
        '''
        深度优先搜索,用于找到所有的路径
        邻接表有问题会导致搜索结构出错
        :param initial:
        :param destination:
        :param searched:
        :param way:
        :param result:
        :return:
        '''
        if result is None:  # 这样可以防止result在函数调用之间意外共享，而不是显式传递
            result = []
        if way is None:  # 这样可以防止way在函数调用之间意外共享，而不是显式传递
            way = []
        if searched is None:  # 这样可以防止searched在函数调用之间意外共享，而不是显式传递
            searched = []
        adjacencyList = self.adjacencyList
        search_queue = adjacencyList[initial]  # 当前位置的临近点
        searched.append(initial)  # searched 用于记录已搜索的点
        for node in search_queue:
            way.append(node)  # 记录定点到当前位置所经过的路径
            if node in searched:
                way.pop()
                continue
            elif node == destination:
                result.append(copy.deepcopy(way))
            elif adjacencyList[node]:
                self.dfs(node, destination, searched, way, result)
            else:
                way.pop()
                return result
            way.pop()
        return result

    def dfs(self, initial, destination, searched=None, way=None, result=None):
        '''
        深度优先搜索,用于找到所有的路径
        邻接表有问题会导致搜索结构出错
        :param initial:
        :param destination:
        :param searched:
        :param way:
        :param result:
        :return:
        '''
        if searched is None:
            searched = []
        if way is None:
            way = deque()
        if result is None:
            result = defaultdict(list)

        search_queue = self.adjacencyList[initial]  # 当前位置的临近点

        searched.append(initial)  # searched 用于记录已搜索的点

        for node in search_queue:
            way.append(node)  # 记录定点到当前位置所经过的路径
            if node in searched:
                way.pop()
                continue
            elif node == destination:
                result[initial] = list(way)
            elif self.adjacencyList[node]:
                self.dfs(node, destination, searched[:], way, result)
            way.pop()

        return dict(result)

    def get_road_sign_old(self, initial, destination):
        """
        由dfs()方法生成的路线，选取最短路径，返回路径跳转元素的list
        :param initial: 起点
        :param destination: 终点
        :return: list
        """
        all_road = self.dfs(initial, destination)
        all_road_len = []
        if len(all_road) == 1:
            road = [initial] + self.dfs(initial, destination)[0]
        else:
            for i in range(len(all_road)):
                all_road_len.append(len(all_road[i]))
            shortest = all_road_len.index(min(all_road_len))
            road = [initial] + all_road[shortest]
        # print(road)
        result = list()
        for i in range(len(road) - 1):
            c1 = road[i]
            c2 = road[i + 1]
            # print(c1,c2)
            for v in self.listVex:
                if v.pageName == c1:
                    result += v.neighbor[c2]
        return result

    def get_road_sign(self, initial, destination):
        """
        由dfs()方法生成的路线，选取最短路径，返回路径跳转元素的list
        :param initial: 起点
        :param destination: 终点
        :return: list
        """
        all_road = self.dfs(initial, destination)
        len_road = [len(x) for x in all_road.values()]
        shortest_idx = min(range(len(len_road)), key=len_road.__getitem__)
        keyList = list(all_road.keys())
        shortest_road = all_road[keyList[shortest_idx]]
        road = [initial] + shortest_road
        # print(road)
        result = []
        for c1, c2 in zip(road[:-1], road[1:]):
            for vertex in self.listVex:
                if vertex.pageName == c1:
                    result += vertex.neighbor[c2]
        return result


if __name__ == "__main__":
    g = LinkedGraph(sheet='universalapp')
    # g = LinkedGraph(sheet='page_element')
    # for frist in g.listVex:

    #     for end in g.listVex:
    #
    #         if frist.pageName != end.pageName:
    #             if not g.dfs(frist.pageName, end.pageName):
    #                 print(frist.pageName, end.pageName)
    #                 print(g.dfs(frist.pageName, end.pageName))
    #                 print("-------------------------------")
    # print(g.dfs('智能', '直播'))
    # print(g.get_road_sign('智能', '设备'))
    # print(g.get_road_sign('设备', '告警'))
    print(g.get_road_sign('智能', '直播'))
