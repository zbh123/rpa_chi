#!python3
# -*- coding:utf-8 -*-
import psycopg2
import pandas as pd
import xlwt
import time
import os
import shutil
import psutil


def kill_pid(name):
    process_name = os.path.basename(name)
    print(process_name)
    all_pid = psutil.pids()
    for sub_id in all_pid:
        process = psutil.Process(sub_id)
        if process_name == process.name():
            print('进程已存在, 3s后自动关闭进程')
            time.sleep(3)
            # print(process.terminate())
            # sleep(2)
            # get_pid(name)
            print('taskkill /f /im %s' % process_name)
            os.system('taskkill /f /im %s' % process_name)
            return False
    return True


def export_excel(table_name):
    # 获得连接
    conn = psycopg2.connect(database="portal", user="rpa", password="rpa@123", host="10.29.101.28", port="45432")
    # 获得游标对象
    cursor = conn.cursor()
    # sql语句
    sql = "select * from t_zts_sensitive_person t where t.valid='1'"
    # 执行语句
    cursor.execute(sql)
    # 获取单条数据.
    data = cursor.fetchall()
    # 事物提交
    fileds = [filed[0] for filed in cursor.description]
    print(fileds)
    conn.commit()
    # 关闭数据库连接
    conn.close()
    # for result in data:
    #     print(result)
    book = xlwt.Workbook()  # 创建一个book
    sheet = book.add_sheet('result')  # 创建一个sheet表
    for col, filed in enumerate(fileds):
        sheet.write(0, col, filed)

    row = 1
    for line in data:
        for col, filed in enumerate(line):
            sheet.write(row, col, str(filed).strip())
        row += 1

    book.save('%s' % table_name)


def parse_excel(filename):
    pd.set_option('display.max_rows', None)
    path = os.path.dirname(filename)
    basedir = os.path.dirname(path)
    mould = os.path.join(basedir, '模板.csv')
    data = pd.read_excel(filename, usecols=['user_name', 'ip', 'address'], index=False)
    data = data.loc[data["address"].str.contains("北京启皓大厦中心")==False]
    # data = data.drop[data['address'].str.contains('北京启皓大厦中心').fillna(True)]
    # 根据IP地址去重，保留第一个值
    data.drop_duplicates(subset=['ip'], keep='first', inplace=True)
    data.reset_index(drop=True, inplace=True)
    print(len(data))
    df = data.dropna()
    df.reset_index(drop=True, inplace=True)
    # 将同一人名下的多个IP地址拆分
    flag = 0
    for index, line in enumerate(df['ip']):
        if '/' in line:
            # print(index, line)
            for i, value in enumerate(line.split('/')):
                # print(i)
                print(df['user_name'][index - flag] + str(i))
                df = df.append({'user_name': df['user_name'][index - flag] + str(i), 'ip': value,
                                'address': df['address'][index - flag]}, ignore_index=True)
            df = df.drop(index - flag)
            flag += 1
            df.reset_index(drop=True, inplace=True)
        elif ',' in line:
            # print(index, line)
            for i, value in enumerate(line.split(',')):
                # print(i)
                print(df['user_name'][index - flag] + str(i))
                df = df.append({'user_name': df['user_name'][index - flag] + str(i), 'ip': value,
                                'address': df['address'][index - flag]}, ignore_index=True)
            df = df.drop(index - flag)
            flag += 1
            df.reset_index(drop=True, inplace=True)
        elif '无' in line:
            df = df.drop(index - flag)
            flag += 1
            df.reset_index(drop=True, inplace=True)

    col_name = df.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里
    # print(col_name)
    col_name.insert(1, 'name')
    col_name.insert(2, 'path')
    col_name.insert(3, 'describe')
    col_name.insert(4, 'password')
    col_name.insert(5, 'password_pass')
    col_name.insert(6, 'allow_ip')
    col_name.insert(8, 'mac')
    col_name.insert(9, 'multi')
    col_name.insert(10, 'start')
    col_name.insert(11, 'out_date')
    df = df.reindex(columns=col_name)
    df['name'] = df['user_name']
    df['path'] = ['/IP监控'] * len(df.index)
    df['describe'] = ['认证模块添加'] * len(df.index)
    df['password'] = [''] * len(df.index)
    df['password_pass'] = [''] * len(df.index)
    df['allow_ip'] = [''] * len(df.index)
    df['mac'] = [''] * len(df.index)
    df['multi'] = ['N'] * len(df.index)
    df['start'] = ['Y'] * len(df.index)
    df['out_date'] = [''] * len(df.index)
    # 整理后的文件再次对ip列去重
    df.drop_duplicates(subset=['ip'], keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    data_out = df.loc[df['address'].str.startswith('济南')]
    if len(data_out.index) != 0:
        del data_out['address']
        shutil.copyfile(mould, os.path.join(path, '济南.csv'))
        time.sleep(0.5)
        data_out.to_csv(os.path.join(path, '济南.csv'), mode='a', encoding='gbk', header=False, index=False)

    data_out = df.loc[df['address'].str.startswith('北京')]
    if len(data_out.index) != 0:
        del data_out['address']
        shutil.copyfile(mould, os.path.join(path, '北京.csv'))
        time.sleep(0.5)
        data_out.to_csv(os.path.join(path, '北京.csv'), mode='a', encoding='gbk', header=False, index=False)

    data_out = df.loc[df['address'].str.startswith('深圳')]
    if len(data_out.index) != 0:
        del data_out['address']
        shutil.copyfile(mould, os.path.join(path, '深圳.csv'))
        time.sleep(0.5)
        data_out.to_csv(os.path.join(path, '深圳.csv'), mode='a', encoding='gbk', header=False, index=False)

    data_out = df.loc[df['address'].str.startswith('上海')]
    if len(data_out.index) != 0:
        del data_out['address']
        shutil.copyfile(mould, os.path.join(path, '上海.csv'))
        time.sleep(0.5)
        data_out.to_csv(os.path.join(path, '上海.csv'), mode='a', encoding='gbk', header=False, index=False)


if __name__ == '__main__':
    kill_pid(r'C:\Program Files (x86)\Kingsoft\WPS Office\11.8.2.9022\office6\et.exe')
    path = r'D:\0RPA\合规部\IP地址监控'
    now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
    path = os.path.join(path, now_time)
    if not os.path.exists(path):
        os.mkdir(path)
    file = os.path.join(path, 'IP地址监控.xls')
    if os.path.exists(file):
        os.remove(file)
    export_excel(file)
    parse_excel(file)
