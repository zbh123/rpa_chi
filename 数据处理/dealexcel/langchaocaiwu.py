import pandas as pd

path = r'D:\0RPA\计划财务部\财务rpa\20210318\1601_经纪客户人民币.xls'
df = pd.read_excel(path, index=False)
col_name = df.columns.tolist()
print(df)

