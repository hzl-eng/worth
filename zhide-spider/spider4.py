# 第2课第二步：抓单个岗位的详情（职位描述）
import requests
import json
from bs4 import BeautifulSoup      # 网页解析库

url = "https://www.ncss.cn/student/jobs/jobslist/ajax/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Referer": "https://www.ncss.cn/student/jobs/index.html",
}

# ---------- 第1步：先拿一个岗位的 jobId ----------
params = {"jobName": "前端", "offset": 1, "limit": 1, "callback": "cb"}
resp = requests.get(url, params=params, headers=headers)
text = resp.text.strip()
if text.startswith("cb("):
    text = text[3:-1]
job = json.loads(text)["data"]["list"][0]   # 取第1条岗位
job_id = job["jobId"]
print("岗位:", job["jobName"], "| jobId:", job_id)

# ---------- 第2步：请求这个岗位的详情页 ----------
detail_url = f"https://www.ncss.cn/student/jobs/{job_id}/detail.html"
resp2 = requests.get(detail_url, headers=headers)
resp2.encoding = resp2.apparent_encoding or "utf-8"   # 纠正中文编码，防止乱码

# ---------- 第3步：用 BeautifulSoup 把网页文字挖出来 ----------
soup = BeautifulSoup(resp2.text, "html.parser")        # 解析整个网页
page_text = soup.get_text(separator="\n")        # 取出网页里的所有文字

# 只保留"职位详情"之后的部分（前面都是导航栏等无关文字）
idx = page_text.find("职位详情")
if idx != -1:
    page_text = page_text[idx:]

print("\n--- 职位详情前600字 ---")
print(page_text[:600])

