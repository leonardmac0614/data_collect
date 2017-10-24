# coding=utf-8
import datetime
import csv
import sys
import commands
import json
import os,sys
reload(sys)
sys.setdefaultencoding("utf8")

def read_csv():

    date = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    file_name = "/root/data_collect/his_data/"+str(date)+ "new_data.csv"
    columns=["time","sitename", "co","siteid","no2","pm25"]
    with open(file_name,'rb') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
    siteid= [201,209,185,203,215,183,207,193,195,228,0]

    with open("/root/data_collect/his_data/"+date+"filter_data.csv","ab") as csvfile:
        writer = csv.writer(csvfile)

        for j in siteid:
            writer.writerow(columns)
            for i in rows:
                if i[3]==str(j):
                    writer.writerow(i)


if __name__ == '__main__':
    read_csv()

