# 第2课第一步：翻页抓取所有"前端"岗位
import requests
import json

url = "https://www.ncss.cn/student/jobs/jobslist/ajax/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Referer": "https://www.ncss.cn/student/jobs/index.html",
}

all_jobs = []            # 空列表，用来收集所有页的岗位

# range(1, 4) 意思是 page 依次取 1、2、3 —— 翻3页
for page in range(1, 4):
    params = {
        "jobName": "前端",
        "offset": page,     # offset 就是页码
        "limit": 20,        # 每页最多20条
        "callback": "cb",
    }
    resp = requests.get(url, params=params, headers=headers)

    text = resp.text.strip()
    if text.startswith("cb("):      # 老规矩：是 cb(...) 才剥壳
        text = text[3:-1]
    data = json.loads(text)

    jobs = data["data"]["list"]     # 这一页的岗位列表
    if not jobs:                    # 这一页是空的 = 到底了，停
        print("没有更多岗位了，停止翻页")
        break

    all_jobs.extend(jobs)           # 把这一页合并进大列表
    print(f"第{page}页拿到 {len(jobs)} 条，累计 {len(all_jobs)} 条")

print("\n翻页完成，一共抓到", len(all_jobs), "个前端岗位")
