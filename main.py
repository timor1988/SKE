#encoding=utf-8

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import sys
import json
import os
import fileHandle
import textPreprocessing
import semanticsCount
import statisticsCount


def main(fileName, path):
    # 逻辑结构
    # 1、文本预处理(分词与词性标注、词语过滤、词语相关信息记录)
    print ('------当前文本预处理操作------')
    wordsStatisticsData, wordsData = textPreprocessing.word_segmentation(fileName, path)
    # 2、词语语义贡献值计算(计算词语语义相似度、构建词语语义相思网络、计算词语居间度密度)
    print ('------当前进行词语语义贡献值计算操作------')
    intermediaryDensity = semanticsCount.intermediaryDegreeDensity(fileName, path)
    # 3、计算词语统计特征值
    keywordDatas = statisticsCount.Tfidf(wordsData)
    print ('------当前进行词语统计特征值计算操作------')
    wordsStatisticsData = statisticsCount.wordsStatistics(wordsStatisticsData)
    print ('------当前进行汇总计算操作------')
    # 4、计算词语关键度
    # 算法基础设定
    # 语义贡献值权重
    vdw = 0.6
    # 统计特征值权重
    tw = 0.4
    # 统计特征位置上权重
    locw1, locw2, locw3 = 0.5, 0.3, 0.3
    # 统计特征词长权重
    lenw = 0.01
    # 统计特征值中词性权重
    posw = 0.5
    # 统计特征中TF-IDF权重
    tfidfw = 0.8

    # 对收集到的词语进行重新遍历
    ske = {}
    for key in wordsStatisticsData.keys():
        # 取语义贡献值(假如居间度密度集合中不存在,补充为0)
        if intermediaryDensity.get(key):
            vdi = intermediaryDensity.get(key)
        else:
            vdi = 0

        # 暂时未加tfidf权值
        score = vdw * vdi + tw * (locw1 * float(wordsStatisticsData[key][0]) + posw * float(
                wordsStatisticsData[key][1]) + tfidfw*keywordDatas[key])
        ske[key] = score

    ske = sorted(ske.items(), key=lambda d: d[1], reverse=True)  # 降序排列
    # print json.dumps(ske, ensure_ascii=False)
    return ske

if __name__ == "__main__":
    # 进行关键词提取的文章
    curPath = fileHandle.get_cur_path()
    curPath = 'corpus/'
    # fileName = '1351409.txt' # bug调试
    fileName = '个人提升职场玛格丽特101.txt'

    print (json.dumps(main(fileName, curPath), ensure_ascii=False))

