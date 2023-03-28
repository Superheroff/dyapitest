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
- 所以我直接使用`scrapy`读网页即可
