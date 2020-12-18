# -*- coding: utf-8 -*-
"""
@Project : code
@File    : cyh.py
@Author  : 王白熊
@Data    ： 2020/11/27 9:30
"""
import re
import xlwt as xlwt

flag = False  # 是否有满足条件的x
with open('cyh.txt', 'r+', encoding='utf-8') as f_raw:
    line = f_raw.readline()
    f = xlwt.Workbook()
    index = 1
    arr_sheet = f.add_sheet('speed', cell_overwrite_ok=True)
    arr_sheet.write(0, 0, 'delay(ms)')
    arr_sheet.write(0, 1, 'Download(Mbit/s)')
    arr_sheet.write(0, 2, 'Upload(Mbit/s)')
    while line:
        i = -1
        pattern_x = re.compile(r'Download:\s[0-9]+\.[0-9]+')
        pattern_y = re.compile(r'Upload:\s[0-9]+\.[0-9]+')
        pattern_z = re.compile(r'Hosted by China Mobile Group Zhejiang.*')
        x = pattern_x.search(line)
        y = pattern_y.search(line)
        z = pattern_z.search(line)
        # print(x, y)
        if z:
            print(z)
            float_z = float(z.group().split()[-2])
            arr_sheet.write(index, 0, float_z)
        if x:
            print(x)
            float_x = float(x.group().split()[1])
            arr_sheet.write(index, 1, float_x)
        if y:
            print(x)
            float_y = float(y.group().split()[1])
            arr_sheet.write(index, 2, float_y)
            index += 1

        line = f_raw.readline()
    f.save('speed.xls')
