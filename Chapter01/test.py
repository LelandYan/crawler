# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2019/1/22 16:29'

import urllib.parse
import urllib.request
import re
import requests
import selenium
from selenium import webdriver

# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode("utf-8"))
# data = bytes(urllib.parse.urlencode({"word":"hello"}),encoding='utf8')
# response = urllib.request.urlopen("http://httpbin.org/post",data=data)
from urllib import request, parse
url = 'http://httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'httpbin.org'
}
dict = {
    'name': 'Germey'
}
data = bytes(parse.urlencode(dict), encoding='utf8')
req = request.Request(url=url, data=data, headers=headers, method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))


# print(requests.get("http://www.baidu.com"))
# drive = webdriver.PhantomJS()
# drive.get("http://www.baidu.com")
# print(drive.page_source)