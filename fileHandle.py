#encoding=utf-8

# 文件处理相关函数

import os
import sys
import codecs
# 获取指定文件数据
def get_file_data(filename, path):
    try:
        # 进行文章的读取
        filePath = os.path.join(path, filename)
        fileObject = open(filePath, 'r+')
        fileData = fileObject.read()
        return fileData
    except:
        pass
        return ''
    finally:
        pass
        # fileObject.close()

# 获取文件目录
def get_file_list(path):
    filelist = []
    files = os.listdir(path)
    for f in files:
        if (f[0] == '.'):
            pass
        else:
            # filelist.append(os.path.join(path, f))
            filelist.append(f)
    return filelist

# 获取文件指定行(第一行)(默认为当前路径下)
def get_file_line_details(filename, path):
    if not path:
        path = get_cur_path()
    filePath = os.path.join(path, filename)
    file = codecs.open(filePath, 'r', 'utf-8')
    text = file.readline()
    return text

# 获取文件第三行数据
def get_file_third_line_details(filename, path):
    if not path:
        path = get_cur_path()
    filePath = os.path.join(path, filename)
    file = codecs.open(filePath, 'r', 'gb18030')
    count = 1
    while count < 6:
        text = file.readline()
        if count == 3:
            tag1 = text
            print(tag1)
            tag = tag1.strip().split('】')
            tag = tag[1]
            print(tag)
        count += 1
    return tag

# 写文件操作(默认为追加)
def write_file(filename, data, mode = 'a+'):
    curDir = get_cur_path()
    filePath = os.path.join(curDir, filename)
    fileObject = codecs.open(filePath, mode, 'utf-8')
    fileObject.write(str(data))
    fileObject.write('\n\n')
    # fileObject.close()

# 获取当前文件路径
def get_cur_path():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


if __name__ == "__main__":
    pass
    curPath = get_cur_path()
    fileName = 'article.txt'
    fileData = get_file_data(fileName, curPath)
    print (fileData)