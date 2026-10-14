# 诊断版：看看 NCSS 接口到底返回了什么
import requests

url = "https://www.ncss.cn/student/jobs/jobslist/ajax/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Referer": "https://www.ncss.cn/student/jobs/index.html",
}
params = {
    "jobName": "前端",
    "offset": 1,
    "limit": 5,
    "callback": "cb",
}

resp = requests.get(url, params=params, headers=headers)

print("HTTP状态码:", resp.status_code)          # 200=成功 404=没找到 403=被拒
print("返回内容的前500个字符：")
print(resp.text[:500])
