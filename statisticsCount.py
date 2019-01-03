#encoding=utf-8

# 词语统计特征值计算

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import os
import json
import jieba
import jieba.posseg as pseg
import sys
import string
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import textPreprocessing
import fileHandle

# 词语词性值权重分配
pos = {
    'a':  0.5,
    'ad': 0.3,
    'an': 0.6,
    'i':  0.6,
    'j':  0.7,
    'l':  0.6,
    'v':  0.3,
    'vg': 0.2,
    'vd': 0.4,
    'vn': 0.6,
    'n':  0.8
}

# 依据指定词性对于词语进行重新记录
# 返回数据格式:
#   {'word': {loc, pos}, ...}
def wordsStatistics(wordsStatisticsData):
    print ('------当前进行词语词性权重统计操作------')
    # 进行单词词性标注统计
    for key in wordsStatisticsData:
        wordsStatisticsData[key][1] = pos.get(wordsStatisticsData[key][1])
    return wordsStatisticsData


# 对语料库所有文章进行tfidf计算
def tfidf(wordsData):
    #print ('------当前进行词语TF-IDF统计值计算操作------')
    # fileList = getCorpusFilelist()
    # for file in fileList:
    #     print ("Using jieba on " + file)
    #     segFile(file)
    # segFileNameList = getCorpusFilelist('segFile')
    keywordDatas = Tfidf(wordsData)
    return keywordDatas


# 获取指定语料库文件列表


# # 对文档进行分词处理
# def segFile(segFileName, recordPath = 'segFile', filePath = 'corpus'):
#     # 保存分词结果的目录
#     if not os.path.exists(recordPath):
#         os.mkdir(recordPath)
#     # 读取文档
#     segFilePath = os.path.join(filePath, segFileName)
#     fileObj = open(segFilePath, 'r+', encoding='gb18030')
#     fileData = fileObj.read()
#     fileObj.close()
#
#     # 对文档进行分词处理，采用默认模式
#     segFileData = jieba.cut(fileData, cut_all=True)
#
#     # 对空格，换行符进行处理
#     result = []
#     for data in segFileData:
#         data = ''.join(data.split())
#         if (data != '' and data != "\n" and data != "\n\n"):
#             result.append(data)
#
#     # 将分词后的结果用空格隔开，保存至本地。
#     recordFileName = segFileName.strip('.txt') + '_seg.txt'
#     recordFilePath = os.path.join(recordPath, recordFileName)
#     f = open(recordFilePath, "w+")
#     f.write(' '.join(result))
#     f.close()


# 读取已分词好的文档，进行TF-IDF计算
def Tfidf(wordsData):
    keywordDatas = {}
    result = {}
    k = len(wordsData)
    with open('./idf.txt','r',encoding='utf-8')as f:
        dic = []
        for line in f.readlines():
            b = line.strip().split(' ')
            dic.append(b)
    dic = dict(dic)
    for word in wordsData:
        result[word] = wordsData.count(word)
        tf = float(result[word]/k)
        if word in list(dic.keys()):
            idf = float(dic[word])
        else: idf = 8.0
        tf_idf = tf*idf
        keywordDatas[word] = tf_idf
    return keywordDatas



if __name__ == "__main__":
    keywordDatas = tfidf()
    print (keywordDatas)
