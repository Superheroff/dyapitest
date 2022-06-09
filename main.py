import requests
import json
import time
from urllib.parse import urlencode
import random
import hashlib

class dyapi:
    # 主
    host = 'https://api2.52jan.com'
    # 备
    # host = 'https://api.app966.cn'



    COMMON_DEVICE_PARAMS = {
        'address_book_access': '2',
        'retry_type': 'no_retry',
        'ac': 'wifi',
        'channel': 'tengxun_new',
        'aid': '1128',
        'app_name': 'aweme',
        'version_code': '11060',
        'version_name': '11.6.0',
        'device_platform': 'android',
        'ssmix': 'a',
        'device_type': '2014813',
        'device_brand': 'Xiaomi',
        'language': 'zh',
        'os_api': '22',
        'os_version': '5.1.1',
        'manifest_version_code': '110601',
        'resolution': '720*1280',
        'dpi': '320',
        'update_version_code': '11609900',
        'app_type': 'normal',
        'host_abi': 'armeabi-v7a',
        'cpu_support64': 'false'
    }

    proxies = {'https': 'https://togk71z9.xiaomy.net:44510'}

    def __init__(self, cid):
        self.cid = cid
        self.array = {}
        self.__web_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        self.__appkey = ''
        self.__params = {
            'address_book_access': '1',
            'client_niu_ready': 'false',
            'os_api': '22',
            'device_type': 'MI%209',
            'ssmix': 'a',
            'manifest_version_code': '120000',
            'dpi': '240',
            'app_name': 'douyin_lite',
            'version_name': '12.0.0',
            'ts': str(int(time.time())),
            'app_type': 'normal',
            'ac': 'wifi',
            'update_version_code': '12009900',
            'channel': self.re_channel(),
            '_rticket': str(time.time() * 1000).split(".")[0],
            'device_platform': 'android',
            'tool_grey_user': '0',
            'version_code': '120000',
            'resolution': '720*1280',
            'os_version': '5.1.1',
            'language': 'zh',
            'device_brand': 'Android',
            'mcc_mnc': '46007'
    }

    def get_appkey(self):
        # 获取appkey
        data = self.cid + '5c6b8r9a'
        self.__appkey = hashlib.sha256(data.encode('utf-8')).hexdigest()
        print('appkey', self.__appkey)

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

    def get_xgorgon(self, url, cookie, params, ver):
        '''
        获取x-gorgon
        :param url:
        :param cookie:
        :param params: post提交
        :param ver: 版本号
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
        resp = requests.post(sign_url, data=self.array, headers=header).json()
        print('xgorgon', resp)
        return resp

    def get_ApiInfo(self):
        """
        获取接口使用情况
        :return:
        """
        url = dyapi.host + '/end_time'
        print(url)
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

    def get_follow(self, uid, page, count, token, fans):
        '''
        获取粉丝/关注列表（抖音版）
        :param uid: 抖音uid
        :param page: 翻页
        :param count: 每次返回的数量 最多49
        :param token:
        :param fans: 是否获取粉丝列表 True=粉丝
        :return:
        '''

        if fans is True:
            ty = 'follower'
        else:
            ty = 'following'

        if uid.find('M') != -1:
            idz = 'sec_user_id'
        else:
            idz = 'user_id'

        num_1 = str(random.randint(10, 99))
        num_2 = str(random.randint(0, 9))
        num_3 = str(random.randint(0, 9))
        version_name = num_1 + '.' + num_2 + '.' + num_3
        version_code = num_1 + '0' + num_2 + '0' + num_3
        params = {
            idz: uid,
            'device_id': device['data'][0]['device_id'],
            'iid': device['data'][0]['install_id'],
            "channel": ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', random.randint(2, 7))),
            "version_name": version_name,
            "version_code": version_code,
            "cursor": page,
            "count": count,
            "": "insert_ids",
            "address_book_access": 2,
            "gps_access": 2,
            "forward_page_type": 1,
            "channel_id": 3,
            "city": 0,
            "os_api": 23,
            "device_type": "Nexus 5",
            "ssmix": "a",
            "manifest_version_code": 130901,
            "dpi": 480,
            "app_name": "aweme",
            "app_type": "normal",
            "appTheme": "dark",
            "ac": "wifi",
            "host_abi": "armeabi-v7a",
            "device_platform": "android",
            "resolution": "1080*1776",
            "os_version": "6.0.1",
            "language": "zh",
            "device_brand": "google",
            "aid": 1128

        }
        url = 'https://aweme.snssdk.com/aweme/v1/user/' + ty + '/list/?' + urlencode(params)
        sig = self.get_xgorgon(url, '', '', '0408')
        headers = {
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '17',
            'sdk-version': '2',
            'X-SS-REQ-TICKET': sig['X-SS-REQ-TICKET'],
            'X-SS-DP': '1128',
            'X-Tt-Token': token,
            'User-Agent': 'okhttp/3.10.0.1'
        }
        req = requests.get(url, headers=headers).text
        js = json.loads(req)
        code = int(js['status_code'])
        if code == 2096:
            resp = '获取失败，该用户粉丝/关注列表已被隐藏'
        else:
            resp = req
        print('用户粉丝/关注列表', resp)
        return resp


    def get_user_search(self, keyword, page, token):
        """
        获取用户搜索列表(抖音极速版)
        :param keyword: 关键词
        :param page: 首页为0，下一页为本次请求返回的max_cursor
        :return:
        """

        params = {
            'keyword': keyword,
            'type': '1',
            'is_pull_refresh': '1',
            'count': '20',
            'cursor': str(page),
            'hot_search': '0',
            'search_source': '',
            'search_id': '',
            'query_correct_type': '1'

        }

        self.__params.update({'uuid': device['data'][0]['uuid']})
        self.__params.update({'device_id': device['data'][0]['device_id']})
        self.__params.update({'iid': device['data'][0]['install_id']})
        self.__params.update({'openudid': device['data'][0]['openudid']})
        self.__params.update({'mac_address': device['data'][0]['mac']})
        self.__params.update({'aid': '2329'})
        url = 'https://search-hl.amemv.com/aweme/v1/discover/search/?' + urlencode(self.__params)
        sig = self.get_xgorgon(url, '', urlencode(params), '0404')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme.lite/120000 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; Cronet/TTNetVersion:a87ab8c7 2020-11-24 QuicVersion:47946d2a 2020-10-14)',
            'X-SS-REQ-TICKET': str(time.time() * 1000).split(".")[0],
            'X-SS-DP': '2329',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '19',
            'X-Tt-Token': token
        }
        resp = requests.post(url, data=params, headers=header).text
        print('用户搜索列表：' + resp)
        return resp



    def get_video_search(self, keyword, page, token):
        """
        获取视频搜索列表(抖音极速版)
        综合排序：is_filter_search=0，sort_type=0
        按热门：is_filter_search=1，sort_type=1
        按最新：is_filter_search=1，sort_type=2
        :param keyword: 关键词
        :param page: 首页为0，下一页为本次请求返回的max_cursor
        :return:
        """

        params = {
            'keyword': keyword,
            'from_user': '',
            'source': 'video_search',
            'count': '20',
            'search_source': 'switch_tab',
            'offset': str(page),
            'is_pull_refresh': '1',
            'hot_search': '',
            'search_id': '',
            'query_correct_type': '1',
            'is_filter_search': '0',
            'sort_type': '0',
            'publish_time': '0',
            'enter_from': 'homepage_hot',
            'backtrace': '',
            'user_avatar_shrink': '64_64',
            'video_cover_shrink': '372_496'

        }

        n = random.randint(0,len(device['data'][0]['uuid'])-1)

        self.__params.update({'uuid': device['data'][0]['uuid'][n]})
        self.__params.update({'device_id': device['data'][0]['device_id'][n]})
        self.__params.update({'iid': device['data'][0]['install_id'][n]})
        self.__params.update({'openudid': device['data'][0]['openudid'][n]})
        self.__params.update({'mac_address': device['data'][0]['mac'][n]})
        self.__params.update({'aid': '2329'})
        url = 'https://search-lf.amemv.com/aweme/v1/search/item/?' + urlencode(self.__params)
        sig = self.get_xgorgon(url, '', urlencode(params), '0404')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme.lite/120000 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; Cronet/TTNetVersion:a87ab8c7 2020-11-24 QuicVersion:47946d2a 2020-10-14)',
            'X-SS-REQ-TICKET': str(time.time() * 1000).split(".")[0],
            'X-SS-DP': '2329',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '19',
            'X-Tt-Token': token
        }
        resp = requests.post(url, data=params, headers=header).text
        print('视频搜索列表：' + resp)
        return resp


    def get_userinfo(self, uid):
        """
        获取用户信息(抖音极速版)
        :param uid: uid
        :return:
        """
        self.__params.update({'user_id': uid})
        self.__params.update({'uuid': device['data'][0]['uuid']})
        self.__params.update({'device_id': device['data'][0]['device_id']})
        self.__params.update({'iid': device['data'][0]['install_id']})
        self.__params.update({'openudid': device['data'][0]['openudid']})
        self.__params.update({'mac_address': device['data'][0]['mac']})
        self.__params.update({'aid': '2329'})
        url = 'https://api5-core-c-hl.amemv.com/aweme/v1/user/?' + urlencode(self.__params)
        sig = self.get_xgorgon(url, '', '', '')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme.lite/120000 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; Cronet/TTNetVersion:a87ab8c7 2020-11-24 QuicVersion:47946d2a 2020-10-14)',
            'X-SS-REQ-TICKET': str(time.time() * 1000).split(".")[0],
            'X-SS-DP': '2329',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '19'
        }
        resp = requests.get(url, headers=header).text
        print('用户信息：' + resp)
        return resp

    def get_favorite(self, vid, page, pg, token):
        """
        获取作品点赞
        :param vid: vid
        :param page: 首页为0，下一页为本次请求返回的max_cursor
        :return:
        """
        url = 'https://api3-normal-c-lq.amemv.com/aweme/v1/favorite/list/?item_id='+vid+'&item_type=0&max_cursor='+str(page)+'&min_cursor='+str(pg)+'&count=30&' \
              'insert_ids&address_book_access=2&hotsoon_filtered_count=0&hotsoon_has_more=0&aweme_filtered_count=2&os_api=22&device_type='+device['data'][0]['device_type']+'&ssmix=a&manifest_version_code=150801&' \
              'dpi=240&uuid='+device['data'][0]['uuid']+'&app_name=aweme&version_name=15.8.0&ts='+str(time.time())+'&cpu_support64=false&storage_type=0&app_type=normal&ac=wifi&host_abi=armeabi-v7' \
              'a&update_version_code=15809900&channel=aweGW&_rticket='+str(time.time() * 1000).split(".")[0]+'&device_platform=android&iid='+device['data'][0]['install_id']+'&version_code=150800&' \
              'mac_address='+device['data'][0]['mac']+'&cdid='+device['data'][0]['cdid']+'&openudid='+device['data'][0]['openudid']+'&device_id='+device['data'][0]['device_id']+'&resolution=720*1280&os_version=5.1.1&language=zh&device_brand' \
              '='+device['data'][0]['device_brand']+'&aid=1128&mcc_mnc=46007'
        sig = self.get_xgorgon(url, '', '', '')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme/150801 (Linux; U; Android 5.1.1; zh_CN; '+device['data'][0]['device_type']+'; Build/NMF26X; Cronet/TTNetVersion:71e8fd11 2020-06-10 QuicVersion:7aee791b 2020-06-05',
            'X-SS-REQ-TICKET': str(time.time() * 1000).split(".")[0],
            'X-SS-DP': '1128',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '17',
            'X-Tt-Token': token

        }
        resp = requests.get(url, headers=header).text
        print('获取作品点赞：' + resp)
        return resp


    def get_video(self, uid, page, token):
        """
        获取作品列表
        :param uid: uid
        :param page: 首页为0，下一页为本次请求返回的max_cursor
        :return:
        """
        self.__params.update({'max_cursor': str(page)})
        self.__params.update({'user_id': uid})
        self.__params.update({'count': '20'})
        self.__params.update({'uuid': device['data'][0]['uuid']})
        self.__params.update({'device_id': device['data'][0]['device_id']})
        self.__params.update({'iid': device['data'][0]['install_id']})
        self.__params.update({'openudid': device['data'][0]['openudid']})
        self.__params.update({'mac_address': device['data'][0]['mac']})
        self.__params.update({'aid': '2329'})
        url = 'https://api5-core-c-hl.amemv.com/aweme/v1/aweme/post/?source=0&' + urlencode(self.__params)
        sig = self.get_xgorgon(url, '', '', '')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme.lite/120000 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; Cronet/TTNetVersion:a87ab8c7 2020-11-24 QuicVersion:47946d2a 2020-10-14)',
            'X-SS-REQ-TICKET': str(time.time() * 1000).split(".")[0],
            'X-SS-DP': '2329',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '19',
            'X-Tt-Token': token

        }
        resp = requests.get(url, headers=header).text
        print('作品列表：' + resp)
        return resp

    def get_video_comment(self, vid, page):
        """
        获取作品评论列表
        :param vid: 视频id
        :param page: 首页为0，下一页为本次请求返回的max_cursor
        :return:
        """
        n = str(random.randint(0, 9))
        url = 'https://api3-normal-c-hl.amemv.com/aweme/v2/comment/list/?address_book_access=1&client_niu_ready=false&os_api=22&device_type=MI%25209&ssmix=a&manifest_version_code=120'+n+'00&dpi=240&app_name=douyin_lite&' \
              'version_name=12.'+n+'.0&ts='+str(time.time()).split(".")[0]+'&app_type=normal&ac=wifi&update_version_code=12'+n+'09900&channel='+self.re_channel()+'&_rticket='+str(time.time() * 1000).split(".")[0]+'&device_platform=android&tool_grey_user=0&version_code=120'+n+'00&' \
              'resolution=720%2A1280&os_version=5.1.1&language=zh&device_brand=Android&mcc_mnc=46007&cursor='+str(page)+'&cdid='+device['data'][0]['cdid']+'&count=20' \
              '&aweme_id='+vid+'&uuid='+device['data'][0]['uuid']+'&device_id='+device['data'][0]['device_id']+'&iid='+device['data'][0]['install_id']+'&openudid='+device['data'][0]['openudid']+'&mac_address='+device['data'][0]['mac']+'&aid=2329'

        sig = self.get_xgorgon(url, '', '', '0408')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme.lite/120'+n+'00 (Linux; U; Android 5.1.1; zh_CN; TAS-AN00; Build/TAS-AN00; Cronet/TTNetVersion:414feb46 2020-09-08 QuicVersion:7aee791b 2020-06-05)',
            'X-SS-REQ-TICKET': sig['X-SS-REQ-TICKET'],
            'X-SS-DP': '2329',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '19',
            'x-tt-dt': device['data'][0]['device_token']

        }

        resp = requests.get(url, headers=header).text
        print('极速评论列表：' + resp)
        return resp

    def api_get_comment(self, vid, page):
        '''
        获取评论列表
        :param vid:视频ID
        :param page:页
        :return:
        '''
        sign = self.set_sign()
        url = dyapi.host + '/dyapi/get_comment?sign=' + sign
        ts = str(time.time()).split('.')[0]
        data = {
            'aweme_id': vid,
            'page': str(page)

        }

        header = {
            'cid': self.cid,
            'timestamp': ts
        }

        resp = requests.post(url, data=data, headers=header).text
        print('app评论列表：' + resp)
        return resp


    def api_get_follow(self, uid, page, ty=''):
        '''
        获取粉丝or关注列表
        :param uid:纯数字uid或sec_uid
        :param page:页
        :param ty:可空，默认为粉丝，1=关注
        :return:
        '''
        sign = self.set_sign()
        url = dyapi.host + '/dyapi/get_follow?sign=' + sign
        ts = str(time.time()).split('.')[0]
        data = {
            'uid': uid,
            'page': str(page),
            'type': ty,
            'iid': device["data"][0]["install_id"],
            'device_id': device["data"][0]["device_id"]
        }

        header = {
            'cid': self.cid,
            'timestamp': ts
        }

        resp = requests.post(url, data=data, headers=header).text
        print('粉丝/关注列表：' + resp)
        return resp

    def get_shop_header(self, uid, token):
        """
        获取带货口碑
        :param uid:
        :param page:
        :return:
        """
        self.__params.update({'merge_product_status': '0'})
        self.__params.update({'author_id': uid})
        self.__params.update({'size': '10'})
        self.__params.update({'uuid': device['data'][0]['uuid']})
        self.__params.update({'device_id': device['data'][0]['device_id']})
        self.__params.update({'iid': device['data'][0]['install_id']})
        self.__params.update({'openudid': device['data'][0]['openudid']})
        self.__params.update({'mac_address': device['data'][0]['mac']})
        self.__params.update({'aid': '1128'})

        url = 'https://api3-normal-c-lf.amemv.com/aweme/v1/shop/header/?' + urlencode(self.__params)
        sig = self.get_xgorgon(url, '', '', '')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme.lite/120000 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; Cronet/TTNetVersion:a87ab8c7 2020-11-24 QuicVersion:47946d2a 2020-10-14)',
            'X-SS-REQ-TICKET': str(time.time() * 1000).split(".")[0],
            'X-SS-DP': '1128',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '18',
            'X-Tt-Token': token
        }
        resp = requests.get(url, headers=header).text
        print('带货口碑：' + resp)
        return resp


    def get_shop_product(self, uid, page, token):
        """
        获取橱窗列表
        :param uid:
        :param page:
        :return:
        """
        self.__params.update({'cursor': str(page)})
        self.__params.update({'author_id': uid})
        self.__params.update({'size': '10'})
        self.__params.update({'uuid': device['data'][0]['uuid']})
        self.__params.update({'device_id': device['data'][0]['device_id']})
        self.__params.update({'iid': device['data'][0]['install_id']})
        self.__params.update({'openudid': device['data'][0]['openudid']})
        self.__params.update({'mac_address': device['data'][0]['mac']})
        self.__params.update({'aid': '1128'})

        url = 'https://api5-normal-c-lf.amemv.com/aweme/v1/shop/product/list/?' + urlencode(self.__params)
        sig = self.get_xgorgon(url, '', '', '')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme.lite/120000 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; Cronet/TTNetVersion:a87ab8c7 2020-11-24 QuicVersion:47946d2a 2020-10-14)',
            'X-SS-REQ-TICKET': str(time.time() * 1000).split(".")[0],
            'X-SS-DP': '1128',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '18',
            'X-Tt-Token': token
        }
        resp = requests.get(url, headers=header).text
        print('橱窗列表：' + resp)
        return resp

    def get_shop_promotions(self, uid, room_id, token):
        """
        获取直播间商品列表
        :param uid:
        :param room_id:
        :return:
        """

        url = 'https://lianmengapi-lf.snssdk.com/live/promotions/?author_id='+uid+'&sec_author_id=&room_id='+room_id+'&entrance_info=&first_enter=false&auto_apply_coupon=false&manifest_version_code=130801&_rticket='+str(time.time() * 1000).split(".")[0]+'&app_type=norma' \
                'l&iid='+device['data'][0]['install_id']+'&channel=wandoujia_1128_1130&device_type=MI+6X&language=zh&cpu_support64=true&host_abi=armeabi-v7a&uuid='+device['data'][0]['uuid']+'&resolution=1080*2030&openudid' \
                 '='+device['data'][0]['openudid']+'&update_version_code=13809900&cdid='+device['data'][0]['cdid']+'&appTheme=dark&os_api=28&dpi=440&ac=wifi&device_id='+device['data'][0]['device_id']+'&os_versi' \
                 'on=9&version_code=130800&app_name=aweme&version_name=13.8.0&device_brand=xiaomi&ssmix=a&device_platform=android&aid=1128&ts='+str(time.time())
        sig = self.get_xgorgon(url, '', '', '')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme/130801 (Linux; U; Android 9; zh_CN; MI 6X; Build/PKQ1.180904.001; Cronet/TTNetVersion:58eeeb7f 2020-11-03 QuicVersion:47946d2a 2020-10-14)',
            'X-SS-REQ-TICKET': str(time.time() * 1000).split(".")[0],
            'X-SS-DP': '1128',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '18',
            'X-Tt-Token': token
        }
        resp = requests.get(url, headers=header).text
        print('直播间商品列表：' + resp)
        return resp


    def get_shop_ranklist(self, sec_uid, room_id, token):
        """
        获取带货榜
        :param sec_uid:
        :param room_id:
        :return:
        """

        url = 'https://webcast5-normal-c-lf.amemv.com/webcast/ranklist/hour/?room_id='+room_id+'&sec_anchor_id='+sec_uid+'&hour_info=0&' \
              'sec_user_id=&style=3&rank_type=31&webcast_sdk_version=1790&webcast_language=zh&webcast_locale=zh_CN' \
              '&webcast_gps_access=1&current_network_quality_info=&manifest_version_code=130801&_rticket='+str(time.time() * 1000).split(".")[0]+'&app_type=' \
              'normal&iid='+device['data'][0]['install_id']+'&channel=wandoujia_1128_1130&device_type=MI+6X&language=zh&cpu_support64=true&host_abi=armeabi-v7a&uuid='+device['data'][0]['uuid']+'&resolution=1080*2030&openudid='+device['data'][0]['openudid']+'&upda' \
              'te_version_code=13809900&cdid='+device['data'][0]['cdid']+'&appTheme=dark&os_api=28&dpi=440&ac=wifi&device_id='+device['data'][0]['device_id']+'&os_version=9&version_code=130800&app_name=aweme&versio' \
              'n_name=13.8.0&device_brand=xiaomi&ssmix=a&device_platform=android&aid=1128&ts='+str(time.time())
        sig = self.get_xgorgon(url, '', '', '')
        header = {
            'User-Agent': 'com.ss.android.ugc.aweme/130801 (Linux; U; Android 9; zh_CN; MI 6X; Build/PKQ1.180904.001; Cronet/TTNetVersion:58eeeb7f 2020-11-03 QuicVersion:47946d2a 2020-10-14)',
            'X-SS-REQ-TICKET': str(time.time() * 1000).split(".")[0],
            'X-SS-DP': '1128',
            'sdk-version': '2',
            'X-Gorgon': sig['xgorgon'],
            'X-Khronos': sig['xkhronos'],
            'passport-sdk-version': '18',
            'X-Tt-Token': token
        }
        resp = requests.get(url, headers=header).text
        print('直播带货榜列表：' + resp)
        return resp



    def get_live_barrage(self, room_id, cursor='', internal_ext='', iid='', device_id=''):
        """
        获取直播弹幕
        :param room_id:直播间ID
        :return:
        """
        url = 'https://live.52jan.com/dyapi/live_barrage/v2'
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
            "device_id": device_id,
            "iid": iid
        }

        resp = requests.post(url, data=data, headers=header).text
        print('直播弹幕：' + resp)
        return resp


    def re_channel(self):
        channel = ['wandoujia_aweme_feisuo', 'wandoujia_aweme2', 'tengxun_new', 'douyinw', 'douyin_tengxun_wzl',
                   'aweGW', 'aweme_360', 'aweme_tengxun', 'xiaomi']
        n = random.randint(0, 8)
        return channel[n]

    def get_web_videoinfo(self, vid):
        """
        web版视频信息
        :param vid:
        :return:
        """
        url = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=' + vid + '&' \
              'version_code=160100&version_name=16.1.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&' \
              'browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F75.0.3770.142+Safari%2F537.36&browser_online=true'

        sign = self.get_web_sign(url, 'https://www.douyin.com/video/' + vid + '?previous_page=video_detail', self.__web_ua)
        url = url + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'referer': 'https://www.douyin.com/video/' + vid + '?previous_page=video_detail'
        }
        resp = requests.get(url, headers=header, cookies=self.get_cookie()).text
        print('web版视频信息：', resp)
        return resp


    def get_web_comment(self, vid, page):
        """
        web版获取评论
        :param vid:
        :param page:
        :return:
        """
        url = 'https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=' + vid + '&' \
              'cursor=' + str(page) + '&count=20&version_code=160100&version_name=16.1.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&' \
              'browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F' \
              '75.0.3770.142+Safari%2F537.36&browser_online=true'
        sign = self.get_web_sign(url, 'https://www.douyin.com/video/' + vid + '?previous_page=main_page', self.__web_ua)
        url = url + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'Cookie': 'passport_auth_status_ss=d345a1fe9498e99aaae8772c4411a6ac%2C; sid_guard=5029a6aab0d1c73a76bd8904562c3d6f%7C1640241717%7C5184000%7CMon%2C+21-Feb-2022+06%3A41%3A57+GMT; uid_tt=e5b46693845811ea6961be4bbb581ef5; uid_tt_ss=e5b46693845811ea6961be4bbb581ef5; sid_tt=5029a6aab0d1c73a76bd8904562c3d6f;'
                      ' sessionid=5029a6aab0d1c73a76bd8904562c3d6f; sessionid_ss=5029a6aab0d1c73a76bd8904562c3d6f; sid_ucp_v1=1.0.0-KDBhMmI5MTI3YTc2MzZlMmE2ZDI1MDgwNjQzMDQzNzJmM2YwOTU2MTQKFwj4ueCXiPTvAhC1tJCOBhjvMTgGQPQHGgJscSIgNTAyOWE2YWFiMGQxYzczYTc2YmQ4OTA0NTYyYzNkNmY; ssid_ucp_v1=1.0.0-KDBhMmI5MTI3YTc2MzZlMmE2ZDI1'
                      'MDgwNjQzMDQzNzJmM2YwOTU2MTQKFwj4ueCXiPTvAhC1tJCOBhjvMTgGQPQHGgJscSIgNTAyOWE2YWFiMGQxYzczYTc2YmQ4OTA0NTYyYzNkNmY; passport_auth_status=d345a1fe9498e99aaae8772c4411a6ac%2C; MONITOR_WEB_ID=a3043f91-cedf-4682-80b2-922f661e7d27; sso_uid_tt=688f7b503a73fa2ccda15a39cf344910; sso_uid_tt_ss=688f7b503a73fa2c'
                      'cda15a39cf344910; toutiao_sso_user=a652c7ab28cfd5529c9cfcfed5b8435f; toutiao_sso_user_ss=a652c7ab28cfd5529c9cfcfed5b8435f; sid_ucp_sso_v1=1.0.0-KDdhNmE3MWRjY2ViZTRiMWNlMTJjN2QyYzI1M2M1NWRmYTY5YTU0ODUKFwj4ueCXiPTvAhC1tJCOBhjvMTgGQPQHGgJsZiIgYTY1MmM3YWIyOGNmZDU1MjljOWNmY2ZlZDViODQzNWY; ssid_ucp_sso_v1=1'
                      '.0.0-KDdhNmE3MWRjY2ViZTRiMWNlMTJjN2QyYzI1M2M1NWRmYTY5YTU0ODUKFwj4ueCXiPTvAhC1tJCOBhjvMTgGQPQHGgJsZiIgYTY1MmM3YWIyOGNmZDU1MjljOWNmY2ZlZDViODQzNWY; n_mh=lIE_aX9LSJUND6iLw_hHl7uvVSs4g-GUPXO6aWyQCL0; msToken=iC10vixO8xiqyytWVnHo3a7JKKyldHHVl25AcRHyVknIW9wQt_1R3_8y6lKMwkaR-6IkXF9AZaPf3QwEdpUGRWQPfJynl57SXZ9ilY'
                      'vjTM91_dKw2cp76A==; passport_csrf_token_default=41023a9541b61ae05c84ca351a7fbf5c; passport_csrf_token=41023a9541b61ae05c84ca351a7fbf5c; ' + cookie
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

        url = 'https://www.douyin.com/aweme/v1/web/user/follower/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAgrpcoLYJIncK6LCPT4A1bDEW2oM12j-PWDvPIWHL7ls&offset=0&min_time=0&max_time=' + page + '&count=20&source_type=' \
              '1&gps_access=0&address_book_access=0&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=3840&screen_height=2560&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=86.0.4240.198&browser_online=true&engine_name=Bl' \
              'ink&engine_version=86.0.4240.198&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50'
        sign = self.get_web_sign(url, 'https://www.douyin.com/user/' + sec_uid + '?previous_page=app_code_link', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
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
                      'vjTM91_dKw2cp76A==; passport_csrf_token_default=41023a9541b61ae05c84ca351a7fbf5c; passport_csrf_token=41023a9541b61ae05c84ca351a7fbf5c; ' + cookie['data'][0]['web_cookie']
        }
        resp = requests.get(url, headers=header).content
        print('web粉丝列表：', resp)
        return resp

    def web_user_search(self, keyword, page=None):
        """
        web版搜索用户
        :param keyword:搜索关键词
        :param page:
        :return:
        """
        import uuid
        url = 'https://www.douyin.com/aweme/v1/web/discover/search/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_user_web&' \
              'keyword=' + keyword + '&search_source=normal_search&query_correct_type=1&is_filter_search=0&offset=' + str(page) + '&count=20&version_code=160100&ve' \
              'rsion_name=16.1.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(W' \
              'indows+NT+10.0%3B+WOW64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F86.0.4240.198+Safari%2F537.36&browser_online=true'
        ref = 'https://www.douyin.com/search/' + keyword + '?aid=' + str(uuid.uuid4()) + '&source=normal_search&type=user'
        sign = self.get_web_sign(url, ref, self.__web_ua)
        url = url + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'referer': ref,
            'Cookie': cookie['data'][0]['web_cookie']
        }
        resp = requests.get(url, headers=header).text
        print('web用户搜索列表：', resp)
        return resp


    def web_video_search(self, keyword, page=None):
        """
        web版获取搜索视频
        :param keyword:搜索关键词
        :param page:
        :return:
        """
        url = 'https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=0&publish_time=0&' \
              'keyword=' + keyword + '&search_source=normal_search&query_correct_type=1&is_filter_search=0&offset=' + str(page) + '&count=30&version_code=160100&version_name=16.1.0&cookie_enable' \
              'd=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+WOW64)+AppleWe' \
              'bKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F86.0.4240.198+Safari%2F537.36&browser_online=true'
        ref = 'https://www.douyin.com/search/' + keyword + '?source=normal_search'
        sign = self.get_web_sign(url, ref, self.__web_ua)
        url = url + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'referer': ref,
            'Cookie': cookie['data'][0]['web_cookie']
        }

        resp = requests.get(url, headers=header).text
        print('web视频搜索列表：', resp)
        return resp


    def get_web_video(self, sec_uid, page):
        """
        web版获取主页作品
        :param sec_uid:
        :param page:
        :return:
        """
        url = 'https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=' + sec_uid + '&max_cur' \
              'sor=' + str(page) + '&count=20&publish_video_strategy_type=2&version_code=160100&version_name=16.1.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_langu' \
              'age=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+WOW64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F86.0.4240.198+Safari%2' \
              'F537.36&browser_online=true'

        sign = self.get_web_sign(url, 'https://www.douyin.com/user/' + sec_uid, self.__web_ua)
        url = url + '&_signature=' + sign['sign']
        header = {
            'User-Agent': self.__web_ua,
            'referer': 'https://www.douyin.com/user/' + sec_uid
        }
        resp = requests.get(url, headers=header, cookies=self.get_cookie()).text
        print('web作品列表：', resp)
        return resp

    def get_live_user(self, uid):
        """
        获取直播用户信息
        :param uid:
        :return:
        """
        url = dyapi.host + '/dyapi/sec_uid'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts
        }
        sign = self.set_sign()
        resp = requests.post(url, data={'sign': sign, 'uid': uid}, headers=header).text
        print('直播用户信息:', resp)
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
        url = dyapi.host + '/dyapi/get_cookie'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        resp = requests.post(url, data={'sign': sign}, headers=header).json()
        print('web_cookie:', resp)
        return resp['data'][0]['web_cookie']


    def get_ranklist(self, room_id, token=''):
        """
        获取直播观众列表
        :param room_id: 直播间id 每次开播都不同
        :return:
        """
        url = dyapi.host + '/dyapi/get_ranklist'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts
        }
        sign = self.set_sign()
        resp = requests.post(url, data={'sign': sign, 'room_id': room_id, 'token': token}, headers=header).text
        print('直播观众列表', resp)
        return resp


    def set_sign(self):
        """
        计算签名
        :return:
        """
        ts = str(time.time()).split('.')[0]
        string = '1005' + self.cid + ts + self.__appkey
        sign = hashlib.md5(string.encode('utf8')).hexdigest()
        print('sign', sign)
        return sign

    def get_dy_userinfo(self, uid, token='', cookie=''):
        """
        通过_uid获取用户信息
        :param uid:
        :return:
        """

        url = dyapi.host + '/dyapi/get_userinfo'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts
        }
        sign = self.set_sign()
        resp = requests.post(url, data={'sign': sign, 'uid': uid, 'iid': device['data'][0]['install_id'], 'device_id': device['data'][0]['device_id'], 'token': token}, headers=header).text
        print('dy_userinfo:', resp)
        return resp




if __name__ == '__main__':



    api = dyapi('d9ba8ae07d955b83c3b04280f3dc5a4a')
    api.get_appkey()

    ApiInfo = api.get_ApiInfo()
    print('到期时间:' + ApiInfo)


    # app取服务器提前生成好的设备号
    device = api.get_device()



    # web版获取cookie
    cookie = api.get_web_cookie()
    print('ret_cookie:', cookie)

    vid = '7050046203945356579'
    page = 0

    token = '00470bbfeb49d95c2ca1e26ac4a1dd510f0384dbdf2f3665dd4bd0714bd8a76157a7058d65daa90d26694f0d385459aa4ab5929223fadc1d5d4c6eaec97cb70c4ede68a69a8853fa2a41b7018eedde0ec5ddd920f0d3e174de2cdccc94b4cfd0e140b-1.0.1'

    # 获取粉丝列表示例
    # api.api_get_follow('100698990140', '0', '')
    # api.get_follow('100698990140', page, 20, token, True)

    # 获取关注列表示例
    # api.api_get_follow('100698990140', '0', '1')
    # api.get_follow('100698990140', page, 20, token, False)

    # 获取用户信息
    # api.get_userinfo('100698990140')

    # 获取直播弹幕get_live_barrage
    api.get_live_barrage('7104989010182867716', iid=device['data'][0]['install_id'], device_id=device['data'][0]['device_id'])

    # 获取直播间观众
    # api.get_ranklist('7070656837364173598')

    # web获取视频信息
    # api.get_web_videoinfo(vid)

    # 获取橱窗列表
    # api.get_shop_product('94409926892', page, token)

    # 获取直播商品列表
    # api.get_shop_ranklist('MS4wLjABAAAAlZNPHQhQMZ-06qmnETc-ifP3b72dCoZSBRoGVHdPQdw', '7035099207857965855', token)
    # api.get_shop_promotions('64613798668', '7035099207857965855', token)

    # 获取带货口碑
    # api.get_shop_header('96851221040', token)

    sec_uid = 'MS4wLjABAAAA9dd_xgKqu5ADzkYWr1GINkW5E8NRNCgaywN2RMCZbq3Jqu-rsvkJ6hHZ4WBxbgxJ'
    # 获取web评论示例
    # api.get_web_comment(vid, 10)

    # 获取web粉丝列表
    # api.get_web_follower(sec_uid, str(time.time()))

    # 获取web作品列表示例
    # api.get_web_video('MS4wLjABAAAA8U_l6rBzmy7bcy6xOJel4v0RzoR_wfAubGPeJimN__4', page)

    import urllib
    keyword = urllib.parse.quote('哈士奇')

    # app用户搜索
    # api.get_user_search('哈士奇', page, token)
    # web用户搜索
    # api.web_user_search(keyword, page)

    # app视频搜索
    # api.get_video_search('哈士奇', page, token)
    # web视频搜索
    # api.web_video_search(keyword, page)



    # 获取评论示例
    api.api_get_comment(vid, 0)
    # api.get_video_comment(vid, 0)

    # 获取视频点赞列表
    # api.get_favorite('7031869128239533343', 0, 0, token)

    # 获取作品列表示例
    # api.get_video('94409926892', page, '')

    # 获取直播用户信息
    # api.get_live_user('64613798668')

    # 通过uid获取用户信息
    api.get_dy_userinfo('94409926892', token)



