#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/1/29 14:27
# @Author: Nome
# @Site: 
# @File: thread.py
# @Software: PyCharm

import threading
import time
import queue   # 导入消息队列模块
import random  # 导入随机数模块，是为了模拟生产者与消费者速度不一致的情形

q = queue.Queue(maxsize=5)


def Producer():  # 生产者函数
    for i in range(1, 21):
        q.put(i)  # 将结果放入消息队列中
        print('cook:生产包子 数量:%s' % i)
        time.sleep(random.randrange(3))  # 生产者的生产速度，3s内


def Consumer():  # 消费者函数
    count = 0
    while count < 20:
        data = q.get()  # 取用消息队列中存放的结果
        print('消费者:Lao Wang 吃包子:%s' % data)
        count += 1
        time.sleep(random.randrange(4))  # 消费者的消费速度，4s内


p = threading.Thread(target=Producer)
c = threading.Thread(target=Consumer)

p.start()
c.start()