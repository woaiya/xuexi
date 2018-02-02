#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/2/2 17:27
# @Author: Nome
# @Site: 
# @File: douban_movie.py
# @Software: PyCharm
"""
抓取豆瓣电影(top250)
"""

import re
import xlwt
import requests
from bs4 import BeautifulSoup


class Movies:
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(r' sheet1', cell_overwrite_ok=True)
    poster_w = ("电影排名", "电影名称", "电影别名", "电影主页", "电影参与人", "电影评分", "评价人数", "电影短评", "是否能播放")
    poster_w_num = len(poster_w)
    for op in range(1, poster_w_num + 1):
        sheet1.write(0, op - 1, poster_w[op - 1])

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"}
        self.movies_list = []

    @staticmethod
    def parse(*value):
        if value[0] == 0:
            data = BeautifulSoup(value[1].content, "html.parser")
        else:
            data = BeautifulSoup(str(value[1]), "html.parser")
        return data

    @staticmethod
    def analyze(*value):
        if value[0] == 0:
            data = value[1].findAll(value[2])
        else:
            data = value[1].findAll(value[2], {value[3]: value[4]})
        return data

    def html_data(self):
        page = 0
        while page < 250:
            url = "https://movie.douban.com/top250?start=%s&filter=" % int(page)
            data = requests.get(url, self.headers)
            all_data = self.parse(0, data)
            re_data = self.analyze(1, all_data, "div", "class", "item")
            re_data_num = len(re_data)
            for num in range(1, re_data_num+1):
                film_list = []
                film = self.parse(1, re_data[num-1])  # 这一页所有的电影数据
                film_id = film.em.string   # 获得电影的排名
                hd = self.analyze(1, film, "div", "class", "hd")   # div 标签下class = hd 的所有数据
                film_hd = self.parse(1, hd)
                film_home = film_hd.a["href"]  # 电影的主页
                title = self.analyze(1, film_hd, "span", "class", "title")
                title_num = len(title)
                if title_num == 2:
                    film_name = title[0].string + title[1].string   # 电影名称
                else:
                    film_name = title[0].string       # 电影名称
                other = self.analyze(1, film_hd, "span", "class", "other")
                film_aliases = other[0].string   # 电影别名
                playable = self.analyze(1, film_hd, "span", "class", "playable")
                playable_num = len(playable)
                if playable_num == 0:
                    film_state = "无法播放"
                else:
                    film_state = playable[0].string  # 是否可播放
                bd = self.analyze(1, film, "div", "class", "bd")    # div 标签下class = bd 的所有数据
                film_bd = self.parse(1, bd)
                film_personnel = film_bd.p.get_text().strip().replace(" ", "").replace("\n", "")   # 电影参与人员
                # personnel = re.findall('主演:(.*)/(.*)/(.*)/(.*)', film_personnel)
                # film_starring = personnel[0][0]  # 电影主演
                # film_year = personnel[0][1].replace(".", "")  # 电影年份
                # film_area = personnel[0][2]  # 电影所属地区
                # film_type = personnel[0][3]  # 电影的分类
                star = self.analyze(1, film_bd, "span", "class", "rating_num")
                film_scoring = star[0].string    # 电影评分
                film_appraise = re.findall('>(.*?)人评价', str(film_bd))[0]  # 评价人数
                inq = self.analyze(1, film_bd, "span", "class", "inq")
                inq_num = len(inq)
                if inq_num == 0:
                    film_essay = "暂无短评"
                else:
                    film_essay = inq[0].string    # 电影短评
                movie1 = "电影排名：" + film_id + "\n" + "电影主页：" + film_home + "\n" + "电影名称：" + film_name + "\n" + "电影别名：" + film_aliases + "\n" + "是否能播放：" + film_state + "\n"
                movie2 = "电影参与人：" + film_personnel + "\n" + "电影评分：" + film_scoring + "\n" + "评价人数：" + film_appraise + "\n" + "电影短评：" + film_essay + "\n"
                movie = movie1 + movie2
                movie_w = film_id + film_name + film_aliases + film_home + film_personnel + film_scoring + film_appraise + film_essay + film_state
                film_list.append(film_id)
                film_list.append(film_name)
                film_list.append(film_aliases)
                film_list.append(film_home)
                film_list.append(film_personnel)
                film_list.append(film_scoring)
                film_list.append(film_appraise)
                film_list.append(film_essay)
                film_list.append(film_state)
                for up in range(1, self.poster_w_num+1):
                    self.sheet1.write(int(film_id), int(up)-1, film_list[up-1])
                self.movies_list.append(movie_w)
            page += 25
            pages = int(page/25)
            print("正在保存第%s页" % pages)
        self.f.save("douban.xls")
        print("保存完毕")
        return self.movies_list


if __name__ == "__main__":
    movies = Movies()
    datas = movies.html_data()