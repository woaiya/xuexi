#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/2/3 9:46
# @Author: Nome
# @Site: 
# @File: jokes.py
# @Software: PyCharm
"""
抓取糗事百科段子
"""
import time
import xlwt
import requests
from bs4 import BeautifulSoup
import pymysql


class Database:
    connect = pymysql.Connect(
        host='localhost',
        port=3610,
        user='root',
        passwd='******',
        db='python',
        charset='utf8'
    )
    cursor = connect.cursor()

    # jokes表添加数据方法
    def add_data_jokes(self, *data):
        sql = "INSERT INTO jokes (jokes_nickname,jokes_content,jokes_funny,jokes_comment,jokes_type) " \
              "VALUE ('%s','%s',%d,%d,%d)" % (data[0], data[1], data[2], data[3], data[4])
        self.cursor.execute(sql)
        self.connect.commit()
        print("添加成功")


class QShiBaiKe:
    head = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Mobile Safari/537.36"}
    initial_url = "https://www.qiushibaike.com/text/page/"
    # url_number = 2
    jokes_number = 0
    jokes_list = []

    def __init__(self, url_number=5):
        self.url_number = url_number
        self.database = Database()

    # 生成url方法
    def return_url(self, page):
        r_url = self.initial_url + str(page)
        return r_url

    # 请求网页数据方法,并解析数据
    def qRequest(self, r_url):
        html_data = requests.get(r_url, self.head)
        tree = BeautifulSoup(html_data.content, "html.parser")
        self.jokesLong(tree, "typs_long")
        self.jokesLong(tree, "typs_hot")

    # 抓取需要的数据
    def jokesLong(self, tree, jokes_type):
        jokes_long = tree.findAll("div", {"class": "article block untagged mb15 " + jokes_type})
        num = len(jokes_long)
        for i in range(0, num):
            self.jokes_number += 1
            jokes_nickname = jokes_long[i].img["alt"]     # 发帖人昵称
            home = jokes_long[i].findAll("a", {"class": "contentHerf"})
            homepage = BeautifulSoup(str(home), "html.parser")
            jokes_homepage = "https://www.qiushibaike.com" + homepage.a["href"]      # 主页url
            jokes_content = homepage.div.span.text.strip()      # 内容
            stats = jokes_long[i].findAll("div", {"class": "stats"})
            stats_data = BeautifulSoup(str(stats), "html.parser")
            number = stats_data.findAll("i", {"class": "number"})
            # jokes_vote = stats_data.span.text.replace(" ", "人觉得")       # 觉得好笑的人数
            jokes_vote = number[0].string       # 觉得好笑的人数
            jokes_comments = number[1].string       # 评论人数
            jokes = [self.jokes_number, jokes_nickname, jokes_homepage,
                     jokes_content, jokes_vote, jokes_comments, jokes_type]
            self.jokes_list.append(jokes)

    # 写入xls文件方法
    def save(self):
        f = xlwt.Workbook()
        sheet1 = f.add_sheet(r' sheet1', cell_overwrite_ok=True)
        poster_w = ("次序", "昵称", "主页", "内容", "感觉好笑的人", "评论人数", "类型")
        poster_w_num = len(poster_w)
        for u in range(1, poster_w_num+1):
            sheet1.write(0, u-1, poster_w[u-1])
        num = len(self.jokes_list)
        for i in range(1, num + 1):
            for op in range(1, poster_w_num+1):
                sheet1.write(i, op-1, self.jokes_list[i-1][op-1])
        f.save("jokes.xls")

    # 写入数据库
    def save_database(self):
        print(self.jokes_list)
        number = len(self.jokes_list)
        for i in range(0, number):
            jokes_nickname = self.jokes_list[i][1]
            jokes_content = self.jokes_list[i][3]
            jokes_funny = self.jokes_list[i][4]
            jokes_comment = self.jokes_list[i][5]
            j_type = self.jokes_list[i][6]
            if j_type == 'typs_long':
                jokes_type = 0
            else:
                jokes_type = 1
            self.database.add_data_jokes(jokes_nickname, jokes_content, int(jokes_funny), int(jokes_comment), int(jokes_type))

    # 主函数
    def main(self):
        start_time = time.time()
        for i in range(1, self.url_number + 1):
            print("第%s页爬取中" % i)
            url = self.return_url(i)
            self.qRequest(url)
            print("第%s页爬取完毕" % i)
        self.save_database()
        # self.save()
        print(time.time()-start_time)


if __name__ == "__main__":
    qsbk = QShiBaiKe(5)
    qsbk.main()