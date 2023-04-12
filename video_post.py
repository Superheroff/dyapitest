# -*- coding: utf-8 -*-
"""
@Time    : 2023/4/5 12:05
@Author  : superhero
@Email   : 838210720@qq.com
@File    : demo.py
@IDE: PyCharm
"""
import hashlib
import re
import requests
import time
import urllib.parse
import json


def set_sign():
    """
    计算api签名
    :return:
    """
    ts = str(time.time()).split('.')[0]
    string = '1005d9ba8ae07d955b83c3b04280f3dc5a4a' + ts + get_appkey()
    sign = hashlib.md5(string.encode('utf8')).hexdigest()
    return sign


def get_appkey():
    """
    获取appkey
    :return:
    """
    data = 'd9ba8ae07d955b83c3b04280f3dc5a4a5c6b8r9a'
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    url = "https://www.douyin.com/user/MS4wLjABAAAAfjsAJZbhlKTAhClTsxbP1b04RvyTjBRPgNWzLGnMR0c"
    ts = str(time.time()).split('.')[0]
    header = {
        'cid': 'd9ba8ae07d955b83c3b04280f3dc5a4a',
        'timestamp': ts,
        'user-agent': 'okhttp/3.10.0.12'
    }
    # 这里只是获取cookie，可以用playwright或selenium替代
    res = requests.post("http://api2.52jan.com/dyapi/get_cookie/v2", data={"sign": set_sign()}, headers=header).json()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/111.0.0.0 Safari/537.36',
        "cookie": res['data'][0][0]}
    ret = requests.get(url, headers=headers).text
    data = re.search(r'<script id="RENDER_DATA" type="application/json">(.*?)%22post%22%3A%7B%22(.*?)%2C%22_location', ret).group(2)
    data_json = json.loads('{"post":{"' + urllib.parse.unquote(data))
    print(data_json)
