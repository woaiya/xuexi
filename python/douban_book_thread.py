#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/2/2 17:29
# @Author: Nome
# @Site: 
# @File: douban_book_thread.py
# @Software: PyCharm

"""
多线程抓取豆瓣图书数据
"""

import re
import requests
import time
import xlwt
from threading import Thread
from bs4 import BeautifulSoup

book = []


class GetUrlThread(Thread):
    def __init__(self, url):
        self.page = url
        self.url = "https://book.douban.com/top250?start=" + str(self.page)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"}
        super(GetUrlThread, self).__init__()

    # 线程公共操作
    def run(self):
        resp = requests.get(self.url, self.headers)
        soup = BeautifulSoup(resp.content, "html.parser")
        datas = soup.findAll("table", {"width": "100%"})
        num = len(datas)
        for i in range(1, num+1):
            data = BeautifulSoup(str(datas[i-1]), "html.parser")
            book_img = data.img["src"]  # 图书照片
            top = data.findAll("td", {"valign": "top"})
            top_data = BeautifulSoup(str(top[1]), "html.parser")
            book_home = top_data.a['href']  # 图书主页
            book_name = top_data.a['title']  # 图书名称
            book_data = top_data.p.string  # 图书的基本信息
            book_scoring = top_data.findAll("span", {"class": "rating_nums"})[0].text  # 图书评分
            book_number = re.findall('(.*?)人评价', str(top_data))[0].strip()  # 评价的人数
            essay = top_data.findAll("span", {"class": "inq"})  # 图书短评
            if len(essay) == 0:
                book_essay = "无"
            else:
                book_essay = essay[0].string
            alt = top_data.findAll("img", {"alt": "可试读"})
            if len(alt) == 0:
                book_alt = "不可试读"
            else:
                book_alt = "可试读"  # 是否可试读
            style = top_data.findAll("span", {"style": "font-size:12px;"})
            if len(style) == 0:
                book_english_name = "无"
            else:
                book_english_name = style[0].string.replace(" : ", "")  # 图书的原名, replace用来将字符串中的：替换成空值
            s = (self.page, i, book_name, book_img, book_home, book_data, book_scoring, book_number, book_essay, book_alt, book_english_name)
            book.append(s)


def get_responses():
    urls = []
    for i in range(0, 250, 25):
        urls.append(i)
    start = time.time()
    threads = []
    for url in urls:
        t = GetUrlThread(url)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print('抓取内容时间:%s' % (time.time()-start))


def write():
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(r' sheet1', cell_overwrite_ok=True)
    poster_w = ("图书名称", "图书照片", "图书主页", "图书信息", "图书评分", "图书评价人数", "图书短评", "图书是否试读", "图书原名")
    poster_w_num = len(poster_w)
    for u in range(1, poster_w_num + 1):
        sheet1.write(0, u - 1, poster_w[u - 1])
    num = len(book)
    for i in range(1, num+1):
        for op in range(1, poster_w_num + 1):
            sheet1.write(i, op-1, book[i-1][op+1])
    f.save("douban.xls")


def main():
    get_responses()
    book.sort(key=lambda k: k[0])
    write()


main()