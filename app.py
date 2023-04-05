
import time
import requests
from flask import Flask, request, redirect

def video_info(video_list: list) -> str:
    url = "https://api3-normal-c-hl.amemv.com/aweme/v1/multi/aweme/detail/?os_api=22&device_type=MI+9&ssmix=a" \
          "&manifest_version_code=120701&dpi=240&uuid=262213994129345&app_name=aweme&version_name=12.7.0&ts" \
          "=%s&cpu_support64=false&storage_type=0&app_type=normal&appTheme=dark&ac=wifi&host_abi=armeabi-v7a&update_version_code=12709900" \
          "&channel=tengxun_new&_rticket=%s&device_platform=android&iid=0&version_code=120700&mac_address=10:2a:b3:52:8c:70&cdid=fda4c8ff-171e-4959-8154-5454fec79a87" \
          "&openudid=af452f2f28b2d1f9&device_id=0&resolution=720*1280&os_version=5.1.1&language=zh&device_brand=Android&aid=1128" \
          "&mcc_mnc=46007" % (str(time.time()).split(".")[0], str(time.time() * 1000).split(".")[0])

    data = {
        "aweme_ids": "".join(video_list),
        "origin_type": "goods_rank_list_0",
        "push_params": "",
        "request_source": "0"
    }
    ret = requests.post(url, data=data).text
    # print(ret)
    return ret

application = Flask(__name__)
@application.route("/video_info", methods=["POST", "GET"])
def video_info():
    """
    测试获取视频信息接口
    post返回视频所有信息
    get重定向至随机一个视频的源地址
    :return:
    """
    video_list = request.values.get("video_list")
    if not video_list:
        return {'msg': '参数video_list不能为空'}
    data = video_info(video_list)
    if request.method == "POST":
        return data
    else:

        json_data = json.loads(data)
        n = json_data["aweme_details"]
        if len(n) == 0:
            return {'msg': '此接口已失效'}
        try:
            v_list = random.choice(n)
            uri = v_list["video"]["play_addr"]["url_list"][0]
        except KeyError:
            uri = {'msg': '此接口已失效'}
        return redirect(uri, code=301)
      
      
      
      
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5050)
