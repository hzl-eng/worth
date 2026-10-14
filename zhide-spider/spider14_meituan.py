# 美团招聘全量：解析岗位卡片(data-jobunionid)，点分页图标翻到底，去重存csv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv

def parse_page(html):
    """解析一页的所有岗位卡片"""
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    for card in soup.find_all("div", class_="position_list_item"):
        jid = card.get("data-jobunionid", "")
        title = tag = job_type = city = date = ""
        t = card.select_one("div.postion_name div.title")
        if t: title = t.get_text(strip=True)
        t = card.select_one(".tag_hot")
        if t: tag = t.get_text(strip=True)
        for it in card.select(".split_line_box_item"):
            txt = it.get_text(strip=True)
            if "更新于" in txt: date = txt
            elif it.select_one(".city") or it.select_one(".zp_clamp_string"): city = txt
            elif txt and not txt.startswith("更新于"): job_type = txt
        desc = ""
        d = [x.get_text(strip=True) for x in card.select(".position_duty .desc")]
        if d: desc = " ".join(x for x in d if x)
        jobs.append({"jobId": jid, "title": title, "tag": tag, "type": job_type,
                     "city": city, "date": date, "desc": desc[:500],
                     "detailUrl": f"https://zhaopin.meituan.com/web/position/detail?jobUnionId={jid}"})
    return jobs

def save(jobs):
    with open("meituan_jobs.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["jobId","title","tag","type","city","date","desc","detailUrl"])
        w.writeheader(); w.writerows(jobs)

all_jobs, seen = [], set()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://zhaopin.meituan.com/web/position/", timeout=60000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    page_num = 1
    while True:
        for j in parse_page(page.content()):
            if j["jobId"] and j["jobId"] not in seen:
                seen.add(j["jobId"]); all_jobs.append(j)
        if page_num % 10 == 0:
            print(f"第{page_num}页：累计{len(all_jobs)}条")
        if page_num % 50 == 0:
            save(all_jobs)            # 每50页存一次，中途崩溃也不丢太多

        nx = page.locator("li.mtd-pagination-next")   # 美团分页是图标按钮，用class定位
        if nx.count() == 0:
            break
        cls = nx.get_attribute("class") or ""
        if "mtd-pagination-item-disabled" in cls:     # 末页时这个class会出现
            print("已到最后一页，结束"); break
        nx.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2500)
        page_num += 1
        if page_num > 310:
            break
    browser.close()

save(all_jobs)
print(f"完成！共 {len(all_jobs)} 条，生成 meituan_jobs.csv")
