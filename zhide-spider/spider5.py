# 完整版爬虫：翻页抓列表 + 抓详情 + 清洗 + 存文件
import requests
import json
import csv
import time
from bs4 import BeautifulSoup

url = "https://www.ncss.cn/student/jobs/jobslist/ajax/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Referer": "https://www.ncss.cn/student/jobs/index.html",
}

# ---------- 1. 翻页抓列表（1~3页） ----------
all_jobs = []
for page in range(1, 4):
    params = {"jobName": "前端", "offset": page, "limit": 20, "callback": "cb"}
    resp = requests.get(url, params=params, headers=headers)
    text = resp.text.strip()
    if text.startswith("cb("):
        text = text[3:-1]
    jobs = json.loads(text)["data"]["list"]
    if not jobs:
        break
    all_jobs.extend(jobs)
print("列表抓完，共", len(all_jobs), "个岗位")

# ---------- 2. 定义一个"抓详情"的函数 ----------
def fetch_detail(job_id):
    detail_url = f"https://www.ncss.cn/student/jobs/{job_id}/detail.html"
    resp = requests.get(detail_url, headers=headers)
    resp.encoding = resp.apparent_encoding or "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n")
    idx = text.find("职位详情")
    if idx != -1:
        text = text[idx:]
    return text[:2000]        # 只留前2000字，防止太长

# ---------- 3. 清洗成结构化记录 ----------
clean_jobs = []
seen = set()                 # 用来去重
for j in all_jobs[:10]:      # 演示：先处理前10个（全量可改）
    job_id = j["jobId"]
    if job_id in seen:       # 重复的跳过
        continue
    seen.add(job_id)
    desc = fetch_detail(job_id)
    time.sleep(0.5)          # 每次抓完歇0.5秒，礼貌限速
    record = {
        "jobName": j.get("jobName", ""),
        "company": j.get("recName", ""),
        "salary_low": j.get("lowMonthPay"),
        "salary_high": j.get("highMonthPay"),
        "degree": j.get("degreeName", ""),
        "area": j.get("areaCodeName", ""),
        "headCount": j.get("headCount"),
        "description": desc,
        "detailUrl": f"https://www.ncss.cn/student/jobs/{job_id}/detail.html",
    }
    clean_jobs.append(record)
    print(f"已处理 {len(clean_jobs)} 条：{record['jobName']} | {record['company']}")

# ---------- 4. 存成 JSON 和 CSV ----------
with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(clean_jobs, f, ensure_ascii=False, indent=2)

with open("jobs.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(clean_jobs[0].keys()))
    w.writeheader()
    w.writerows(clean_jobs)

print("\n完成！生成了 jobs.json 和 jobs.csv（左侧文件树能看到）")
