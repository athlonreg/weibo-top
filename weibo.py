import datetime
import urllib.parse

import requests
import json

# spider variables
weibo_url = 'https://weibo.com/ajax/side/hotSearch'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
}


# 爬取数据
def spider():
    response = requests.get(weibo_url, headers=headers)
    response.encoding = 'utf-8'

    origin_result = response.text
    origin_result_dict = json.loads(json.dumps(json.loads(origin_result), ensure_ascii=False))
    top_list = list(origin_result_dict.get("data").get("realtime"))

    text_result = "| 热搜榜 | 热搜分类 | 热搜标题 | 上榜时间 |"
    text_result += "\n| --- | --- | --- | --- |"
    for index in range(0, len(top_list)):
        item = top_list[index]
        timestamp = item.get("onboard_time")
        word = item.get("word")
        realpos = str(item.get("realpos"))
        category = item.get("category")
        link = urllib.parse.quote("https://s.weibo.com/weibo?q=%23" + word + "%23", safe='://')
        word = '[' + item.get("word") + '](' + link + ')'
        if timestamp is None:
            continue
        text_result += "\n| " + realpos + " | " + category + " | " + word + " | " + str(
            datetime.datetime.fromtimestamp(timestamp)) + " | "
    return text_result


# 生成发布内容
def generate(now, content):
    now_date = str(now.date())
    head = f"""---
title:  每日热搜 - {now_date}
categories: 每日热搜
summary: 每日热搜 - {now_date}
tags:
  - 每日热搜
  - 微博
  - 热搜
index_img: https://cdn.jsdelivr.net/gh/athlonreg/weibo-top/weibo-top.jpeg
excerpt: 每日热搜 - {now.strftime("%Y-%m-%d %H:%M:%S")}
---

"""
    result = head + content
    return result


current_now = datetime.datetime.now()
file = "./source/_posts/" + str(current_now.date()) + ".md"
file_stream = open(file, mode='w', encoding='utf-8')
file_stream.truncate()
print(generate(now=current_now, content=spider()), file=file_stream)
file_stream.close()
print()
