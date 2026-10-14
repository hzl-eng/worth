# 探测美团列表：滚动能否加载新岗位？是否有分页？岗位链接长啥样？
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://zhaopin.meituan.com/web/position/", timeout=60000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    def stat():
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        total = re.search(r"全部职位（(\d+)）", text)
        return (total.group(1) if total else "?"), text.count("更新于")

    total, u = stat()
    print(f"初始：全站{total}条，当前可见'更新于'数={u}")

    # 滚动5次，看岗位数是否增长
    for i in range(1, 6):
        page.mouse.wheel(0, 4000)
        page.wait_for_timeout(2000)
        total, u = stat()
        print(f"第{i}次滚动：可见'更新于'数={u}")

    # 看有没有分页/加载更多
    html = page.content()
    print("有'下一页':", "下一页" in html, "| 有'加载更多':", "加载更多" in html)

    # 看岗位卡片的链接结构
    soup = BeautifulSoup(html, "html.parser")
    n = 0
    for a in soup.find_all("a", href=True):
        href = a["href"]
        txt = a.get_text(strip=True)
        if href and len(txt) > 4 and "position" in href:
            print("岗位链接:", href[:80], "|", txt[:25])
            n += 1
            if n >= 8:
                break
    browser.close()
