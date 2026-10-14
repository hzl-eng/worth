# 整合数据底座v2：全量采集、不做预设分类，筛选留给以后网站
import csv
import os
from collections import Counter

FIELDS = ["source", "title", "org", "category", "location",
          "salary", "degree", "date", "description", "url"]

def read_csv(path):
    if not os.path.exists(path):
        print("  跳过（文件不存在）:", path)
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def salary_of(low, high):
    if low and high:
        return f"{low}-{high}"
    return "面议"

rows = []

# 1) NCSS：全量(81) + 关键词补充(前端/后端)，统一归为 NCSS 来源，类别留空（不预设筛选）
for src_file in ["jobs_all.csv", "jobs_more.csv", "jobs_backend.csv"]:
    for r in read_csv(src_file):
        rows.append({
            "source": "NCSS", "title": r.get("jobName") or r.get("title", ""),
            "org": r.get("company", ""), "category": "",          # 筛选后置，不硬分类
            "location": r.get("area", ""), "salary": salary_of(r.get("salary_low"), r.get("salary_high")),
            "degree": r.get("degree", ""), "date": "", "description": r.get("description", ""),
            "url": r.get("detailUrl", ""),
        })

# 2) 政府/事业单位招聘公告（有才读）
for r in read_csv("gov_jobs_full.csv"):
    rows.append({
        "source": "人社局官网", "title": r.get("title", ""), "org": "人社局/事业单位",
        "category": "", "location": "福州", "salary": "", "degree": "",
        "date": r.get("date", ""), "description": r.get("body", ""), "url": r.get("url", ""),
    })

# 3) 大厂招聘（腾讯），类别保留它的原始值（如"产品""技术"）
for r in read_csv("tencent_jobs.csv"):
    rows.append({
        "source": "腾讯招聘", "title": r.get("title", ""), "org": r.get("dept", ""),
        "category": r.get("category", ""), "location": r.get("location", ""),
        "salary": "", "degree": "", "date": "",
        "description": r.get("responsibility", ""), "url": r.get("postId", ""),
    })

# 合并去重（标题+链接）
seen = set()
uniq = []
for r in rows:
    key = (r["title"], r["url"])
    if key in seen:
        continue
    seen.add(key)
    uniq.append(r)

with open("jobs_all_in_one.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(uniq)

count = Counter(r["source"] for r in uniq)
print("各来源条数：")
for src, n in count.items():
    print(f"  {src}: {n} 条")
print(f"去重后总计: {len(uniq)} 条")
print("已生成 jobs_all_in_one.csv")
