#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/2/5 14:07
# @Author: Nome
# @Site: 
# @File: database.py
# @Software: PyCharm

"""
连接本地数据库
"""
from pyecharts import Bar
import pymysql.cursors


class DataBase:
    connect = pymysql.Connect(
        host='localhost',
        port=3610,
        user='root',
        passwd='*******',
        db='python',
        charset='utf8'
    )
    # 获得数据库游标
    cursor = connect.cursor()

    # 查询数据
    def query_data(self, statements):
        sql = statements
        self.cursor.execute(sql)
        results = self.cursor.fetchall()  # 此行获得查询到的所有数据
        self.connect.close()
        return results


class Analysis:
    database = DataBase()

    # 获得数据
    def get_data(self):
        statements = "SELECT jokes_nickname,jokes_funny, jokes_comment FROM `jokes`"
        data = self.database.query_data(statements)
        return data

    def generated(self):
        data = self.get_data()
        data_num = len(data)
        nickname_array = []
        funny_array = []
        comment_array = []
        for i in range(0, data_num):
            nickname = data[i][0]
            funny = data[i][1]
            comment = data[i][2]
            nickname_array.append(nickname)
            funny_array.append(funny)
            comment_array.append(comment)
        bar = Bar("糗事百科", "最新八十条数据觉得好笑的图表")
        # --------------------生成一个数据的-----------------------
        # bar.add("觉得好笑", nickname_array, funny_array)

        # --------------------生成两个数据的-----------------------
        bar.add("觉得好笑人数", nickname_array, funny_array, mark_line=["average"], mark_point=["max", "min"])
        bar.add("评论人数", nickname_array, comment_array, mark_line=["average"], mark_point=["max", "min"])
        # # bar.show_config()   # 打印配置信息
        bar.render("jokes.html")


if __name__ == "__main__":
    analysis = Analysis()
    analysis.generated()