import requests
import re
import json
import pymysql
import time
from config import *
import warnings
warnings.filterwarnings('ignore')

url_base = "http://xiaochengxu.58.com/{}/{}" #  city/category
headers = {
    'user-agent': "Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x2607023A) NetType/WIFI Language/zh_CN",
    'host': "xiaochengxu.58.com",
    'connection': "Keep-Alive",
    'accept-encoding': "gzip",
    'charset': "utf-8",
    'cache-control': "no-cache",
    'content-type': 'application/json',
    }

def pick_city():
    try:
        conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS,db='info_data')
        cur = conn.cursor()
        cur.execute('select * from code58 order by querytime  limit 1;')
        res = cur.fetchall()[0]
        cur.execute('update code58 set querytime={} where code="{}";'.format(int(time.time()),res[2]))
        conn.commit()
        return res
    except Exception as e:
        print(e)
        return ()
    finally:
        conn.close()
        
def pick_info_page(infoid=-1,status=1):
    try:
        conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS,db='info_data')
        cur = conn.cursor()
        if infoid==-1:
            cur.execute('select distinct infoid,userid from page58 where finish=0 limit 1;')
            res = cur.fetchall()[0]
            # print(res)
            return res
        else:
            cur.execute('update page58 set finish={} where infoid="{}";'.format(status,infoid))
            conn.commit()
            return True
    except Exception as e:
        print(e)
        return ()
    finally:
        conn.close()

def insert_info_page(info):
    if len(info)==0:
        print('页面读取错误')
        return 0
    try:
        conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS,db='info_data')
        cur = conn.cursor()
        cur.executemany('insert ignore into page58 (infoid,userid) values (%s,%s);',info)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        
def clear_info_page():
    try:
        conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS,db='info_data')
        cur = conn.cursor()
        cur.execute('delete from page58 where finish<1')
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        
def get_info_page(page=1):
    try:
        response = requests.request("GET", url, headers=headers, params={"page":page})#, allow_redirects=False)
        if response.status_code != requests.codes.OK:
            print ('获取信息页失败: %u' % resp.status_code)
            return []
    #     print(response.text)
        ret = re.findall('"infoId":(\d*),"userId":(\d*)',response.text)
        if len(ret) == 0:
            print('可能需要验证码,延时10s')
            time.sleep(10)
            return []        
    #     print(ret)
        return ret
    except Exception as e:
        print(e)
        return 0    
    
def get_detail_page(info=''):
    try:
        response = requests.request("GET", url+'/{}x.shtml'.format(info), headers=headers)#, allow_redirects=False)
        if response.status_code != requests.codes.OK:
            print ('获取详情页失败: %u' % resp.status_code)
            return []
    #     print(response.text)
        ret = json.loads(response.text)
    except Exception as e:
        print(e)
        return []    
    try:
        infoTitle = ret['infoTitle']
        shopcellphone = str(ret['shop']['shopcellphone'])
        goblianxiren = ret['goblianxiren']
    except Exception as e:
        print('可能需要验证码,延时10s')
        time.sleep(10)
        return []
    try:
        enterpriseName = ret['qiyeEntity']['enterpriseName']
    except Exception as e:
        enterpriseName = 'No EnterpriseName'
    try:
        enterpriseAddress = ret['qiyeEntity']['extendMap']['enterpriseAddress']
    except Exception as e:
        enterpriseAddress = 'No EnterpriseAddress'      
    
    return [goblianxiren,shopcellphone,enterpriseName,infoTitle]
#     return '\t'.join([infoTitle,enterpriseName,shopcellphone,goblianxiren,enterpriseAddress])

def sql_execute(sql=''):
    try:
        conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS,db='info_data')
        cur = conn.cursor()
        ret = cur.execute(sql)
        conn.commit()
        return ret
    except Exception as e:
        print(e)
        return -1
    finally:
        conn.close()

cityret=()
while len(cityret)==0:
    cityret=pick_city()

for k,v in FENLEI_58.items():
    url = url_base.format(cityret[2],k)
    for i in range(FENLEI_PAGE_READ):
        clear_info_page()
        print('正在读取{}-{}，分类{}，第{}页'.format(cityret[0],cityret[1],v,i))
        res = get_info_page(i)
        insert_info_page(res)
        for j in range(len(res)):
            page = pick_info_page()
            if len(page)==0:
                break
            print('读取详情页{}...'.format(page[0]))
            pageret =get_detail_page(page[0])
            if len(pageret)>0:
                pick_info_page(page[0])
            else:
                pick_info_page(page[0],-1)
                continue
            sql = '''insert ignore into info58 (name,phone,enterpriseName,infoTitle,province,city,category,userid) values ("{}","{}","{}","{}","{}","{}","{}",{})'''.format(*pageret,cityret[0],cityret[1],v,page[1])
            print(sql.split('values')[1])    
            if len(pageret[1])==1:
                continue
            sql_execute(sql)