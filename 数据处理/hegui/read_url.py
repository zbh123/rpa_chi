#!python3
# -*- coding:utf-8 -*-

import cx_Oracle
import os
import xlwt, time

os.environ["NLS_LANG"] = ".AL32UTF8"


def read_url(file):
    '''
    10.29.128.24:1521/orcl    '10.29.182.15:1521/orcl'    hg_jgal        hg_jgal!123
    '''
    con = cx_Oracle.connect('hg_jgal', 'hg_jgal!123', '10.29.128.24:1521/qlzcgldb')
    cursor = con.cursor()

    sql = 'select * from HG_JGAL_CJDZGL'
    # sql = 'select * from HG_JGAL_JGJGAL'

    cursor.execute(sql)
    data1 = cursor.fetchall()
    # print(data1)
    for line in data1:
        print(line)
    fileds = [filed[0] for filed in cursor.description]
    print(fileds)
    cursor.close()

    con.close()
    # 事物提交

    book = xlwt.Workbook()  # 创建一个book
    sheet = book.add_sheet('result')  # 创建一个sheet表
    for col, filed in enumerate(fileds):
        sheet.write(0, col, filed)

    row = 1
    for line in data1:
        for col, filed in enumerate(line):
            sheet.write(row, col, str(filed).strip())
        row += 1
    book.save(file)


path = r'D:\0RPA\合规部\监管案例'
now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
path = os.path.join(path, now_time)
if not os.path.exists(path):
    os.mkdir(path)
file = os.path.join(path, '监管案例url.xls')
if os.path.exists(file):
    os.remove(file)
read_url(file)
