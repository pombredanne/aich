# coding:utf8


import urllib.request
import os
import time
import datetime
import jieba
import requests
from lxml import etree
import re
 

start = time.clock()

print("                                        程序启动成功,3秒后开始采集   ")
print("\r")
print("\r")
print("\r")
time.sleep(3)
import json
print(" 正在读取分词库...........")
# dededata = xlrd.open_workbook('dededic.xlsx')
# dedetable = dededata.sheets()[0]
# dederesult= dedetable.col_values(1)
print(" Success！")

lt = [1, 2, 3, 4, 5, 6]
def add(num):
    return num + 1
rs = list(map(add, lt))
print (rs)

print("\r")
print(" 正在获取采集URl......")
def ht(url='',words=''):
    s = requests.session()
    s.headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"
    if url=='':
        url = "http://www.120ask.com/list/"
    query = url+words
    search_result=s.get(query)
    search_html = search_result.content
    html_obj = etree.HTML(search_html)
    return html_obj

html_obj=ht()
fenleiList=html_obj.xpath("/html/body/div[*]/div[*]/div/div[*]/div/div/div[*]/div[*]/div[*]/p/a")
fenleiItems=[]
for fenlei in fenleiList:
    ur=fenlei.attrib.get('href','')
    if 'http' in ur:
        fenleiItems.append(ur)

def per_page(base_ual):
    for pa in range(1, 10000):
        url = base_ual+'over/'
        url1 = url + '{}/'.format(pa)
        print(url1)
        html_obj = ht(url1)
        per_list = html_obj.xpath("//*[@id='list']/div[1]/div[3]/ul/li[*]/div[1]/p/a")
        questions = []
        print(url1)
        for per in per_list:
            ur = per.attrib.get('href', '')
            if 'http' in ur:
                questions.append(ur)

        result=[]
        for q in questions:
            try:
                html_obj = ht(q)
                title = html_obj.xpath("//*[@id='d_askH1']//text()")[0].strip().replace('\n', '')
                try:
                    detail = html_obj.xpath("/html/body/div[1]/div[5]/div[2]/div[3]/div[2]/p[1]//text()")
                    ans = []
                    for h in html_obj.xpath("/html/body/div[1]/div[5]/div[2]/div[3]/div[2]/p[1]//text()"):
                        h = str(h)
                        try:
                            if len(re.search('[\u4e00 -\u9fa5]+', str(h).strip()).group(0)) > 2:
                                if '描述' not in str(h) and 'ask' not in str(h) and ':' not in str(h):
                                    ans.append(str(h).strip())
                        except:
                            pass
                    detail = ' '.join(ans)
                except Exception as e:
                    detail = ''
                    print(e, pa)
                # answer=str()
                # answer =answer.split('意见：')[1].strip().replace('\n','')
                ans = []
                for h in html_obj.xpath("/html/body/div[1]/div[5]/div[2]/div[7]/div[1]/div[2]/div[2]//text()"):
                    h = str(h)
                    try:
                        if len(re.search('[\u4e00 -\u9fa5]+', str(h).strip()).group(0)) > 2:
                            if '我要投诉' not in str(h) and '医生回答' not in str(h) and '意见' not in str(h) and 'ask' not in str(
                                    h) and '病情分析' not in str(h) and ':' not in str(h):
                                ans.append(str(h).strip())
                    except:
                        pass
                answer = ' '.join(ans)
                d={'title':title,
                 'detail':detail,
                    'answer':answer

                }
                l = json.dumps(d, ensure_ascii=False)
                result.append(l)

            except Exception as e:
                print(e)

        with open('../input/{}'.format(base_ual.replace('/','_')), 'a', encoding='utf8') as f:
            for r in result:
                f.writelines(r+ '\n')
    return 'gg'
def all_class():
    fg=[]
    import multiprocessing
    p = multiprocessing.Pool(30)
    for i in  range(0,len(fenleiItems)):



        p.apply_async(per_page, args=(fenleiItems[i],))
        if (i + 1) % 30== 0:
            p.close()
            p.join()



    print( 'Waiting for all subprocesses done...')


all_class()

