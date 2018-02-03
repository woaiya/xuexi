#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/2/2 17:25
# @Author: Nome
# @Site: 
# @File: qsbk_jokes.py
# @Software: PyCharm
"""
异步多线程抓取糗百文字段子
"""
import requests
from bs4 import BeautifulSoup
import threading
import time
import queue   # 导入消息队列模块
import random  # 导入随机数模块，每页抓取完毕后随机休眠


class Qsbk:

    def __init__(self, type_num=1):
        self.jokes_data = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"}
        self.initial_url = "https://www.qiushibaike.com/text/page/"
        self.q = queue.Queue(1)
        self.type_num = type_num

    # 请求网页数据
    def request_url(self):
        for i in range(1, self.type_num+1):
            url = self.initial_url + str(i)
            url_request = requests.get(url, self.headers)
            url_data = BeautifulSoup(url_request.content, "html.parser")
            self.q.put(url_data)
            s_time = random.randint(1, 3)
            time.sleep(s_time)

    # 抓取网页数据
    def analytical_data(self):
        count = 0
        while count < self.type_num:
            q_data = self.q.get()
            self.get_data(q_data, "article block untagged mb15 typs_long")
            self.get_data(q_data, "article block untagged mb15 typs_hot")
            count += 1
            time.sleep(2)
        print(self.jokes_data)
        print(len(self.jokes_data))

    # 抓取的主要方法
    def get_data(self, data, data_type):
        jokes = []
        jokes_type = data.findAll("div", {"class": data_type})
        jokes_num = len(jokes_type)
        for num in range(0, jokes_num):
            jokes_data = jokes_type[num]
            jokes_release = jokes_data.img["alt"]
            jokes_content = jokes_data.findAll("div", {"class": "content"})[0].text.strip()
            jokes.append(jokes_release)
            jokes.append(jokes_content)
            self.jokes_data.append(jokes)

    #  显示抓取的数据及其数量
    def get_jokes_data(self):
        print(self.jokes_data)
        print(len(self.jokes_data))

    # 线程管理
    def thread(self):
        p = threading.Thread(target=self.request_url)
        c = threading.Thread(target=self.analytical_data)

        p.start()
        c.start()

    # 主程序
    def main(self):
        self.thread()


if __name__ == "__main__":
    qsbk = Qsbk(5)
    qsbk.main()