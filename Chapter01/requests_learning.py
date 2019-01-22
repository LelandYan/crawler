# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2019/1/22 20:49'

import requests

# response = requests.get("http://www.baidu.com")
#print(type(response))
#print(response.status_code)
#print(type(response.text))
#print(response.text)
#print(response.cookies)

#response = requests.get("http://httpbin.org/get")
#print(response.text)

# 带参数的get请求
# response = requests.get("http://httpbin.org/get?name=germey&age=22")
# print(response.text)

data = {
    'name':'gemery',
    'age':22
}
# response = requests.get("http://httpbin.org/get",params=data)
# print(response.text)


# 获取json数据
import json
# response = requests.get("http://httpbin.org/get")
# print(type(response.text))
# print(response.json())
# print(json.loads(response.text))
# print(type(response.json()))

# 获取二进制数据
# response = requests.get("https://github.com/favicon.ico")
# with open("favicon.ico",'wb') as f:
#     f.write(response.content)
# header = {
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
# }
# response = requests.get("https://www.zhihu.com/explore",headers=header)
# print(response.text)

# response = requests.post("http://httpbin.org/post",data=data)
# print(response.text)


# response = requests.get("http://www.jianshu.com")
# exit() if not response.status_code == 200 else print("Successful")

# 文件上传
# files = {'file':open('favicon.ico','rb')}
# response = requests.post("http://httpbin.org/post",files=files)
# print(response.text)

# 获取cookie
# response = requests.get("http://www.baidu.com")
# print(response.cookies)
# for key,value in response.cookies.items():
#     print(key + "=" + value)

# 模拟请求
# s = requests.Session()
# s.get("http://httpbin.org/cookies/set/number/123456789")
# response = s.get("http://httpbin.org/cookies")
# print(response.text)

# 证书验证
from requests.packages import urllib3
urllib3.disable_warnings()
response = requests.get("https://www.12306.cn",verify=False)
print(response.status_code)

# 代理设置

from requests.exceptions import  ReadTimeout
# 超时设置
# try:
#     response = requests.get("https://www.12306.cn",verify=False, timeout=0.1)
#     print(response.status_code)
# except Exception:
#     print("timeout")

# 认证
from requests.auth import HTTPBasicAuth
r = requests.get("http://www.baidu.com",auth=HTTPBasicAuth('user','123'))
