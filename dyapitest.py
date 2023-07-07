# -*- coding: utf-8 -*-
import base64
import gzip
import hashlib
import json
import random
import time
from urllib.parse import urlencode

import requests


def get_str_btw(s, f, b):
    # 取文本中间
    par = s.partition(f)
    return (par[2].partition(b))[0][:]


class dyapi:
    # 主
    host = 'http://api2.52jan.com'

    # proxies = {'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}

    def __init__(self, cid):
        self.cid = cid
        self.array = {}
        self.__web_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        self.__appkey = ''

    def get_appkey(self):
        """
        这是本api的加密
        :return:
        """
        # 获取appkey
        data = self.cid + '5c6b8r9a'
        self.__appkey = hashlib.sha256(data.encode('utf-8')).hexdigest()
        # print('appkey', self.__appkey)

    def get_web_xbogus(self, url, ua):
        """
        获取web xbogus
        :param url:
        :param ua:
        :return:
        """
        sign_url = dyapi.host + '/dyapi/web/xbogus'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        params = {
            'url': url,
            'ua': ua,
            'sign': sign
        }
        resp = requests.post(sign_url, data=params, headers=header).json()
        print('web_xbogus', resp)
        return resp

    def get_web_sign(self, url, referer, ua):
        """
        获取web sign
        :param url:
        :param referer:
        :param ua:
        :return:
        """
        sign_url = dyapi.host + '/dyapi/web/signature'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        params = {
            'url': url,
            'referer': referer,
            'ua': ua,
            'sign': sign

        }
        resp = requests.post(sign_url, data=params, headers=header).json()
        print('web_sign', resp)
        return resp

    def get_xgorgon(self, url, cookie, params, ver, headers=None):
        '''
        获取x-gorgon
        :param url:
        :param cookie:
        :param params: post提交
        :param ver: 版本号
        :param headers:
        :return:
        '''
        sign_url = dyapi.host + '/dyapi/xgorgon'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        self.array['url'] = url
        self.array['sign'] = sign
        self.array['cookie'] = cookie
        self.array['ver'] = ver
        self.array['params'] = params
        self.array['headers'] = json.dumps(headers)
        resp = requests.post(sign_url, data=self.array, headers=header).json()
        print('xgorgon', resp)
        return resp

    def get_ApiInfo(self):
        """
        获取接口使用情况
        minCount 当前用了多少
        maxCount 你可以用的最大值
        :return:
        """
        url = dyapi.host + '/end_time'
        resp = requests.post(url, data={'cid': self.cid, 'api': 'dyapi'}).text
        return resp

    def get_device(self):
        '''
        获取设备号
        :return:
        '''
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        params = {
            'sign': sign,
            'set_ip': '0',
            'num': '1'
        }

        """
        set_ip：0=随机设备池，1=根据ip分配固定设备池
        num: 获取设备的数量
        """
        device_url = dyapi.host + '/dyapi/get_device'
        resp = requests.post(device_url, data=params, headers=header)
        print('设备id:', resp.text)
        return resp.json()

    def md5(self, str):
        post_data = gzip.compress(bytes(json.dumps(str), encoding="utf8"))
        m = hashlib.md5()
        m.update(bytes(post_data))
        str_md5 = m.hexdigest()
        return str_md5.upper()

    def get_keyword(self, device_id, iid, keyword, page):
        """
        搜索视频
        :param device_id:
        :param iid:
        :param keyword:
        :param page:
        :return:
        """

        url = f"https://aweme.snssdk.com/aweme/v1/search/item/?os_api=25&device_type=Pixel+XL&ssmix=a" \
              f"&manifest_version_code=180101&dpi=560&is_guest_mode=0&app_name=aweme&version_name=18.1" \
              f".0&ts={int(time.time())}&cpu_support64=true&app_type=normal&appTheme=light&ac=wifi&host_abi=armeabi" \
              f"-v7a&channel=wandoujia_lesi_1128_0629&update_version_code=18109900&_rticket=1686903952535" \
              f"&device_platform=android&iid={iid}&version_code=180100&cdid=0528d7f9-bb0f-4d1d-b142-097951a0629d&os" \
              f"=android&is_android_pad=0&openudid=60a02c5de917fa4c&device_id=" \
              f"{device_id}&package=com.ss.android.ugc.aweme&resolution=1440*2392&device_brand=google&language=zh" \
              f"&os_version=7.1.2&need_personal_recommend=1&aid=1128&minor_status=0"

        data = {
            "keyword": keyword,
            "offset": page,
            "count": "12",
            "source": "video_search",
            "from_user": "",
            "search_source": "switch_tab",
            "is_pull_refresh": "1",
            "hot_search": "0",
            "search_id": "",
            "query_correct_type": "1",
            "is_filter_search": "0",
            "sort_type": "0",
            "publish_time": "0",
            "search_range": "0",
            "enter_from": "homepage_hot",
            "backtrace": "",
            "user_avatar_shrink": "64_64",
            "video_cover_shrink": "372_496",
            "previous_searchid": "20230616162541D17367263D89FB0029F7",
            "switch_tab_from": "general",
            "rs_word_count": "5",
            "location_permission": "0",
            "need_filter_settings": "1",
            "enable_history": "1"
        }

        headers = {
            "X-SS-STUB": self.md5(json.dumps(data)),
            "activity_now_client": str(int(time.time() * 1000)),
            "x-ss-req-ticket": str(int(time.time() * 1000)),
            "x-vc-bdturing-sdk-version": "2.2.1.cn",
            "passport-sdk-version": "20356",
            "sdk-version": "2",
            "User-Agent": "okhttp/3.10.0.1",
            # "X-Ladon": "Fmwzchui1d9Bq4YebHART+PamP6awv5wq1ovcMlrm2Ugad0r",
            # "X-Khronos": "1686900009",
            # "X-Gorgon": "8404e04200056c703e652c97d023fd0577de3ae546915de0072d",
            # "X-Medusa": "Kw2MZB9hGQgcf9b/zdmRAeG19ULZNGJF1QWJQlIBamjbj/Jvc4gOGDJHatwPrzkMg3XHeDG/D1HWp23rFtOEze91VQd1RsEa0oZb9JEbfJLPJNDQTvP+Yg7DAYpO1k5Q9CNldKbv6FuGuqfFBt8Llx8lvbu16yxbwExrxXIDpxetUkw9Y4p9jc5y1MFT222L9ex/DJ4jDpe4HGchME2XQT/ygJNHJ12MFMYk/sTRYbDCuzWFe2rqErJSAVREY53HHU1ovFgXB2YKLqghSk/ZD+5/9a70i8x5D85aJMxUa8U6BN5gG6l8+5/hc+9p/NHXX2WcIEj+zXxZ2uDCOZPO9vn/LDpzYM4UGKRDIKk4SstUKCLgRL8A7NmXbwqGmfl7FXM1fXserhP59EXBBryjUbjRoxlf/Q==",
            # "X-Helios": "Jcqpen49rqhO8rTb/3E9G+N85U65yy4//vupPM33B6BaoQ6S",
            # "X-Argus": "XdYCNeAU12qsWMY0anSNeqWBmM4FNPLHXe4HY3C0VK/rVajjGV6+S2hnYoODLJX3A9a9dHM4UouytekIw+D/CWb1izuwO9LADIV+ro/5WxZJBriWVODiRk7mSQJJZQ5uCtgeVmd8YmfubtAI/QKG0L+EkhVvblnRY5fO8JxSSsrhM51/nfC7vAZ1csVCJh7fBf8L43dM5M+60NtwYVbBjM36nKcq1Kd1DKRq9oZfqHn/Za6DUDwf1ejq7+qh615hennjTaZSrg8YHodkHgfHzOYy",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "aweme.snssdk.com",
            "Cookie": f"install_id={iid};",
        }
        sig = self.get_xgorgon(url, '', urlencode(data), 'max', headers)
        headers.update(sig)
        print(headers)
        response = requests.post(url=url, headers=headers, data=data)
        print("最新版搜索", response.text)
        return response.text

    def get_comment(self, video_id, device_id, iid, page=None):
        """
        视频评论
        :param video_id:
        :param device_id:
        :param iid:
        :param page:
        :return:
        """

        if page is None:
            page = '0'

        url = f"https://api3-normal-c.amemv.com/aweme/v2/comment/list/?aweme_id={video_id}" \
              f"&cursor={page}&count=20&insert_ids&address_book_access=2&gps_access=2&forward_page_type=1&channel_id=0" \
              f"&city=360800&hotsoon_filtered_count=0&hotsoon_has_more=0&follower_count=0&is_familiar=0&page_source=0" \
              f"&user_avatar_shrink=64_64&item_type=0&comment_aggregation=0&top_query_word&is_preload=0&channel_ext" \
              f"=%7B%7D&service_id=0&group_id=0&comment_scene=0&hotspot_id&ad_info=&iid={iid}&device_id" \
              f"={device_id}&ac=wifi&channel=update&aid=1128&app_name=aweme&version_code=250900&version_name=25.9" \
              f".0&device_platform=android&os=android&ssmix=a&device_type=MI+9&device_brand=Xiaomi&language=zh&os_api" \
              f"=28&os_version=9&openudid={device['data'][0]['openudid']}&manifest_version_code=250901&resolution=900*1600&dpi=320" \
              f"&update_version_code=25909900&_rticket={round(time.time() * 1000)}" \
              f"&package=com.ss.android.ugc.aweme&mcc_mnc=46000&cpu_support64=true&host_abi=arm64-v8a&is_guest_mode" \
              f"=0&app_type=normal&minor_status=0&appTheme=light&need_personal_recommend=1&is_android_pad=0&ts=" \
              f"{round(time.time())}&uuid={device['data'][0]['uuid']}"

        headers = {
            'Host': 'api3-normal-c.amemv.com',
            'passport-sdk-version': '2036851',
            'sdk-version': '2',
            "activity_now_client": str(int(time.time() * 1000)),
            "X-SS-REQ-TICKET": str(int(time.time() * 1000)),
            'x-tt-store-region': 'cn-jx',
            'x-tt-store-region-src': 'did',
            'x-vc-bdturing-sdk-version': '3.6.1.cn',
            'user-agent': 'com.ss.android.ugc.aweme/250901 (Linux; U; Android 9; zh_CN; MI 9; Build/PQ3B.190801.06161913;tt-ok/3.12.13.1)',
            "Cookie": f"install_id={iid}; "
        }

        sig = self.get_xgorgon(url, '', '', 'max', headers)
        headers.update(sig)

        response = requests.get(url, headers=headers).json()
        print("视频评论", response)
        if len(response['comments']) == 0:
            print(url)
        return response

    def get_live_barrage(self, room_id, cookie, cursor='', internal_ext=''):
        """
        获取直播弹幕流
        :param room_id: 直播间ID
        :param cookie: 网页cookie
        :param cursor: 翻页参数 首页为空下页为本次请求返回的cursor
        :param internal_ext: 翻页参数 首页为空下页为本次请求返回的internal_ext
        :return:
        """

        url = 'https://live.douyin.com/webcast/im/fetch/?aid=6383&app_name=douyin_web&browser_language=zh-CN&browser_name' \
              '=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B' \
              '%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F107.0.0.0%20Safari' \
              '%2F537.36&cookie_enabled=true&cursor={0}&device_platform=web&did_rule=3&fetch_rule=1&identity=audience' \
              '&internal_ext={1}&last_rtt=0&live_id=1&resp_content_type=protobuf&room_id={2}&screen_height' \
              '=1707&screen_width=2560&tz_name=Asia%2FShanghai&version_code=180800'.format(cursor, internal_ext,
                                                                                           room_id)

        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'

        header = {
            'User-Agent': ua,
            'Accept-Encoding': 'gzip, deflate',
            "Referer": "https://live.douyin.com",
            # 'Cookie': cookie
        }
        # sign = self.get_web_sign(url, 'https://live.douyin.com', ua)
        # xbogus = self.get_web_xbogus(url, ua)
        # url += '&X-Bogus=' + xbogus['xbogus'] + '&_signature=' + sign['sign']

        ret = requests.get(url, headers=header, cookies=cookie)
        print('ret.content', ret.content)
        return self.get_pb(base64.b64encode(ret.content))

    def get_pb(self, content):
        """
        解析直播弹幕
        :param content: 弹幕字节流
        :return:
        """
        url = dyapi.host + '/dyapi/live_barrage/get_pb'
        ts = str(time.time()).split('.')[0]
        sign = self.set_sign()
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12',
            "sign": sign,
        }

        resp = requests.post(url, data={'data': content}, headers=header).text
        print('解析直播弹幕：' + resp)
        return resp

    def get_live_barrage_v2(self, room_id, cursor='', internal_ext='', cookie=''):
        """
        获取直播弹幕v2，无需解析
        :param room_id: 直播间ID
        :param cursor: 翻页参数 首页为空下页为本次请求返回的cursor
        :param internal_ext: 翻页参数 首页为空下页为本次请求返回的internal_ext
        :param cookie: 网页cookie
        :return:
        """

        url = dyapi.host + '/dyapi/live_barrage/v2'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        data = {
            "sign": sign,
            "room_id": room_id,
            "cursor": cursor,
            "internal_ext": internal_ext,
            "cookie": cookie
        }

        resp = requests.post(url, data=data, headers=header).text
        print('直播弹幕v2：' + resp)
        return resp

    def get_live_barrage_v3(self, room_id, cursor='', internal_ext='', iid='', device_id=''):
        """
        获取直播弹幕v3
        :param room_id: 直播间ID
        :param cursor: 翻页参数 首页为空下页为本次请求返回的cursor
        :param internal_ext: 翻页参数 首页为空下页为本次请求返回的internal_ext
        :param iid: 设备id
        :param device_id: 设备id
        :return:
        """

        url = dyapi.host + '/dyapi/live_barrage/v3'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        data = {
            "sign": sign,
            "room_id": room_id,
            "cursor": cursor,
            "internal_ext": internal_ext,
            "iid": iid,
            "device_id": device_id
        }

        resp = requests.post(url, data=data, headers=header).text
        print('直播弹幕v3：' + resp)
        return resp

    def re_channel(self):
        channel = ['wandoujia_aweme_feisuo', 'wandoujia_aweme2', 'tengxun_new', 'douyinw', 'douyin_tengxun_wzl',
                   'aweGW', 'aweme_360', 'aweme_tengxun', 'xiaomi']
        return random.choice(channel)

    def get_web_comment(self, vid, page):
        """
        web版获取评论
        :param vid:
        :param page:
        :return:
        """
        url = 'https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel' \
              '=channel_pc_web&aweme_id={0}&cursor={1}&count=20&item_type=0&insert_ids=&rcFT=AAM4H_ZlA' \
              '&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1707' \
              '&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=103.0.0.0' \
              '&browser_online=true&engine_name=Blink&engine_version=103.0.0.0&os_name=Windows&os_version=10' \
              '&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid' \
              '=&msToken='.format(vid, page)

        sign = self.get_web_sign(url, 'https://www.douyin.com/', self.__web_ua)
        xbogus = self.get_web_xbogus(url, self.__web_ua)
        url += '&X-Bogus=' + xbogus['xbogus'] + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'Cookie': ''
        }
        resp = requests.get(url, headers=header).text
        print('web评论列表：', resp)
        return resp

    def get_web_follower(self, sec_uid, page):
        """
        web版获取粉丝
        :param sec_uid:
        :param page:
        :return:
        """

        url = 'https://www.douyin.com/aweme/v1/web/user/follower/list/?device_platform=webapp&aid=6383&channel' \
              '=channel_pc_web&sec_user_id=MS4wLjABAAAAgrpcoLYJIncK6LCPT4A1bDEW2oM12j-PWDvPIWHL7ls&offset=0&min_time' \
              '=0&max_time=' + page + '&count=20&source_type=1&gps_access=0&address_book_access=0&version_code' \
                                      '=170400&version_name=17.4.0&cookie_enabled=true&screen_width=3840&screen_height=2560&browser_language=zh-CN' \
                                      '&browser_platform=Win32&browser_name=Chrome&browser_version=86.0.4240.198&browser_online=true&engine_name=Bl' \
                                      'ink&engine_version=86.0.4240.198&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50'

        sign = self.get_web_sign(url, 'https://www.douyin.com/user/' + sec_uid + '?previous_page=app_code_link',
                                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
        url = url + '&_signature=' + sign['sign']
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie': 'passport_auth_status_ss=d345a1fe9498e99aaae8772c4411a6ac%2C; sid_guard=5029a6aab0d1c73a76bd8904562c3d6f%7C1640241717%7C5184000%7CMon%2C+21-Feb-2022+06%3A41%3A57+GMT; uid_tt=e5b46693845811ea6961be4bbb581ef5; uid_tt_ss=e5b46693845811ea6961be4bbb581ef5; sid_tt=5029a6aab0d1c73a76bd8904562c3d6f;'
                      ' sessionid=5029a6aab0d1c73a76bd8904562c3d6f; sessionid_ss=5029a6aab0d1c73a76bd8904562c3d6f; sid_ucp_v1=1.0.0-KDBhMmI5MTI3YTc2MzZlMmE2ZDI1MDgwNjQzMDQzNzJmM2YwOTU2MTQKFwj4ueCXiPTvAhC1tJCOBhjvMTgGQPQHGgJscSIgNTAyOWE2YWFiMGQxYzczYTc2YmQ4OTA0NTYyYzNkNmY; ssid_ucp_v1=1.0.0-KDBhMmI5MTI3YTc2MzZlMmE2ZDI1'
                      'MDgwNjQzMDQzNzJmM2YwOTU2MTQKFwj4ueCXiPTvAhC1tJCOBhjvMTgGQPQHGgJscSIgNTAyOWE2YWFiMGQxYzczYTc2YmQ4OTA0NTYyYzNkNmY; passport_auth_status=d345a1fe9498e99aaae8772c4411a6ac%2C; MONITOR_WEB_ID=a3043f91-cedf-4682-80b2-922f661e7d27; sso_uid_tt=688f7b503a73fa2ccda15a39cf344910; sso_uid_tt_ss=688f7b503a73fa2c'
                      'cda15a39cf344910; toutiao_sso_user=a652c7ab28cfd5529c9cfcfed5b8435f; toutiao_sso_user_ss=a652c7ab28cfd5529c9cfcfed5b8435f; sid_ucp_sso_v1=1.0.0-KDdhNmE3MWRjY2ViZTRiMWNlMTJjN2QyYzI1M2M1NWRmYTY5YTU0ODUKFwj4ueCXiPTvAhC1tJCOBhjvMTgGQPQHGgJsZiIgYTY1MmM3YWIyOGNmZDU1MjljOWNmY2ZlZDViODQzNWY; ssid_ucp_sso_v1=1'
                      '.0.0-KDdhNmE3MWRjY2ViZTRiMWNlMTJjN2QyYzI1M2M1NWRmYTY5YTU0ODUKFwj4ueCXiPTvAhC1tJCOBhjvMTgGQPQHGgJsZiIgYTY1MmM3YWIyOGNmZDU1MjljOWNmY2ZlZDViODQzNWY; n_mh=lIE_aX9LSJUND6iLw_hHl7uvVSs4g-GUPXO6aWyQCL0; msToken=iC10vixO8xiqyytWVnHo3a7JKKyldHHVl25AcRHyVknIW9wQt_1R3_8y6lKMwkaR-6IkXF9AZaPf3QwEdpUGRWQPfJynl57SXZ9ilY'
                      'vjTM91_dKw2cp76A==; passport_csrf_token_default=41023a9541b61ae05c84ca351a7fbf5c; passport_csrf_token=41023a9541b61ae05c84ca351a7fbf5c; ' +
                      cookie['data'][0]['web_cookie']
        }
        resp = requests.get(url, headers=header).content
        print('web粉丝列表：', resp)
        return resp

    def web_user_search(self, keyword, cookie, page) -> str:
        """
        web版搜索用户
        :param keyword: 搜索关键词
        :param cookie: web
        :param page: 默认0
        :return:
        """
        url = 'https://www.douyin.com/aweme/v1/web/discover/search/?device_platform=webapp&aid=6383&channel' \
              '=channel_pc_web&search_channel=aweme_user_web&keyword=%s&search_source=switch_tab&query_correct_type=1' \
              '&is_filter_search=0&from_group_id=&offset=%s&count=20&search_id=&pc_client_type=1&version_code=170400' \
              '&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN' \
              '&browser_platform=Win32&browser_name=Chrome&browser_version=110.0.0.0&browser_online=true&engine_name' \
              '=Blink&engine_version=110.0.0.0&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform' \
              '=PC&downlink=10&effective_type=4g&round_trip_time=50' % (keyword, page)
        ref = 'https://www.douyin.com/search/%s?source=switch_tab&type=user' % keyword
        # sign = self.get_web_sign(url, ref, self.__web_ua)
        xbogus = self.get_web_xbogus(url, self.__web_ua)
        url += '&X-Bogus=' + xbogus['xbogus']  # + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'referer': ref,
            'Cookie': cookie
        }
        resp = requests.get(url, headers=header).text
        print('web用户搜索列表：', resp)
        return resp

    def web_my_follower(self) -> str:
        """
        web获取自己的粉丝列表
        :return:
        """
        url = 'https://www.douyin.com/aweme/v1/web/user/follower/list/?device_platform=webapp&aid=6383&channel' \
              '=channel_pc_web&user_id=1935590725788205&sec_user_id' \
              '=MS4wLjABAAAAM7F13HAkU5iljq8yBp6WSb7m6Ia028iT00HNWzWyNRlnUSkumJYb8jG6ri5g6W3m&offset=0&min_time=0' \
              '&max_time=1679574528&count=20&source_type=1&gps_access=0&address_book_access=0&pc_client_type=1' \
              '&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864' \
              '&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=111.0.0.0' \
              '&browser_online=true&engine_name=Blink&engine_version=111.0.0.0&os_name=Windows&os_version=10' \
              '&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50'
        ref = 'https://www.douyin.com/user/self'
        sign = self.get_web_sign(url, ref, self.__web_ua)
        xbogus = self.get_web_xbogus(url, self.__web_ua)
        url += '&X-Bogus=' + xbogus['xbogus'] + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'referer': ref,
            'Cookie': 'passport_csrf_token=f20a3ff92fdc81a579374d3e51ffed45; passport_csrf_token_default=f20a3ff92fdc81a579374d3e51ffed45; s_v_web_id=verify_ldlndk0i_N19VDLUA_7oSk_4GZG_Adl1_ryW6rlRCfTEv; ttcid=1ab18e1e09554ddd8297b8a15ab0165144; xgplayer_user_id=934970751508; LOGIN_STATUS=1; store-region=cn-jx; store-region-src=uid; n_mh=KQ-p6faDP5EkFlkMjaqicI6RZzvZ01nR1dSjk560S14; d_ticket=3f3ff3a64c5fbacb967e00ba35f6d08fbcce5; publish_badge_show_info="0,0,0,1679293080807"; _tea_utm_cache_10006=undefined; _tea_utm_cache_6247=undefined; _tea_utm_cache_1243=undefined; MONITOR_WEB_ID=f58cdd7b-7773-4cc6-b546-a3bac43d43cb; ttwid=1|fV_pvne8oMRuOmMsyU5GTAk3RJyIt2whEHUFb28fD8I|1679295647|50986abae4b47c748306c6da1e6a0fa1e60d675cfe6313bf2dc948f66cfa75a9; SEARCH_RESULT_LIST_TYPE="single"; download_guide="3/20230321"; FOLLOW_LIVE_POINT_INFO="MS4wLjABAAAAM7F13HAkU5iljq8yBp6WSb7m6Ia028iT00HNWzWyNRlnUSkumJYb8jG6ri5g6W3m/1679414400000/0/0/1679383305927"; strategyABtestKey="1679568116.481"; passport_assist_user=CkG6XT9RNO-kTFz_cUa7rPie40nC5fmfBeiw-3R3u48fmaR_B6JbBktRSw_HKJ2WEgOYt3pOb2xhWfyizoqygG1hdhpICjwk4U-Whi6BGVKopoU-jcT-Jdgta23ZRDiN4qhvv-5YxHWVObQJG3jJ5VXAzwBATRsuMw0xrBW6PxD6dTIQ88SsDRiJr9ZUIgEDkwqHgA==; sso_uid_tt=2de736ee679a93288f1d1854a0985f65; sso_uid_tt_ss=2de736ee679a93288f1d1854a0985f65; toutiao_sso_user=229b5eff65d30531ca152e1ba4ca1881; toutiao_sso_user_ss=229b5eff65d30531ca152e1ba4ca1881; sid_ucp_sso_v1=1.0.0-KGM0MmQ1M2M4ZTViNjhkZDllNDEyNmFhNmY2NmU4Mjk5OTk2NDljMmUKIQitxJCtjY24AxD22fCgBhjvMSAMMNa4tYQGOAVA-wdIAxoCbHEiIDIyOWI1ZWZmNjVkMzA1MzFjYTE1MmUxYmE0Y2ExODgx; ssid_ucp_sso_v1=1.0.0-KGM0MmQ1M2M4ZTViNjhkZDllNDEyNmFhNmY2NmU4Mjk5OTk2NDljMmUKIQitxJCtjY24AxD22fCgBhjvMSAMMNa4tYQGOAVA-wdIAxoCbHEiIDIyOWI1ZWZmNjVkMzA1MzFjYTE1MmUxYmE0Y2ExODgx; odin_tt=84093224bd43f104588b104ee91247e73a214153e1e24bb8e170a9200a7b7272f5bd2f3da203da0294736832a4cf567e03d1cae3d5385ae2c899b8600dcfba84; uid_tt=01c7463fb5c7e609938359902f49415a; uid_tt_ss=01c7463fb5c7e609938359902f49415a; sid_tt=796b5cac70aa184aac6afcdb522235a2; sessionid=796b5cac70aa184aac6afcdb522235a2; sessionid_ss=796b5cac70aa184aac6afcdb522235a2; sid_guard=796b5cac70aa184aac6afcdb522235a2|1679568121|5183996|Mon,+22-May-2023+10:41:57+GMT; sid_ucp_v1=1.0.0-KGNlM2JkMzk1ZGY4NGFjNzFmOGZmZjc4MTRiZWI0YTg0MDhkNTdhMDEKGwitxJCtjY24AxD52fCgBhjvMSAMOAVA-wdIBBoCaGwiIDc5NmI1Y2FjNzBhYTE4NGFhYzZhZmNkYjUyMjIzNWEy; ssid_ucp_v1=1.0.0-KGNlM2JkMzk1ZGY4NGFjNzFmOGZmZjc4MTRiZWI0YTg0MDhkNTdhMDEKGwitxJCtjY24AxD52fCgBhjvMSAMOAVA-wdIBBoCaGwiIDc5NmI1Y2FjNzBhYTE4NGFhYzZhZmNkYjUyMjIzNWEy; __ac_nonce=0641c45b500fe1f25e1da; __ac_signature=_02B4Z6wo00f01iu26twAAIDCq7QQn0kk8DYrlu5AAO8AZWAFUqanP06RNcBNyhP.5fh.rvXQMdlLIpgpkFRcAtONAYMBUK1wREpF8elGK8Jb.jMhrvuE-KZ2-svrqjZ0QViqzYW61lq.tAEyb1; douyin.com; VIDEO_FILTER_MEMO_SELECT={"expireTime":1680179257071,"type":1}; csrf_session_id=700eb3f83137527fd9d2773bb6604e7e; FOLLOW_NUMBER_YELLOW_POINT_INFO="MS4wLjABAAAAM7F13HAkU5iljq8yBp6WSb7m6Ia028iT00HNWzWyNRlnUSkumJYb8jG6ri5g6W3m/1679587200000/0/0/1679575657382"; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jZXJ0IjoiLS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tXG5NSUlDRkRDQ0FicWdBd0lCQWdJVVVhYjJYTEF4d21jVkljU1RGMEE1UE82OUpDMHdDZ1lJS29aSXpqMEVBd0l3XG5NVEVMTUFrR0ExVUVCaE1DUTA0eElqQWdCZ05WQkFNTUdYUnBZMnRsZEY5bmRXRnlaRjlqWVY5bFkyUnpZVjh5XG5OVFl3SGhjTk1qTXdNakF6TURVeU5qTTFXaGNOTXpNd01qQXpNVE15TmpNMVdqQW5NUXN3Q1FZRFZRUUdFd0pEXG5UakVZTUJZR0ExVUVBd3dQWW1SZmRHbGphMlYwWDJkMVlYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEXG5BUWNEUWdBRVQ1ZHE5Q2llbURJdWF6Ly9iMEpyQktSUzdUMVlCMFU4RUJjMHF6LzkvelgyNzNIWkdqMFRHeHFmXG5BcHdONno0b3NSa3VnL2JBd2VhOVlxWkZFRXVTNGFPQnVUQ0J0akFPQmdOVkhROEJBZjhFQkFNQ0JhQXdNUVlEXG5WUjBsQkNvd0tBWUlLd1lCQlFVSEF3RUdDQ3NHQVFVRkJ3TUNCZ2dyQmdFRkJRY0RBd1lJS3dZQkJRVUhBd1F3XG5LUVlEVlIwT0JDSUVJQ3RDUVY3UlM3UXdYR2w4cUJoWU1adk11WWhWSURvckViNWZDekswK0xxb01Dc0dBMVVkXG5Jd1FrTUNLQUlES2xaK3FPWkVnU2pjeE9UVUI3Y3hTYlIyMVRlcVRSZ05kNWxKZDdJa2VETUJrR0ExVWRFUVFTXG5NQkNDRG5kM2R5NWtiM1Y1YVc0dVkyOXRNQW9HQ0NxR1NNNDlCQU1DQTBnQU1FVUNJUUNBY0VjRUM5ZVNxODJPXG5hVVU0QVhpYU5kNnlOMExGRmhYallidjY1V205UEFJZ0o3Rk91d1l2WE5ZMFFwVzhpVnNuWnltdEdteG1jNWJYXG5ISGNIeTMyTEVXbz1cbi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS1cbiJ9; msToken=Z9D1QOzp4LLjRhl7LXOgwfON5yfxZ9ybUmT2xw6jlSea4iu6BEp1wW3AwxhEv_9GA57r_pKre-KWuZ24rGlds7bh3ogmeUz2H47OFOt8wS7H-Oo8mXhfUA==; tt_scid=uyzBkRIJtK1Ty0HYk83HVuL8SpYnpZEr9woVMQrHCrkhpyZht6reBEJHTLM7T6xO9653; pwa2="2|1"; my_rd=1; home_can_add_dy_2_desktop="1"; passport_fe_beating_status=true; msToken=8XJdwmDjUsZUAYeEwnvh-pfgV56R1dAr3FP2CRI6MDIkN2hnq3TFQu86iA1Q2nEaK2rqzZrUqVRvDe1Pbhm5LR5jxkr1nqUr8rCYYVNEwGri23o10bDdIQ=='
        }
        resp = requests.get(url, headers=header).text
        print('web获取自己的粉丝列表：', resp)
        return resp

    def web_video_search(self, keyword, page=None):
        """
        web版获取搜索视频
        :param keyword:搜索关键词
        :param page:
        :return:
        """
        url = 'https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=0&publish_time=0&' \
              'keyword=' + keyword + '&search_source=normal_search&query_correct_type=1&is_filter_search=0&offset=' + str(
            page) + '&count=30&version_code=160100&version_name=16.1.0&cookie_enable' \
                    'd=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+WOW64)+AppleWe' \
                    'bKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F86.0.4240.198+Safari%2F537.36&browser_online=true'
        ref = 'https://www.douyin.com/search/' + keyword + '?source=normal_search'
        sign = self.get_web_sign(url, ref, self.__web_ua)
        url = url + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'referer': ref,
            'Cookie': self.get_web_cookie()
        }

        resp = requests.get(url, headers=header).text
        print('web视频搜索列表：', resp)
        return resp

    def get_web_video(self, sec_uid, page, cookie):
        """
        web版获取主页作品
        :param sec_uid:
        :param page:
        :param cookie:
        :return:
        """
        url = 'https://www.douyin.com/aweme/v1/web/locate/post/?device_platform=webapp&aid=6383&channel' \
              '=channel_pc_web&sec_user_id=%s&max_cursor=0&locate_item_id=7215521171238931749&locate_item_cursor=1679816897000&locate_query' \
              '=true&count=10&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0' \
              '&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32' \
              '&browser_name=Firefox&browser_version=111.0&browser_online=true&engine_name=Gecko&engine_version=109.0' \
              '&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=&platform=PC' % sec_uid

        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'

        sign = self.get_web_sign(url, 'https://www.douyin.com/', ua)
        xbogus = self.get_web_xbogus(url, ua)
        url += '&X-Bogus=' + xbogus['xbogus'] + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'referer': 'https://www.douyin.com/',
            'cookie': cookie
        }
        resp = requests.get(url, headers=header).text
        print('web作品列表：', resp)
        return resp

    def get_ac_sign(self, ac_nonce):
        """
        ac_sign
        :param ac_nonce:
        :return:
        """
        url = dyapi.host + '/dyapi/web/ac_sign'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'User-Agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        resp = requests.post(url, data={'sign': sign, 'ac_nonce': ac_nonce}, headers=header).text
        print('ac_sign:', resp)
        return resp

    def get_video_info(self, video_list: list) -> str:
        """
        测试获取视频信息接口
        :param video_list: 视频列表
        :return:
        """
        url = dyapi.host + '/video_info'
        resp = requests.post(url, data={'video_list': str(video_list)}).text
        print('视频信息列表:', resp)
        return resp

    def get_cookie(self):
        header = {
            'Referer': 'https://www.douyin.com/',
            'x-tt-passport-csrf-token': '',
            'User-Agent': self.__web_ua
        }
        ret = requests.get('https://www.douyin.com/', headers=header)
        cookie_1 = requests.utils.dict_from_cookiejar(ret.cookies)
        # print('得到最初cookie', cookie_1)
        url = 'https://sso.douyin.com/get_qrcode/?service=https%3A%2F%2Fwww.douyin.com%2F&need_logo=false&aid=6383'
        header['Cookie'] = urlencode(cookie_1)
        ret = requests.get(url, headers=header)
        cookie_2 = requests.utils.dict_from_cookiejar(ret.cookies)
        # print('得到token', cookie_2)
        cookie = dict()
        cookie.update(cookie_1)
        cookie.update(cookie_2)
        print('cookie合并后', cookie)
        return cookie

    def get_web_cookie(self):
        """
        获取滑块后的cookie
        :return:
        """
        url = dyapi.host + '/dyapi/get_cookie/v2'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        resp = requests.post(url, data={'sign': sign}, headers=header).json()
        return resp['data'][0][0]

    def get_room_id(self, live_url):
        """
        网页直播链接转直播id
        :param live_url: 网页版直播链接
        :return:
        """
        url = 'http://www.52jan.com/dyapi/web/get_room_id'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts
        }
        sign = self.set_sign()
        resp = requests.post(url, data={'sign': sign, 'url': live_url}, headers=header).text
        # print('获取直播id', resp)
        return resp

    def set_sign(self):
        """
        计算本api签名
        :return:
        """
        ts = str(time.time()).split('.')[0]
        string = '1005' + self.cid + ts + self.__appkey
        sign = hashlib.md5(string.encode('utf8')).hexdigest()
        print('本api的sign', sign)
        return sign


