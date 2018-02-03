#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/2/3 10:48
# @Author: Nome
# @Site: 
# @File: pyecharts_test.py
# @Software: PyCharm
"""
图表生成练习
"""
from pyecharts import Bar

bar = Bar("我的第一个图表", "这个是一个副标题")
bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
        [5, 20, 36, 10, 75, 90])
bar.show_config()
bar.render()
