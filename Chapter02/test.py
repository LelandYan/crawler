# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2019/1/23 15:57'
import  requests
import re
if __name__ == '__main__':
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    path = "https://www.toutiao.com/a6428359204088660226/"
    content = requests.get(path,headers=headers).text
    images_pattern = re.compile('gallery: JSON.parse\((.*?)\),', re.S)
    result = re.search(images_pattern, content)
    print(result.group(1))