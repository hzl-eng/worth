# NCSS 全部岗位：全量100条 + 多个关键词合并去重
import requests, json, time, csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36',
    'Referer': 'https://www.ncss.cn/student/jobs/index.html',
}

def fetch(offset, kw=None, limit=20):
    url = 'https://www.ncss.cn/student/jobs/jobslist/ajax/'
    params = {'offset': offset, 'limit': limit, 'callback': 'cb'}
    if kw:
        params['jobName'] = kw
    r = requests.get(url, params=params, headers=headers, timeout=20)
    t = r.text
    if t.startswith('cb('):          # 剥掉 JSONP 外壳
        t = t[3:-1]
    try:
        return json.loads(t).get('data') or {}
    except:
        return {}

seen, rows = set(), []
def add(lst):
    for j in lst:
        jid = j.get('jobId')
        if jid and jid not in seen:
            seen.add(jid)
            rows.append({'jobName': j.get('jobName', ''), 'company': j.get('recName', ''),
                         'area': j.get('areaCodeName', ''), 'degree': j.get('degreeName', ''),
                         'description': j.get('description', ''),
                         'detailUrl': f'https://www.ncss.cn/student/jobs/{jid}/detail.html',
                         'salary_low': str(j.get('lowMonthPay') or ''),
                         'salary_high': str(j.get('highMonthPay') or '')})

# 1) 全量（不带关键词）
for off in range(1, 7):
    add(fetch(off).get('list') or []); time.sleep(0.2)
print('全量后:', len(rows))

# 2) 各关键词合并（想覆盖更全就继续加关键词）
for kw in ['前端', '后端', '产品', '算法', '测试', '运维', '数据分析', '设计', 'Java', 'Python', '新媒体', '运营']:
    for off in range(1, 7):
        lst = fetch(off, kw).get('list') or []
        if not lst:
            break
        add(lst); time.sleep(0.2)
    print(f'{kw}: 累计{len(rows)}')

with open('jobs_all_ncss.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['jobName', 'company', 'area', 'degree', 'description', 'detailUrl', 'salary_low', 'salary_high'])
    w.writeheader(); w.writerows(rows)
print('完成！NCSS全部岗位:', len(rows), '条 → jobs_all_ncss.csv')
