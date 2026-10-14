# 官网招聘公告爬虫·第1步：抓列表页（标题 + 日期 + 详情链接）
import requests
from bs4 import BeautifulSoup
import re
import csv

list_url = "https://www.fujian.gov.cn/zwgk/zdlyxxgk/jyxx/jygqxx/sydwzpxx/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
}

resp = requests.get(list_url, headers=headers)
resp.encoding = resp.apparent_encoding or "utf-8"   # 政府站常见中文编码，纠正防乱码
soup = BeautifulSoup(resp.text, "html.parser")

rows = []
for a in soup.find_all("a", href=True):            # 找出页面上所有链接
    href = a["href"]
    # 只保留"事业单位招聘"相关的公告链接（网址里都带 sydwrczp）
    if "sydwrczp" not in href and "sydwzpxx" not in href:
        continue
    title = a.get("title") or a.get_text(strip=True)   # 标题在 title 属性里
    if not title:
        continue
    # 日期在父标签 <li> 的文本开头，用正则抓出来
    parent = a.find_parent("li")
    parent_text = parent.get_text(strip=True) if parent else ""
    m = re.search(r"\d{4}-\d{2}-\d{2}", parent_text)
    date = m.group(0) if m else ""
    rows.append({"date": date, "title": title, "url": href})

# 存成 CSV
with open("gov_jobs.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["date", "title", "url"])
    w.writeheader()
    w.writerows(rows)

print("抓到", len(rows), "条公告")
for r in rows:
    print(r["date"], "|", r["title"][:30])
