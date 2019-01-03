#encoding=utf-8

# 文本预处理
# 分词与词性标注
# 词语过滤
# 词语相关信息记录

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
# 除法运算
from __future__ import division
import os
import json
import sys
# 操作中文必须语句，解决字符问题

import fileHandle
import textPreprocessing
import dijkstra

# 词语语义贡献值计算
# 计算词语语义相似度
# 构建词语语义相似度网络
# 计算词语居间度密度


# 《同义词词林》的读入
# 返回格式{code: '文字字符串', }
def cilin():
    print ('------当前进行《同义词词林》的读入操作------')
    cilinFilePath = 'dict_file/cilin.txt'
    cilinFileObject = open(cilinFilePath, 'r', encoding='utf-8')  # 进行分词文件的读取
    cilinDatas = {}
    for line in cilinFileObject:
        word = line.strip('\n')  # 去除换行符
        cilinDatas[word[0:8]] = word[9:]
    return cilinDatas

# 变量存储
cilinCodeDatas = cilin()

# 指定词语编码
def wordEncoding(word ,data = cilinCodeDatas):
    print ('------当前进行指定词语编码操作------')
    if data:
        cilinDatas = data
    else:
        cilinDatas = cilin()
    wordEncodingDatas = []
    # 新词检测标记(新词为False,否则为True)
    flag = False
    wordNewEncodingDatas = []
    for k, v in cilinDatas.items():
        # 此处对于《同义词词林》中不存在的单词进行了过滤
        # 对于自定义词库中的标签进行操作
        # 对于新词(存在于自定义标签库中)的处理：将所有编码均赋予它，这样其与其他单词的语义相似度均为1，不会影响其产生
        wordNewEncodingDatas.append(k)
        if str(word) in v:
            flag = True
            wordEncodingDatas.append(k)
    return wordEncodingDatas
    # if flag:
    #     return wordEncodingDatas
    # else:
        # 对于是否存在于自定义标签库中，进行检测
        # userdictFilePath = 'dict_file/user_dict.txt'
        # userdictFileObject = open(userdictFilePath, 'r')  # 进行分词文件的读取
        # 存在True，否则为False
        # tagFlag = False
        # for line in userdictFileObject:
        #     data = line.strip('\n')  # 去除换行符
        #     if str(word) in data:
        #         tagFlag = True
        #         break
        # if tagFlag:
        #     return wordNewEncodingDatas
        # else:
        #     return wordEncodingDatas


# 进行词语间语义相似度计算
def wordSemanticSimilarity(word1, word2, wordsEncodingData):
    print ('------当前进行词语间语义相似度计算操作------')
    # 获取单词的编码
    word1EncodingDatas = wordsEncodingData.get(word1)
    word2EncodingDatas = wordsEncodingData.get(word2)
    # 应对分词不存在于《同义词词林》中的情况
    if len(word1EncodingDatas) == 0 or len(word2EncodingDatas) == 0:
        return 0
    # 自定义初始距离值
    init_dis = 10
    # 权重数组
    weights = [1.0, 0.5, 0.25, 0.125, 0.06, 0.03]
    # 进行语义距离计算
    disData = []
    for code1 in word1EncodingDatas:
        for code2 in word2EncodingDatas:
            if code1.find(code2) == 0 and code1[-1] == '#':
                tmpDis = weights[5] * init_dis
            elif code1.find(code2) == 0 and code1[-1] != '#':
                tmpDis = 0
            else:
                # 判断从第i层开始不同
                hierarchy = codeCmp(code1, code2)
                tmpDis = weights[hierarchy - 1] * init_dis
            disData.append(tmpDis)
    # 获取其中最小值
    disData.sort()
    # 计算语义相似度(参数a = 5)
    sim = 5 / (5 + disData[0])
    return sim


# 判断两个等长字符串从第几位开始不同，并按照编码规则输出对应的层级
def codeCmp(code1, code2):
    if len(code1) != len(code2):
        raise Exception("Not the same length!")
    flag = 0
    for i in range(len(code1) + 1):
        if code1[0:i] != code2[0:i]:
            flag = i
            break
        flag += 1

    # 进行层级判断(按照哈工大扩展版编码规则表实现)
    if flag == 1 or flag == 2:
        hierarchy = flag
    if flag == 3 or flag == 4:
        hierarchy = 3
    if flag == 5:
        hierarchy = 4
    if flag == 6 or flag == 7:
        hierarchy = 5
    if flag == 8:
        hierarchy = 6
    if flag == 9:
        hierarchy = 0
    return hierarchy


# 语义相似度网络
# 返回形式{
#   "词1": {"词2": "词1和词2的语义相似度", "词3": "词1和词3的语义相似度",...}
#   "词2": {"词1": "词2和词1的语义相似度", "词3": "词2和词3的语义相似度",...}
# }
def wordSemanticSimilarityGraph(fileName, path):
    print ('------当前进行语义相似度网络构建操作------')
    # 图G的顶点集合
    wordsStatisticsData, wordsData = textPreprocessing.word_segmentation(fileName, path)
    # 词语编码的统计
    wordsEncodingData = {}
    for word in wordsData:
        code = wordEncoding(word)
        wordsEncodingData[word] = code
    # 语义相似度阈值
    b = 0.66
    graphDatas = {}
    for startWord in wordsData:
        graphData = {}
        for endWord in wordsData:
            # 若两个单词不同,则计算其语义相似度，大于指定阈值，则生成边
            if startWord != endWord:
                # 计算语义相似度
                sim = wordSemanticSimilarity(startWord, endWord, wordsEncodingData)
                if sim > b:
                    graphData[endWord] = sim
        if graphData:
            graphDatas[startWord] = graphData
    return graphDatas


