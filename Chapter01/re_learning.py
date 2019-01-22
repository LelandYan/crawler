# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2019/1/22 22:19'

import re

# re.match
# content = 'Hello 123 4567 World_This is'
#result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}.*',content,re.S)
#print(result.group())
# 输出字符串的长度
#print(result.span())

import requests
import re
from requests.packages import urllib3
urllib3.disable_warnings()
# headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
# content = requests.get("https://book.douban.com/",headers=headers,verify=False).text
# with open("data.txt",'w',encoding='utf-8') as f:
#     f.write(content)
with open('data.txt','r',encoding='utf8') as f:
    content = f.read()
    print(type(content))
    # pattern = re.compile('<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(>*?)</span>.*?</li>',re.S)
    # results = re.findall(pattern,content)
    # for result in results:
    #    print(result)
    pattern = re.compile(
        '<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>',
        re.S)
    results = re.findall(pattern, content)
    for result in results:
        url, name, author, date = result
        author = re.sub('\s', '', author)
        date = re.sub('\s', '', date)
        print(url, name, author, date)