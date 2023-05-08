# dyapitest
- 抖音系api整理测试，仅供测试学习使用
- 如有侵权请[联系我](https://www.app966.cn)删除
```
https://www.douyin.com/robots.txt
```

## 2023.03.28
**测试web获取用户作品信息**
- 此接口今天升级了，安全性提高了
- 简单分析了下说下我的结论和解决方式
  - 旧版路径`/aweme/v1/web/aweme/post/`，只允许登录过的用户访问
  - 新版路径`/aweme/v1/web/locate/post/`，只允许知晓对方任意一个作品id的情况下访问，关键参数为：`locate_item_id`（对方任意一个作品id）
  - 直接读取网页`./user/MS4wLjABAAAAlZNPHQhQMZ-06qmnETc-ifP3b72dCoZSBRoGVHdPQdw`，只允许读取一页
- 有了以上结论就大概知道如何解决了
- 我的场景是抖音摸鱼小插件，主要是随机取一位自己添加在随机池内的播主的近期随机一个作品并播放
- 所以我直接使用`scrapy`读网页即可[拿到的数据](https://github.com/Superheroff/dyapitest/blob/main/web_video_demo.json)
## 2023.03.29
- 这个数据太乱太长了建议不要取整段，用正则精简下`<script id="RENDER_DATA" type="application/json">(.*?)%22post%22%3A%7B%22(.*?)%2C%22_location`
- 这样之后返回的内容要拼接一下，拼接头：`{"post":{"`
- [相关源码](https://github.com/Superheroff/dyapitest/blob/main/video_post.py)
- 推荐一个好用的json解析网站，可以快速定位json错误位置[Jsonlint](https://jsonlint.com/)

## 2023.04.05
**测试视频信息列表**
- 使用flask包装接口并调用测试
- [相关源码](https://github.com/Superheroff/dyapitest/blob/main/video_info.py)

**接口说明**
- GET：重定向至随机一个视频的源地址
- POST：返回视频所有信息

参数名|参数类型|参数描述|参数示例
---|---|---|---
video_list|int: list|视频ID列表|[7206592982118616324,7180333041812819237,7212918206074309899]


**请求示例**
```
http://api2.52jan.com/video_info?video_list=[7206592982118616324,7180333041812819237,7212918206074309899]
```
**失败示例**
```
{"msg": "此接口已失效"}
```

## 2023.04.15
**抖音网页版没有`WebDriver`检测**
- 没有检测可能导致的后果：使用`playwright`或`selenium`用户登录、爬取数据、发布视频、点赞、发表评论等操作。

## 2023.04.23
**分析无水印解析**
- 此处分为2步
  1. 把视频的key取出来，字段为`uri`
  2. 拼接地址，此处又分高清和普通版本
- 如何找到清晰度最高的地址呢
  1. 通过`dataSize`这个字段，数值越大视频越清晰
      - 最清晰的一般是在`video.play_addr_lowbr`或`video.play_addr_h264`里面
      - 文件最小的是在`video.play_addr_265`
      - 带水印的在`video.download_addr`，总之包含`download`的路径都是带水印的
  2. 保存数值最大的字段下的`file_id`的值，然后拼接url
- 拼接示例
    1. 高清地址（81.4 MB）：`https://api-play-hl.amemv.com/aweme/v1/play/?video_id=v0200fg10000cgdcksjc77ucureni2j0&file_id=157e3967e85a461db2383bbee2d13889`
    2. 普通地址（25.7 MB）：`https://www.douyin.com/aweme/v1/play/?video_id=v0200fg10000cgdcksjc77ucureni2j0&file_id=426954cc72d7448dbaaddfa4663d495c`

## 2023.05.08
**测试web用户粉丝接口**
- 使用`playwright`执行一段js代码即可，如下所示
- 你所需要掌握的知识
  - 如何使用`playwright`执行js代码
  - 如何让`playwright`带cookie访问网页
```
function queryData(url) {
     var p = new Promise(function(resolve,reject) {
         var e={
                 "url":"https://www.douyin.com/aweme/v1/web/user/follower/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&user_id=&sec_user_id=%s&offset=0&min_time=0&max_time=0&count=20&source_type=3&gps_access=0&address_book_access=0&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=112.0.0.0&browser_online=true&engine_name=Blink&engine_version=112.0.0.0&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100",
                 "method":"GET"
               };
          var h = new XMLHttpRequest;
          h.open(e.method, e.url, true);
          h.setRequestHeader("accept","application/json, text/plain, */*");
          h.onreadystatechange =function() {
               if(h.readyState === 4 && h.status === 200) {
                    resolve(h.responseText);
               } else {}
          };
          h.send(null);
          });
          return p;
      }
  var p1 = queryData();
  res = Promise.all([p1]).then(function(result){
          return result
  })
  return res
```