if __name__ == '__main__':
    api = dyapi('d9ba8ae07d955b83c3b04280f3dc5a4a')
    api.get_appkey()

    # 通过直播链接转直播间id
    # live_url = 'https://live.douyin.com/158893494907'
    # room_id = api.get_room_id(live_url)
    # print('room_id:', room_id)

    ApiInfo = api.get_ApiInfo()
    print('到期时间:' + ApiInfo)

    # app取设备号
    device = api.get_device()

    # ac_sign
    # api.get_ac_sign('')

    # web版获取cookie
    cookie = api.get_web_cookie()
    print('ret_cookie:', cookie)

    vid = '7244717478532762936'
    page = 0

    token = '00470bbfeb49d95c2ca1e26ac4a1dd510f0384dbdf2f3665dd4bd0714bd8a76157a7058d65daa90d26694f0d385459aa4ab5929223fadc1d5d4c6eaec97cb70c4ede68a69a8853fa2a41b7018eedde0ec5ddd920f0d3e174de2cdccc94b4cfd0e140b-1.0.1'
    # api.get_qishui()

    # 获取web作品列表
    # api.get_web_video('MS4wLjABAAAA2Ixr52FdZXzowS37S8bhgGYUcruovygBNDqOtBxFfvI', page, cookie)

    # 获取直播弹幕
    cursor = ''
    internalExt = ''
    room_id = '7195168871676906277'

    device_id = device['data'][0]['device_id']
    iid = device['data'][0]['install_id']
    # for i in range(3):
    #     ret = api.get_live_barrage_v2(room_id=room_id, cursor=cursor, internal_ext=internalExt, cookie=cookie)
    #     # messages = api.get_live_barrage_v3(room_id=room_id, cursor=cursor, internal_ext=internalExt, iid=iid, device_id=device_id)
    #     # ret = api.get_pb(messages)
    #     res = json.loads(ret)
    #     try:
    #         cursor = res['cursor']
    #         internalExt = res['internalExt']
    #         if i >= 2:
    #             print("正在直播：" + cursor)
    #     except KeyError:
    #         print("下播了去别处看看吧")
    #         break
    #     time.sleep(3)

    # web获取视频信息
    # video_list = [7206592982118616324, 7180333041812819237, 7212918206074309899]
    # api.get_video_info(video_list)
    sec_uid = 'MS4wLjABAAAA9dd_xgKqu5ADzkYWr1GINkW5E8NRNCgaywN2RMCZbq3Jqu-rsvkJ6hHZ4WBxbgxJ'

    # 获取web评论示例
    # api.get_web_comment(vid, 10)

    # 获取web粉丝列表
    # api.get_web_follower(sec_uid, str(time.time()))

    import urllib

    keyword = urllib.parse.quote('哈士奇')
    # web用户搜索
    # api.web_user_search(keyword, cookie, "0")

    # 获取自己的粉丝列表
    # api.web_my_follower()

    # app视频搜索
    # api.get_keyword(device_id, iid, keyword, "12")

    # web视频搜索
    # api.web_video_search(keyword, page)

    # 获取评论示例
    # device_id=4323692175176509 install_id=2184085302687243
    api.get_comment(vid, device_id="4323692175176509", iid="2184085302687243", page='0')