# 居间度集合
def intermediaryDegreeInterval(fileName, path):
    print ('------当前进行词语居间度集合构建操作------')
    # 获取语义相似度网络图
    graphDatas = wordSemanticSimilarityGraph(fileName, path)

    # 获取最短路径数据集合
    shortestDatas = {}
    for key in graphDatas.keys():
        shortestData = dijkstra.dijkstra(graphDatas, key)
        shortestDatas[key] = shortestData # 三重字典。

    # 构建居间度集合
    interval = {}
    for key in graphDatas.keys():
        score = intermediaryDegreeScore(key, shortestDatas)
        interval[key] = score

    return interval


# 计算指定顶点的居间度
# 传入参数：指定顶点，最短路径信息
def intermediaryDegreeScore(word, shortestDatas):
    print ('------当前进行指定顶点居间度计算操作------')
    Score = 0
    for m in shortestDatas.keys():
        for k in shortestDatas.keys():
            if m == k:
                pass
            else:
                # 计算两个顶点间的最短路径数(此处可能有歧义)
                try:
                    path = shortestDatas[m][k]['path']
                    # 此处有两种处理逻辑，一种是利用距离，一种是利用路径数
                    # 暂时使用路径数
                    routes = path.split('->')  # 至少为2
                    routesNum = len(routes)
                    distances = shortestDatas[m][k]['distance']
                    if word in path:
                        # 使用路径数
                        score = 1 / (routesNum - 1)
                        # 使用路径距离
                        # score = 1 / distances
                    else:
                        score = 0
                    Score += score
                except:
                    Score = 0
    return Score


# 计算居间度密度
def intermediaryDegreeDensity(fileName, path):
    print ('------当前进行居间度密度集合构建操作------')
    # 顶点集合V对应的居间度集合bc
    interval = intermediaryDegreeInterval(fileName, path)

    # 顶点个数
    wordCount = len(interval)
    # 基础控制参数配置
    # bc的区间划分个数
    s = 10
    # 区间个数增长的速度参数
    c = 5
    # 区间密度阈值
    d = 0.8
    # 对bc进行重新划分的最大次数
    max = 6

    # 对字典按照键值进行排序(降序)
    sortedInterval = sorted(interval.items(), key=lambda asd: asd[1], reverse=True)
    # 获取当前居间度密度最大值
    maxratio, intervalDensity = refinementBC(sortedInterval, s)

    # 设定循环次数
    loop = 1
    while maxratio >= d and loop < max:
        s = s * c
        maxratio, intervalDensity = refinementBC(sortedInterval, s)
        loop += 1

    # 根据获取到的居间度密度集合进行相应的单词的居间度密度集合更新

    # 居间度密度集合
    intermediaryDensity = {}
    for key in intervalDensity:
        wordData = intervalDensity[key]
        wordList = wordData.split(',')
        wordNum = len(wordList)
        for word in wordList:
            intermediaryDensity[word] = wordNum / wordCount

    return intermediaryDensity


# 最优区间划分细度(降序排列的居间度集合)
# 计算最大居间度密度
# 参数:按居间度降序排列的居间度集合sortedInterval,区间划分个数s
def refinementBC(sortedInterval, s):
    # 顶点个数
    wordCount = len(sortedInterval)
    # 居间度最大值&最小值
    maxIntermediaryDegree = sortedInterval[0][1]
    minIntermediaryDegree = sortedInterval[wordCount - 1][1]
    # print maxIntermediaryDegree, minIntermediaryDegree
    # 居间度划分区间长度
    intervalScore = (maxIntermediaryDegree - minIntermediaryDegree) / s

    # 居间度密度数组
    intervalDensity = {}

    tmpNode = minIntermediaryDegree
    # 按照居间度平均划分到不同的区间内，区间键为int，键值为单词(中间使用,连接)
    for key in sortedInterval:
        flag = int((key[1] - minIntermediaryDegree) / intervalScore)
        if flag in intervalDensity:
            intervalDensity[flag] = intervalDensity.get(flag) + ',' + key[0]
        else:
            intervalDensity[flag] = key[0]

    # 首次对区间度集合进行检测,输出当前最大的居间度密度作为比较
    maxratio = 0
    for key in intervalDensity:
        wordData = intervalDensity.get(key)
        wordList = wordData.split(',')
        wordNum = len(wordList)
        if maxratio < (wordNum / wordCount):
            maxratio = (wordNum / wordCount)
    return maxratio, intervalDensity



if __name__ == "__main__":
    pass

    curPath = fileHandle.get_cur_path()
    fileName = 'article2.txt'

    # 返回单词居间度密度集合
    intermediaryDensity = intermediaryDegreeDensity(fileName, curPath)
    print (json.dumps(intermediaryDensity, ensure_ascii=False))

