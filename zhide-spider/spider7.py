# 探测：不带关键词，能不能直接翻页拿"全部"岗位
import requests
import json

url = "https://www.ncss.cn/student/jobs/jobslist/ajax/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Referer": "https://www.ncss.cn/student/jobs/index.html",
}

# 注意：这次不传 jobName，只翻第1页
params = {"offset": 1, "limit": 20, "callback": "cb"}
resp = requests.get(url, params=params, headers=headers)
text = resp.text.strip()
if text.startswith("cb("):
    text = text[3:-1]
data = json.loads(text)

flag = data.get("flag")
print("flag:", flag)
data2 = data.get("data") or {}
lst = data2.get("list", [])
print("不带关键词，第1页返回条数:", len(lst))
if lst:
    print("第1条岗位名:", lst[0].get("jobName"))
print("data 里有哪些字段:", list(data2.keys()))   # 看有没有 total 总数
