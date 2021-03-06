# coding=utf-8
import io
import requests
from pyamf import remoting
import re
import datetime
import csv
import sys
import commands
import json
import os,sys
reload(sys)
sys.setdefaultencoding("utf8")

def simple_request():
    headers = {
        'Content-Type': 'application/x-amf'
    }
    r = requests.post('http://www.semc.gov.cn/aqi/Gateway.aspx', headers=headers, data=io.open('/root/data_collect/requests', 'rb'))
    res = remoting.decode(r.content)
    # print '--- updated time----\n'
    rawDate = res.bodies[4][1].body.body
    a = re.sub(r'[^\x00-\x7F]+', r'/', rawDate).replace(' ', '')
    dt = datetime.datetime.strptime(a, '%Y/%m/%d/%H/')
    time = dt.strftime('%Y/%m/%d %H')
    # print dt.strftime('%Y/%m/%d-%H')
    # print '-- 浓度 ---\n'
    date = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime('%Y-%m-%d')
    #date = datetime.datetime.now().strftime('%Y-%m-%d')
    # date =datetime.datetime.strptime(a, '%Y-%m-%d')
    columns=["sitename", "co","siteid","no2","pm25"]
    # columns=["sitename", "co","pm10","pm101","so2","siteid","no2","pm251",'o3',"pm25"]
    with open("/root/data_collect/his_data/"+date+"new_data.csv","ab") as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(['--- 更新时间---'.decode('utf8').encode('GBK'),dt.strftime('%Y/%m/%d-%H'),'-- 浓度 ---'.decode('utf8').encode('GBK')])
        m =0
        n=0
        for site in res.bodies[0][1].body.body:
            a=["time"]
            b=[time]
            for k,v in site.iteritems():
                if str(k) not in columns:continue
                a.append(k.decode('utf8').encode('GBK'))
                b.append(v.decode('utf8').encode('GBK'))
            m+=1
            if m ==1 : writer.writerow(a)
            writer.writerow(b)

if __name__ == '__main__':
    simple_request()
