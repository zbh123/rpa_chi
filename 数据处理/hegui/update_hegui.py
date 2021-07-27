import cx_Oracle
import os

os.environ["NLS_LANG"] = ".AL32UTF8"
'''
 10.29.128.24:1521/orcl    '10.29.182.15:1521/orcl'
 '''

con = cx_Oracle.connect('hg_jgal', 'hg_jgal!123', '10.29.128.24:1521/qlzcgldb')
cursor = con.cursor()

# cursor.execute('')

# sql = "update HG_JGAL_CJDZGL set WZ='http://www.csrc.gov.cn/pub/ningbo/nbcxxx/' where FWJG=38 and BZ='市场禁入'"
sql = "update HG_JGAL_CJDZGL set CJLX=3 where FWJG=10 and BZ='监管措施'"
# sql = "update HG_JGAL_CJDZGL set CJLX=11 where FWJG=41"
# sql = "update HG_JGAL_CJDZGL set QTZT=0 where FWJG=19 and BZ='证券机构监管-其它'"
# sql = "insert into HG_JGAL_CJDZGL (ID, FWJG,WZ,ZJZXSJ,ZJZXJG,CJLX,QTZT,BZ) VALUES (128, 35, 'http://www.csrc.gov.cn/pub/zjhpublicofxj/index.htm?channel=2280','','','3',1,'监管措施')"

# cursor.execute(sql)

con.commit()
cursor.close()
con.close()
