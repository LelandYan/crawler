import requests
from bs4 import BeautifulSoup
import os


def getImages(url, path):
    response = requests.get(url=url)
    response.encoding = response.apparent_encoding
    b1 = BeautifulSoup(response.text, 'html.parser')
    a = b1.find_all('img', attrs={'data-s': "300,640"})
    num = 1
    for imgs in a:
        url = imgs.get('data-src')
        image = requests.get(url=url)
        path = path + '\\'
        cnt = str(num) + '.jpg'
        with open(path+cnt, 'wb') as f:
            f.write(image.content)
        num += 1


def images(args):
    url_list = args
    n = 1
    for url in url_list:
        path = os.getcwd()
        path = path + '\\数学竞赛' + str(n)
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        getImages(url, path)
        n += 1


if __name__ == '__main__':
    url_list = [
        'https://mp.weixin.qq.com/s?__biz=MzI2OTE2NzczNQ==&mid=2649967186&idx=1&sn=89c94df331ddc40f188c0d377e69b962&scene=4#wechat_redirect',
        'https://mp.weixin.qq.com/s?__biz=MzI2OTE2NzczNQ==&mid=2649967188&idx=1&sn=14ace8de8e4976f2282d79cafcc1ff64&scene=4#wechat_redirect',
        'https://mp.weixin.qq.com/s?__biz=MzI2OTE2NzczNQ==&mid=2649967190&idx=1&sn=dfa0f6072ae85212d3703e5a6efc5774&scene=4#wechat_redirect',
        'https://mp.weixin.qq.com/s?__biz=MzI2OTE2NzczNQ==&mid=2649967192&idx=1&sn=b7b8d50dce4c9c2f7bcda175a8f452e6&scene=4#wechat_redirect',
        'https://mp.weixin.qq.com/s?__biz=MzI2OTE2NzczNQ==&mid=2649968005&idx=1&sn=eca73fbf128cce1a4051469ff4d692f9&chksm=f2e3909dc594198bee00dd57f54e58fe158e863eb2962f76eb79e43874ab22d8808c49bf24af#rd',
        'https://mp.weixin.qq.com/s/p7vdIKfwHNPYZYcOIvfKzQ?',
    ]
    images(url_list)
