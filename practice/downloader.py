# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/23 12:54'

from urllib import request
from urllib.parse import *
import random
import time
from datetime import datetime
import socket

DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60


class Download:
    def __init__(self, delay=DEFAULT_DELAY, user_agent='DEFAULT_AGENT', proxies=None, num_retries=DEFAULT_RETRIES,
                 timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                try:
                    if self.num_retries > 0 and 500 <= result['code'] < 600:
                        result = None
                except Exception as e:
                    result = None
                else:
                    pass
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        print('Downloading: ', url)
        req = request.Request(url, data, headers or {})
        opener = self.opener or request.build_opener()
        if proxy:
            proxy_params = {urlparse(url).scheme: proxy}
            opener.add_handler(request.ProxyHandler(proxy_params))
        try:
            response = opener.open(req)
            html = response.read().decode('utf-8')
            code = response.code
        except Exception as e:
            print('Download error', str(e))
            html = ""
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    return self.download(url, headers, proxy, num_retries - 1, data)
            else:
                code = None
        return {"html": html, 'code': code}


class Throttle:
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_delay = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_delay > 0:
                time.sleep(sleep_delay)
        self.domains[domain] = datetime.now()
