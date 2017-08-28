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
os.chdir(os.path.dirname(sys.argv[0]))
reload(sys)
sys.setdefaultencoding("utf8")


def simple_request():
    headers = {
        'Content-Type': 'application/x-amf'
    }
    r = requests.post('http://www.semc.gov.cn/aqi/Gateway.aspx', headers=headers, data=io.open('./requests', 'rb'))
    res = remoting.decode(r.content)
    # print '--- updated time----\n'
    rawDate = res.bodies[4][1].body.body
    a = re.sub(r'[^\x00-\x7F]+', r'/', rawDate).replace(' ', '')
    dt = datetime.datetime.strptime(a, '%Y/%m/%d/%H/')
    # print dt.strftime('%Y/%m/%d-%H')
    # print '-- 浓度 ---\n'
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    columns=["sitename", "co","pm10","pm101","so2","siteid","no2","pm251",'o3',"pm25"]
    with open("/root/data_collect/"+date+"data.csv","ab") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['--- 更新时间---'.decode('utf8').encode('GBK'),dt.strftime('%Y/%m/%d-%H'),'-- 浓度 ---'.decode('utf8').encode('GBK')])
        # writer.writerow(dt.strftime('%Y/%m/%d-%H'))
        # writer.writerow('-- concentration ---')
        # writer.writerow(columns)
        m =0
        n=0
        for site in res.bodies[0][1].body.body:
            a=[]
            b=[]
            for k,v in site.iteritems():
                a.append(k.decode('utf8').encode('GBK'))
                b.append(v.decode('utf8').encode('GBK'))
            m+=1
            if m ==1 : writer.writerow(a)
            writer.writerow(b)

        # print '-- 实时空气质量指数 ---\n'
        writer.writerow(['-- 实时空气质量指数 ---'.decode('utf8').encode('GBK')])
        for site in res.bodies[1][1].body.body:
            d=[]
            c=[]
            for k,v in site.iteritems():
                # print k,v
                # print type(v)
                c.append(k.decode('utf8').encode('GBK'))
                d.append(v.decode('utf8').encode('GBK'))
            n+=1
            if n ==1 : writer.writerow(c)
            writer.writerow(d)

if __name__ == '__main__':
    simple_request()
