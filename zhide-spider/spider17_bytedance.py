# 字节跳动 校招+实习：点页码翻页，监听接口响应抓岗位，去重存csv
from playwright.sync_api import sync_playwright
import csv, datetime

FIELDS = ["source","title","org","category","location","salary","degree","date","description","url"]
all_jobs, seen = [], set()

def parse_job(j, rtname=None):
    cat = j.get("job_category") or {}
    city = j.get("city_info") or {}
    ts = j.get("publish_time") or 0
    date = datetime.datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d") if ts else ""
    code = j.get("code") or ""
    return {"source":"字节跳动","title":j.get("title",""),"org":"字节跳动",
            "category":cat.get("name","") if isinstance(cat,dict) else str(cat),
            "location":city.get("name","") if isinstance(city,dict) else str(city),
            "salary":"","degree": rtname,"date":date,
            "description":(j.get("requirement") or "")[:500],
            "url":f"https://jobs.bytedance.com/campus/position/{code}" if code else str(j.get("id"))}

def save():
    with open("bytedance_jobs.csv","w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(all_jobs)

MAX_PAGES = 100000
  # 先设30页验证(约300条)；跑通后改成 100000 全量
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page()
    def on_resp(resp):
        if "search/job/posts" in resp.url:
            try:
                d=resp.json(); data=d.get("data") or {}
                for j in data.get("job_post_list") or []:
                    jid=j.get("id")
                    if jid and jid not in seen:
                        seen.add(jid); all_jobs.append(parse_job(j))
            except: pass
    page.on("response",on_resp)
    page.goto("https://jobs.bytedance.com/campus/position",timeout=60000)
    page.wait_for_load_state("load"); page.wait_for_timeout(5000)
    page.evaluate("() => document.querySelectorAll('.hire-ai-assistant-guide-cn-mask').forEach(m => m.remove())")
    def flip(tag):
        n=0
        while n < MAX_PAGES:
            n+=1
            if n%10==0: print(f"[{tag}]第{n}页 累计{len(all_jobs)}")
            if n%100==0: save()
            nx=page.locator("li.atsx-pagination-next")
            if nx.count()==0: break
            if nx.get_attribute("aria-disabled")=="true": print(f"[{tag}]已到末页"); break
            nx.click(force=True); page.wait_for_load_state("networkidle"); page.wait_for_timeout(2500)
        print(f"[{tag}]完成 累计{len(all_jobs)}")

    print("=== 开始抓校招 ===")
    flip("校招")
    try:
        page.get_by_text("日常实习").first.click()   # 切到实习
        page.wait_for_timeout(6000)
        print("=== 开始抓实习 ===")
        flip("实习")
    except Exception as e:
        print("切换实习失败:",e)
    browser.close()

save()
print("完成！字节共",len(all_jobs),"条 → bytedance_jobs.csv")
