import pandas as pd
import os
import sys

def parse_excel(path):
    filename = os.path.basename(path).split('.')[0]
    filepath = os.path.dirname(path)
    filename2 = filename + '_轧差.xls'
    path2 = os.path.join(filepath, filename2)
    if os.path.exists(path2):
        os.remove(path2)

    df = pd.read_excel(path, usecols=['核算部门编号', '预计存款利息'], index=False)
    # col_name = df.columns.tolist()
    # print(col_name)
    data = df.groupby('核算部门编号').sum()
    # print(data)
    filename1 = filename + '_解析.xls'
    path1 = os.path.join(filepath, filename1)
    data.to_excel(path1)

    df1 = pd.read_excel(path, index=False)
    df1.drop_duplicates(subset=['核算部门编号'], keep='first', inplace=True)
    df1.reset_index(drop=True, inplace=True)
    # df1.to_excel(path, index=False)
    # df1.reset_index()

    df3 = pd.read_excel(path1, index=False)

    for i, index_2 in enumerate(df1['核算部门编号']):
        for j, index_3 in enumerate(df3['核算部门编号']):
            # print(index_3)
            if index_2 == index_3:
                # print(df3.loc[j, ('预计存款利息')])
                df1.loc[i, ('预计存款利息')] = df3.loc[j, ('预计存款利息')]

    df.reset_index(drop=True, inplace=True)
    df1.to_excel(path2, index=False)

    os.remove(path1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('未输入路径参数')
        os._exists(1)
    path = sys.argv[1]
    if not os.path.isfile(path):
        print('输入参数不是有效文件')
        os._exists(1)
    parse_excel(path)


