#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time: 2018/2/26 14:14
# @Author: Nome
# @Site: 
# @File: fist.py
# @Software: PyCharm

"""
后台保险产品上传脚本练习
"""

import xlrd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select


class FistData:
    data = xlrd.open_workbook('保险.xlsx')
    data_fist = data.sheet_by_index(0)
    num = data_fist.nrows
    browser = webdriver.Firefox()
    browser.get("http://cyj1.binarynt.com/admin.php/login/index.html")

    # 登录
    def login_html(self):
        self.browser.find_element_by_name("name").send_keys("admin")
        self.browser.find_element_by_name("password").send_keys("******")
        WebDriverWait(self.browser, 20, 0.5)\
            .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'panel-heading')))
        self.browser.find_element_by_link_text("保险管理").click()
        for i in range(0, self.num):
            WebDriverWait(self.browser, 20, 0.5) \
                .until(expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, '添加保险产品')))
            self.browser.find_element_by_link_text("添加保险产品").click()
            product_name = self.data_fist.cell_value(i, 0)
            company_name = self.data_fist.cell_value(i, 1)
            card_code = self.data_fist.cell_value(i, 2)
            insure_type = self.data_fist.cell_value(i, 3)
            # ke_content = self.data_fist.cell_value(i, 4)
            self.browser.find_element_by_name("insure_name").send_keys(company_name)
            self.browser.find_element_by_name("logo").send_keys("E:\PythonTest\\180225\photo\%s.jpg" % company_name)
            # 下拉框选择
            Select(self.browser.find_element_by_name("insure_type")).select_by_visible_text(insure_type)

            self.browser.find_element_by_name("productName").send_keys(product_name)
            self.browser.find_element_by_name("cardCode").send_keys(card_code)

            """            
            sleep(2)
            富文本输入框输入
            rich_text = self.browser.find_element_by_xpath('//*[@class="ke-edit-iframe"]')   # 定位到框架
            self.browser.switch_to_frame(rich_text)       # 进入框架
            self.browser.find_element_by_xpath('//*[@class="ke-content"]').send_keys(ke_content)
            self.browser.switch_to_default_content()      # 退出框架
            """

            self.browser.find_element_by_id("submit").click()
        self.browser.quit()

    def main(self):
        self.login_html()


if __name__ == "__main__":
    fist = FistData()
    fist.login_html()