#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/2/2 17:22
# @Author: Nome
# @Site: 
# @File: douban_book.py
# @Software: PyCharm
"""
抓取豆瓣图书
"""

import re
import requests
from bs4 import BeautifulSoup


def requests_html_data():
    i = 0
    while i < 300:
        url = 'https://book.douban.com/top250?start='
        geturl = url + str(i)
        postData = {"start": i}
        res = requests.post(geturl, data=postData)
        soup = BeautifulSoup(res.content, "html.parser")  # 此行及其以上是获取目标网页的html源码
        table = soup.findAll('table', {"width": "100%"})  # 此行用来查询html标签table下且有width，100% 标签的所有数据
        sz = len(table)   # 统计有多少个table数据
        for j in range(1, sz+1):  # 遍历1到sz
            sp = BeautifulSoup(str(table[j - 1]), "html.parser")  # 解析每一本书的信息
            imageurl = sp.img['src']  # 图片链接
            bookurl = sp.a['href']    # 图书链接
            bookName = sp.div.a['title']  # 图书名字
            nickname = sp.div.span   # 别名
            if (nickname):  # 有别名则有，无别名则None
                nickname = nickname.string.strip()
            else:
                nickname = 'None'

            notion = str(sp.find('p', {"class": "pl"}).string)   # 出版信息 str类型
            rating = str(sp.find("span", {"class": "rating_nums"}).string)  # 平均分数
            nums = sp.find('span', {"class": "pl"}).string  # 评分人数
            nums = nums.replace('(', '').replace(')', '').replace('\n', '').strip()
            nums = re.findall('(\d+)人评价', nums)[0]

            book = requests.get(bookurl)   # 打开图书链接
            sp3 = BeautifulSoup(book.content, "html.parser")  # 解析
            taglist = sp3.find_all('a', {"class": " tag"})   # 找标签
            tag = ""
            lis = []
            for tagurl in taglist:
                sp4 = BeautifulSoup(str(tagurl), "html.parser")   # 解析每个标签
                lis.append(str(sp4.a.string))
            tag = ','.join(lis)   # 加逗号
            if tag == "":         # 没有标签则显示None
                tag = "None"
            print(i + j, bookName, nickname, imageurl, bookurl, notion, rating, nums, tag)
        i += 25
    print("数据加载完毕")


if __name__ == '__main__':
    requests_html_data()