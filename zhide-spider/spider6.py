# 进阶爬虫：多个关键词 + 翻多页 + 去重，抓更多岗位
import requests
import json
import csv
import time

url = "https://www.ncss.cn/student/jobs/jobslist/ajax/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Referer": "https://www.ncss.cn/student/jobs/index.html",
}

# 多个关键词：每个都去搜一遍
keywords = ["后端","前端", "前端开发", "Web前端", "Vue", "React", "小程序", "H5", "TypeScript"]

all_jobs = []      # 收集所有岗位
seen = set()       # 记下见过的 jobId，用来去重

# 外层循环：一个词一个词搜
for kw in keywords:
    # 内层循环：每个词翻5页
    for page in range(1, 6):
        params = {"jobName": kw, "offset": page, "limit": 20, "callback": "cb"}
        resp = requests.get(url, params=params, headers=headers)
        text = resp.text.strip()
        if text.startswith("cb("):
            text = text[3:-1]
        data = json.loads(text)
        jobs = data["data"]["list"] if data.get("data") else []

        if not jobs:           # 这一页空 = 这个词到底了，跳出内层循环
            break

        for j in jobs:         # 逐条处理
            jid = j["jobId"]
            if jid in seen:    # 已经见过了，跳过（去重）
                continue
            seen.add(jid)
            all_jobs.append({
                "jobName": j.get("jobName", ""),
                "company": j.get("recName", ""),
                "salary_low": j.get("lowMonthPay"),
                "salary_high": j.get("highMonthPay"),
                "degree": j.get("degreeName", ""),
                "area": j.get("areaCodeName", ""),
                "headCount": j.get("headCount"),
                "detailUrl": f"https://www.ncss.cn/student/jobs/{jid}/detail.html",
            })
        print(f"[{kw}] 第{page}页，当前累计 {len(all_jobs)} 个")
        time.sleep(0.4)        # 限速

# 存文件
with open("jobs_backend.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=2)
with open("jobs_backend.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(all_jobs[0].keys()))
    w.writeheader()
    w.writerows(all_jobs)

print("\n采集完成！共", len(all_jobs), "个岗位（已去重），生成 jobs_more.json / jobs_more.csv")
