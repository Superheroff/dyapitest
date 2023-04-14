# dyapitest
- **device_id已失效**
- 抖音相关api整理测试，仅供测试学习使用
- 如有侵权请[联系我](https://www.app966.cn)删除
```
https://www.douyin.com/robots.txt
```

## 2022.08.06
- 测试直播弹幕
## 2023.03.21
- 测试web获取作品信息

## 2023.03.28
- 测试web获取作品信息
- 此接口今天升级了，安全性提高了
- 简单分析了下说下我的结论和解决方式
1. 旧版路径`/aweme/v1/web/aweme/post/`，只允许登录过的用户访问
2. 新版路径`/aweme/v1/web/locate/post/`，只允许知晓对方任意一个作品id的情况下访问，关键参数为：`locate_item_id`（对方任意一个作品id）
3. 直接读取网页`./user/MS4wLjABAAAAlZNPHQhQMZ-06qmnETc-ifP3b72dCoZSBRoGVHdPQdw`，只允许读取一页
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
- 没有检测可能导致的后果：使用`playwright`或`selenium`用户登录、爬取数据、发布视频、点赞、发表评论等操作
