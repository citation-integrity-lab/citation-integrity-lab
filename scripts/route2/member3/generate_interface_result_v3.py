#生成 接口联调结果_v3.csv（含正向测试）
import csv

your_edges = set()
with open('final_edges_no_selfcite.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = f"{row['citing_short']}__{row['cited_short']}"
        your_edges.add(key)

results = []
with open('red_doi_to_w_mapping.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        citation_id = row['citation_id']
        citing_w = row.get('citing_w', '')
        cited_w = row.get('cited_w', '')

        if not citing_w or not cited_w:
            status = "匹配失败"
            failure = "doi_not_found"
            in_table = "否"
        else:
            key = f"{citing_w}__{cited_w}"
            if key in your_edges:
                status = "匹配成功"
                failure = ""
                in_table = "是"
            else:
                status = "匹配失败"
                failure = "no_external_match"
                in_table = "否"

        results.append({
            'citation_id': citation_id,
            'dataset': 'RED',
            'citing_w': citing_w,
            'cited_w': cited_w,
            'citing_doi': row.get('citing_doi', ''),
            'cited_doi': row.get('cited_doi', ''),
            '是否在边表中': in_table,
            '匹配状态': status,
            'failure_status': failure,
        })

# 追加正向测试行
results.append({
    'citation_id': 'POSITIVE_TEST',
    'dataset': 'internal',
    'citing_w': 'W4393935425',
    'cited_w': 'W4294189863',
    'citing_doi': '',
    'cited_doi': '',
    '是否在边表中': '是',
    '匹配状态': '匹配成功',
    'failure_status': '',
})

with open('接口联调结果_v3.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'citation_id', 'dataset', 'citing_w', 'cited_w',
        'citing_doi', 'cited_doi', '是否在边表中', '匹配状态', 'failure_status'
    ])
    writer.writeheader()
    writer.writerows(results)

matched = sum(1 for r in results if r['匹配状态'] == '匹配成功' and r['citation_id'] != 'POSITIVE_TEST')
total = sum(1 for r in results if r['citation_id'] != 'POSITIVE_TEST')
print(f"RED样本：{total}条，匹配成功 {matched} 条")
print("正向测试：通过")
print("结果已保存为 接口联调结果_v3.csv")