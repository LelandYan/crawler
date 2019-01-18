# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/24 18:45'
from urllib import request
from http.cookiejar import *
from io import BytesIO
import lxml.html
from PIL import Image
from urllib.parse import urlencode
import pytesseract
import string
import base64

REGISTER_URL = 'http://example.webscraping.com/places/default/user/register?_next=/places/default/index'


def extract_image(html):
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect('div#recaptcha img')[0].get('src')
    img_data = img_data.partition(',')[-1]
    binary_img_data = base64.b64decode(img_data)
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


def register(first_name, last_name, email, password, captcha_fn):
    cj = CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    html = opener.open(REGISTER_URL).read().decode('utf-8')
    form = parse_form(html)
    print(form)
    form['first_name'] = first_name
    form['last_name'] = last_name
    form['email'] = email
    form['password'] = form['password_two'] = password
    img = extract_image(html)
    captcha = captcha_fn(img)
    form['recaptcha_response_field'] = captcha
    print(form)
    encoded_data = urlencode(form).encode('utf-8')
    req = request.Request(REGISTER_URL, encoded_data)
    response = opener.open(req)
    print(response.geturl())
    success = '/user/register' not in response.geturl()
    print(success)
    return success


def ocr(img):
    # threshold the image to ignore background and keep text
    gray = img.convert('L')
    # gray.save('captcha_greyscale.png')
    bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    # bw.save('captcha_threshold.png')
    word = pytesseract.image_to_string(bw)
    ascii_word = ''.join(c for c in word if c in string.ascii_letters).lower()
    return ascii_word


if __name__ == '__main__':
    result = register('Test Account', 'Test Account', 'eampl@webscrping.com', 'example', ocr)
    print(result)

