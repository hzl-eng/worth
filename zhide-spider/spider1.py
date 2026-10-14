# 第一个爬虫：调国家大学生就业平台的公开接口
import requests      # 发网络请求的库
import json          # 解析 JSON 的库（Python 自带）

# 接口地址（NCSS 公开的岗位搜索接口）
url = "https://www.ncss.cn/student/jobs/jobslist/ajax/"

# 请求要带的"浏览器身份"（关键！没有它服务器不理我们）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Referer": "https://www.ncss.cn/student/jobs/index.html",
}

# 要问它的参数：搜"前端"，取第1页，要5条
params = {
    "jobName": "前端",
    "offset": 1,
    "limit": 5,
    "callback": "cb",
}

# 发请求（这次带上了身份 headers）
resp = requests.get(url, params=params, headers=headers)

# 接口返回 cb({...})，剥掉前后的 cb( 和 ) 才是纯 JSON
text = resp.text.strip()                 # 去掉首尾空格
if text.startswith("cb("):               # 只有真是 cb(...) 才剥壳
    text = text[3:-1]
data = json.loads(text)                  # 转成字典
jobs = data["data"]["list"]      # 岗位列表
print("找到了", len(jobs), "个前端岗位：")

for job in jobs:                 # 逐个打印
    print("-", job["jobName"], "|", job["recName"], "|", job["degreeName"])
