#encoding=utf-8

# 文本预处理
# 分词与词性标注
# 词语过滤
# 词语相关信息记录

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import os
import json
import sys
# 操作中文必须语句，解决字符问题
import jieba
import jieba.posseg as pseg

# 加载分词字典
jieba.set_dictionary("dict_file/dict.txt.big")
# 加载用户自定义词典
jieba.load_userdict("dict_file/user_dict.txt")

# 加载自定义模块
import fileHandle

# 词性过滤文件(保留形容词、副形词、名形词、成语、简称略语、习用语、动词、动语素、副动词、名动词、名词)
ALLOW_SPEECH_TAGS = ['a', 'ad', 'an', 'i', 'j', 'l', 'v', 'vg', 'vd', 'vn', 'n']

# 词语位置
Word_Location = {'title': 1, 'section-start': 2, 'section-end':3, 'content': 4}

# 分词&词性标注
# 去除停用词
# 保留指定词性词语
def word_segmentation(fileName, path):
    print ('------当前进行分词&词性标注&去重停用词&保留指定词性词语操作------')
    # 加载停用词文件
    # jieba.analyse.set_stop_words('dict_file/stop_words.txt')
    stopWords = [line.strip()for line in open('dict_file/stop_words.txt',encoding='utf-8').readlines()]

    # 获取文件数据
    fileData = fileHandle.get_file_data(fileName, path)
    # jieba分词&词性标注
    psegDataList = pseg.cut(fileData)

    # 词语集合
    wordsData = []
    # 词语统计数据
    wordsStatisticsData= {}
    # 获取文章的标题信息
    title = fileHandle.get_file_third_line_details(fileName, path)
    # 词性过滤&停用词过滤
    for data in psegDataList:
        # 添加单词长度限制(至少为2)
        if data.flag in set(ALLOW_SPEECH_TAGS) and data.word not in stopWords and len(data.word) > 1:
            wordsData.append(data.word)
            # 进行词语位置&词性记录（此处还需补充段首,段尾）
            if data.word in title:
                wordDetail = [1, str(data.flag)]
            else:
                wordDetail = [0, str(data.flag)]
            # print data.word, data.flag
            wordsStatisticsData[data.word] = wordDetail
    #print(wordsStatisticsData)
    # 对词语集合进行去重
    wordsData = list(set(wordsData))
    return wordsStatisticsData, wordsData

if __name__ == "__main__":
    pass
    curPath = fileHandle.get_cur_path()
    fileName = 'article2.txt'
    wordsStatisticsData, wordsData = word_segmentation(fileName, curPath)

    # 进行词语位置的查找测试
    # print json.dumps(wordsStatisticsData, ensure_ascii=False)
    print(json.dumps(wordsData, ensure_ascii=False))

    # # 词语位置和词语词性
    # data = {'我': [], '你': {}}