# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/24 17:20'

import pprint
from urllib import request
import lxml.html
from http.cookiejar import *
from io import BytesIO
from PIL import Image
import pytesseract


def get_captcha(html):
    print(type(html))
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect('div#recaptcha img')[0].get('src')
    img_data = img_data.partition(',')[-1]
    print(img_data)
    img_data = img_data.encode('utf-8')
    print(img_data)
    binary_img_data = img_data.decode('base64')
    file_like = BytesIO(binary_img_data)
    img = Image.open(file_like)
    return img


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


REGISTER_URL = 'http://example.webscraping.com/places/default/user/register?_next=/places/default/index'
cj = CookieJar()
opener = request.build_opener(request.HTTPCookieProcessor(cj))
html = opener.open(REGISTER_URL).read().decode('utf-8')
# img = get_captcha(html)
# res = pytesseract.image_to_string(img)
# print(res)
form = parse_form(html)
pprint.pprint(form)
