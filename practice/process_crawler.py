# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/23 18:05'

import time
import threading
from urllib.parse import *
from downloader import Download
import multiprocessing
from mongo_cache import MongoCache
from mongo_queue import MongoQueue

SLEEP_TIME = 1


def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None,
                     num_retries=1, max_threads=10, timeout=60):
    crawl_queue = MongoQueue()
    crawl_queue.clear()
    crawl_queue.push(seed_url)
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
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print(f'Error in callback for:{url}:{e}')
                    else:
                        for link in links:
                            crawl_queue.push(normalize(seed_url, link))
                crawl_queue.complete(url)

    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < max_threads and crawl_queue.peek():
            thread = threading.Thread(target=process_queue)
            thread.start()
            threads.append(thread)

            time.sleep(SLEEP_TIME)


def process_crawler(args, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    print(f'Starting {num_cpus}processed')
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler, args=[args], kwargs=kwargs)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def normalize(seed_url, link):
    link, _ = urldefrag(link)
    return urljoin(seed_url, link)
