from collections import Counter
wordsData = ['a','b','a']
result = {}
for word in wordsData:
    result[word] = wordsData.count(word)
    tf = float(result[word] / k)
    if word in list(dic.keys()):
        idf = float(dic[word])
    else:
        idf = 8.0
    tf_idf = tf * idf
    keywordDatas[word] = tf_idf