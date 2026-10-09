#重跑RED:25的DOI转换
import requests
import csv
import time

API_KEY = ""  # 请替换为自己的 OpenAlex API Key

def doi_to_openalex_w(doi, max_retries=3):
    url = f"https://api.openalex.org/works/https://doi.org/{doi}"
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params={"api-key": API_KEY}, timeout=30)
            print(f"  请求URL: {url}")
            print(f"  HTTP状态: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                return data.get("id", "").split("/")[-1]
        except Exception as e:
            print(f"  第{attempt+1}次尝试异常: {e}")
            time.sleep(3)  # 等3秒重试
    return None

# 补 RED:25 的 citing DOI
citing_doi = "10.1038/s41467-017-00519-2"
print(f"查询 RED:25 citing DOI: {citing_doi}")
citing_w = doi_to_openalex_w(citing_doi)
print(f"  结果: {citing_w}\n")

# 更新 red_doi_to_w_mapping.csv
rows = []
with open('red_doi_to_w_mapping.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        if row['citation_id'] == 'RED:25':
            row['citing_w'] = citing_w
        rows.append(row)

with open('red_doi_to_w_mapping.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("red_doi_to_w_mapping.csv 已更新")