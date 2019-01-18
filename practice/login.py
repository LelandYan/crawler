# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/24 16:36'

from urllib import request
from urllib.parse import *
import lxml.html
from http.cookiejar import *


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


LOGIN_URL = 'http://example.webscraping.com/places/default/user/login'
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
cj = CookieJar()
opener = request.build_opener(request.HTTPCookieProcessor(cj))
html = opener.open(LOGIN_URL).read().decode('utf-8')
data = parse_form(html)
data['email'] = LOGIN_EMAIL
data['password'] = LOGIN_PASSWORD
encoded_data = urlencode(data).encode('utf-8')
req = request.Request(LOGIN_URL, encoded_data)
response = opener.open(req)
s1 = response.geturl()
print(s1)

