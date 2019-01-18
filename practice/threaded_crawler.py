# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/23 18:05'

import time
import threading
from urllib.parse import *
from downloader import Download

SLEEP_TIME = 1


def threaded_crawler(seed_url, delay=5, cache=None, scrapy_callback=None, user_agent='wswp', proxies=None,
                     num_retries=1, max_threads=10, timeout=60):
    crawl_queue = [seed_url]
    seen = set([])
    D = Download(cache=cache, delay=delay
                 , user_agent=user_agent, proxies=proxies,
                 num_retries=num_retries, timeout=timeout)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                break
            else:
                html = D(url)
                if scrapy_callback:
                    try:
                        links = scrapy_callback(url, html) or []
                    except Exception as e:
                        print(f'Error in callback for:{url}:{e}')
                    else:
                        for link in links:
                            link = normalize(seed_url, link)
                            if link not in seen:
                                seen.add(link)
                                crawl_queue.append(link)

    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < max_threads and crawl_queue:
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)


def normalize(seed_url, link):
    link, _ = urldefrag(link)
    return urljoin(seed_url, link)
