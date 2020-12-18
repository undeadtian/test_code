# -*- coding: utf-8 -*-
"""
@Project : code
@File    : cyh.py
@Author  : 王白熊
@Data    ： 2020/11/27 9:30
"""
import re
import xlwt as xlwt

# obstacle number(0)
flag = False  # 是否有满足条件的x
with open('yasuohou.txt', 'r+', encoding='utf-8') as f_raw:
    line = f_raw.readline()
    f = xlwt.Workbook()
    index = 1
    arr_sheet = f.add_sheet('obs_num', cell_overwrite_ok=True)
    arr_sheet.write(0, 0, 'obs_num')
    while line:
        i = -1
        pattern = re.compile(r'obstacle\snumber[(]([0-9]+)[)]')
        x = pattern.search(line)
        if x:
            # print(x)
            int_x = int(x.group().split('(')[1].strip(')'))
            arr_sheet.write(index, 0, int_x)
            index += 1
        line = f_raw.readline()
    f.save('speed.xls')
