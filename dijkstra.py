#encoding=utf-8

# 文本预处理
# 分词与词性标注
# 词语过滤
# 词语相关信息记录

from __future__ import unicode_literals
import os
import json
import sys
import json
from sys import argv

# 完成距离计算(当前中心点标记值+中心点到此点的权值)
def dijkstra_score(G, shortest_distances, v, w):
    return shortest_distances[v] + G[v][w]


# 此算法完成了从任意指定点startNode到图中任意一点最短距离的计算
def dijkstra(G, startNode):
    print ('------当前进行Dijkstra算法最短路径的计算操作------')
    # 未标记顶点集合
    unprocessed = set(G.keys())  # vertices whose shortest paths from source have not yet been calculated
    # 初始，将起始点移出
    try:
        unprocessed.remove(startNode)
    except:
        raise Exception('invild node!')
    # 已标记的顶点集合
    shortest_distances = {startNode: 0}
    # 进行路径存储
    path = {startNode: startNode}

    # 对所有顶点进行遍历
    for i in range(len(G) - 1):
        # find a vertex with the next shortest path, i.e. minimal Dijkstra score
        # m代表距离，closest_head代表相邻最近的顶点
        length, closest_head = float('inf'), 0

        # 最短路径的记录
        tmpPath = ''

        # 已处理顶点集合中的当前中心点
        for tail in shortest_distances:
            # 以已标记顶点集中点作为起点，遍历查询未标记顶点集中距离最小的点
            for head in G[tail]:
                # 对未标记的顶点集合进行遍历计算
                if head in unprocessed:
                    distance = dijkstra_score(G, shortest_distances, tail, head)
                    if distance < length:
                        length, closest_head = distance, head
                        # 最短路径记录
                        tmpPath = tail + '->' + head
        # 查找到距离已标记顶点集合中的最近的邻接点，并标记记录


        # 会存在
        # 在未标记顶点集中移除
        if closest_head != 0:
            unprocessed.remove(closest_head)
            # 添加新的标记点
            shortest_distances[closest_head] = length
            # 最短路径记录
            flagList = tmpPath.split('->')
            path[closest_head] = path.get(flagList[0]) + '->' + flagList[1]
        else:
            unprocessed.pop()


    # in case G is not fully connected
    for vertex in unprocessed:
        shortest_distances[vertex] = float('inf')

    # 进行合并输出
    shortest_data = {}
    for key in shortest_distances:
        shortest_data[key] = {
            'path': path.get(key),
            'distance': shortest_distances.get(key)
        }

    return shortest_data


if __name__ == '__main__':
    pass