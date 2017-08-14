import io
import requests
from pyamf import remoting
import re
import datetime


def simple_request():
    headers = {
        'Content-Type': 'application/x-amf'
    }
    r = requests.post('http://www.semc.gov.cn/aqi/Gateway.aspx', headers=headers, data=io.open('./requests', 'rb'))
    res = remoting.decode(r.content)
    print '--- updated time----\n'
    rawDate = res.bodies[4][1].body.body
    a = re.sub(r'[^\x00-\x7F]+', r'/', rawDate).replace(' ', '')
    dt = datetime.datetime.strptime(a, '%Y/%m/%d/%H/')
    print dt.strftime('%Y/%m/%d-%H')
    print '-- concentration ---\n'
    for site in res.bodies[0][1].body.body:
        print site

    print '-- realtime ---\n'
    for site in res.bodies[1][1].body.body:
        print site


if __name__ == '__main__':
    simple_request()
