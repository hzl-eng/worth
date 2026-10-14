# 腾讯招聘·全量版：自动算总页数，抓全站岗位
import requests
import csv
import time

url = "https://careers.tencent.com/tencentcareer/api/post/Query"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
    "Referer": "https://careers.tencent.com/zh-cn/search.html",
}

# 第1步：先问第一页，拿到全站总数，自动算总页数
def ask(page):
    return requests.get(url, params={
        "pageIndex": page, "pageSize": 10, "language": "zh-cn",
        "area": "", "keyword": "", "timestamp": int(time.time() * 1000),
    }, headers=headers).json()

total = ask(1)["Data"]["Count"]
pages = total // 10 + 1            # 2236//10=223，+1=224页
print(f"全站共 {total} 条，约 {pages} 页")

all_posts = []

def save():                        # 分批保存，防中断
    with open("tencent_jobs_all.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["title", "category", "dept", "location", "postId", "responsibility"])
        w.writeheader()
        w.writerows(all_posts)
    print(f"  --- 已保存一批，累计 {len(all_posts)} 条 ---")

for page in range(1, pages + 1):
    try:
        data = ask(page).get("Data")
    except Exception as e:         # 某页请求失败就跳过，不中断整程
        print(f"第{page}页请求失败，跳过:", e)
        continue
    posts = (data or {}).get("Posts") or []
    if not posts:                  # 没数据了，正常结束
        print(f"第{page}页无数据，结束")
        break
    for p in posts:
        all_posts.append({
            "title": p.get("RecruitPostName", ""),
            "category": p.get("CategoryName", ""),
            "dept": p.get("BGName", ""),
            "location": p.get("LocationName", ""),
            "postId": p.get("PostId", ""),
            "responsibility": (p.get("Responsibility") or "")[:300],
        })
    if len(all_posts) % 200 == 0:
        save()
    if page % 20 == 0:
        print(f"第{page}页，累计 {len(all_posts)} 条")
    time.sleep(0.4)                # 限速，防被封

save()
print("完成！共", len(all_posts), "条腾讯岗位，生成 tencent_jobs_all.csv")
