# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : find_pcd.py
@Author  : 王白熊
@Data    ： 2020/12/2 13:49
"""

import os
import struct

def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])


def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

def ReadFile():
    filepath = r'D:\data\biaoding\33.bin'
    binfile = open(filepath, 'rb')  # 打开二进制文件
    size = os.path.getsize(filepath)  # 获得文件大小
    for i in range(size):
        data = binfile.read(1)  # 每次输出一个字节
        data1 = ord(data)
        data2 = chr(data1)
        # data = decode(data)
        print(data)
        print(data1)
        print(data2)
    binfile.close()


if __name__ == '__main__':
    ReadFile()
