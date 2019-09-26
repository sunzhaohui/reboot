# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-09-12 11:18'

import os
import struct

# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少半2字符，长则8字符



# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


# 获取文件大小
def getFileSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)


# 获取文件夹大小
def getDirSize(path):
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return formatSize(sumsize)
    except Exception as err:
        print(err)

def getFileType(path):
    try:
        return path.split('.')[-1]
    except Exception as e:
        print(e)

t = getFileType('/Users/sunzhaohui/PycharmProjects/51reboot/django2.2/reboot/media/orderfiles/1a0e9aedbe55465f9d18802b78b8a901/01-space鸟巢-打印机安装指导-客户20170913.docx')
print(t)



