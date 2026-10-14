# 浏览器自动化：让真实浏览器渲染美团职位列表，再抓数据
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)      # 无头浏览器（不弹窗）
    page = browser.new_page()
    page.goto("https://zhaopin.meituan.com/web/position/", timeout=60000)
    page.wait_for_load_state("networkidle")          # 等网络空闲（JS基本加载完）
    page.wait_for_timeout(3000)                      # 再额外等3秒
    html = page.content()                            # 拿渲染后的完整HTML
    browser.close()

# 渲染完的HTML里就有岗位了，用 BeautifulSoup 解析
soup = BeautifulSoup(html, "html.parser")
text = soup.get_text(" ", strip=True)
print("渲染后页面文字前1000字：")
print(text[:1000])
