#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/2/2 17:25
# @Author: Nome
# @Site: 
# @File: qioubai.py
# @Software: PyCharm
"""
抓取糗事百科段子
"""
import requests
from bs4 import BeautifulSoup
import xlwt

f = xlwt.Workbook()
sheet1 = f.add_sheet(r' sheet1', cell_overwrite_ok=True)
poster_w = ("发帖人", "头像", "年龄", "主页URL", "帖子内容", "详情URL", "感觉好笑人数", "评论人数")
poster_w_num = len(poster_w)
for op in range(1, poster_w_num+1):
    sheet1.write(0, op-1, poster_w[op-1])


# 用来解析html网页数据
def html_data(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup


# 用来控制抓取的页码数量
def text_url(num=2):
    page = 1
    url_list = []
    while page < num:
        url = "https://www.qiushibaike.com/text/page/%s" % page
        url_list.append(url)
        page += 1
    url_list_num = len(url_list)
    return url_list_num, url_list


# 抓取段子的第一条数据
def pars_data_long(soup):
    typs_long = soup.findAll("div", {"class": "article block untagged mb15 typs_long"})
    typs_long_num = len(typs_long)
    return typs_long_num, typs_long


# 抓取段子的其他数据
def pars_data_hot(soup):
    typs_hot = soup.findAll("div", {"class": "article block untagged mb15 typs_hot"})
    typs_hot_num = len(typs_hot)
    return typs_hot_num, typs_hot


# 解析需要的数据
def data_pars(soup, number):
    soup_num = soup[0]
    soup_data = soup[1]
    particulars_url_list = []
    for num in range(1, soup_num+1):
        data = BeautifulSoup(str(soup_data[num-1]), "html.parser")
        poster = data.img["alt"]  # 发帖人昵称
        poster_img = "https:" + data.img["src"]  # 发帖人头像
        poster_url = "https://www.qiushibaike.com" + data.a["href"]  # 发布人主页url
        if poster == "匿名用户":
            poster_age = None       # 匿名用户时年龄为None
        else:
            poster_age = data.div.div.div.string  # 发帖人的年龄
        content = data.findAll("div", {"class": "content"})
        content1 = BeautifulSoup(str(content), "html.parser")
        poster_content = content1.span.text.strip()  # 帖子内容
        stats = data.findAll("div", {"class": "stats"})
        stats1 = BeautifulSoup(str(stats), "html.parser")
        particulars_url = "https://www.qiushibaike.com" + stats1.a["href"]  # 帖子详情页网址
        particulars_url_list.append(particulars_url)
        funny_number = stats1.span.i.string  # 感觉好笑的人数
        commentaries_number = stats1.a.i.string  # 评论人数
        poster_1 = "发帖人：" + poster + "\n" + "头像：" + poster_img + "\n" + "年龄：" + str(poster_age) + "\n" + "主页URL：" + poster_url + "\n"
        poster_2 = "帖子内容：" + poster_content + "\n" + "详情URL：" + particulars_url + "\n" + "感觉好笑人数:" + funny_number + "\n" + "评论人数:" + commentaries_number
        poster_3 = "\n" + "-------------------------------------------------"
        poster_4 = "这是第%d页第%d条帖子" % (number, num) + "\n"
        out = (number-1)*soup_num + num
        posters = poster_4 + poster_1 + poster_2 + poster_3
        poster_data = (poster, poster_img, str(poster_age), poster_url, poster_content, particulars_url, funny_number, commentaries_number)
        for up in range(1, poster_w_num+1):
            sheet1.write(out, up-1, poster_data[up-1])
        print(posters)
    return particulars_url_list


def main():
    data = text_url(5)
    data_num = data[0]
    for num in range(1, data_num+1):
        url = data[1][num-1]
        datas = html_data(url)
        soups = pars_data_hot(datas)
        data_pars(soups, num)


if __name__ == "__main__":
    main()
    f.save("qsbk.xls")