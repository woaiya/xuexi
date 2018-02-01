#!/usr/bin/env python
# _*_coding:utf-8_*_


import logging
import qrcode
from TEST.QQtest import logger

try:
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )
    qr.add_data("https://www.baidu.com/")
    qr.make(fit=True)
    img = qr.make_image()
    img.save("E:\PythonTest\TEST\二维码\test1.png")
except OSError as e:
    logging.error(e, exc_info=1)
    logger.info(e)
