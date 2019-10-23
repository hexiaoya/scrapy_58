import pymysql
import requests
import re
import json
from config import *
import warnings
warnings.filterwarnings('ignore')

conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS)

try:
    # 初始化数据库
    cur = conn.cursor()
    cur.execute('''CREATE DATABASE IF NOT EXISTS `info_data`;''')

    sql = '''CREATE TABLE `info_data`.`code58`  (
      `province` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `city` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `code` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
      `querytime` int(32) NULL DEFAULT NULL
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;'''
    cur.execute('''DROP TABLE IF EXISTS `info_data`.`code58`;''')
    cur.execute(sql)

    sql='''CREATE TABLE `info_data`.`info58`  (
      `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `phone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `province` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `city` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `category` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `enterpriseName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `infoTitle` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `userid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
      PRIMARY KEY (`userid`) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;'''
    cur.execute('''DROP TABLE IF EXISTS `info_data`.`info58`;''')
    cur.execute(sql)

    sql='''CREATE TABLE `info_data`.`page58`  (
      `infoid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
      `userid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
      `finish` int(32) NULL DEFAULT 0,
      PRIMARY KEY (`infoid`) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;'''
    cur.execute('''DROP TABLE IF EXISTS `info_data`.`page58`;''')
    cur.execute(sql)

    # 获取全部城市
    resp = requests.get('https://www.58.com/changecity.html')
    respstr = resp.text.replace('\n','').replace(' ','')

    citys = re.findall('independentCityList=({.*?})',respstr)
    if len(citys)==0:
        print('获取城市出错')
        exit(0)
    citys = citys[0]
    citys = json.loads(citys)
    citys1 = [ (k,k,v.split('|')[0],0) for k,v in citys.items()]

    citys = re.findall('cityList=({.*})</script>',respstr)
    if len(citys)==0:
        print('获取城市出错')
        exit(0)
    citys = citys[0]
    citys = json.loads(citys)
    citys.pop('其他')
    citys.pop('海外')
    citys2 = [ (k,ik,iv.split('|')[0],0)  for k,v in citys.items() for ik,iv in v.items()]

    citys = citys1+citys2
    # print(citys)
    sql='insert into `info_data`.`code58` (province,city,code,querytime) values (%s,%s,%s,%s)'
    cur.executemany(sql,citys)
    conn.commit()

    cur.execute('''select * from `info_data`.`code58`;''')
    res = cur.fetchall()
    if len(res) == len(citys):
        print('数据库初始化成功，{}个城市加入数据库中'.format(len(citys)))
    else:
        print('数据库初始化失败，请尝试重新运行脚本')
except Exception as e:
    print(e)
    print('数据库初始化失败，请尝试重新运行脚本')
finally:
    conn.close()