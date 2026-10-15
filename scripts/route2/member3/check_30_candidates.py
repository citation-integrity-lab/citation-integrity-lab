import csv
import pandas as pd

# 读基线边表
your_edges = set()
with open('final_edges_no_selfcite.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        your_edges.add(f"{row['citing_short']}__{row['cited_short']}")

# 读xlsx候选边
df = pd.read_excel('反向选样_优先候选边30条_覆盖核查版_20261015.xlsx',
                   sheet_name='30条候选边明细')

results = []
for _, row in df.iterrows():
    edge_id = row['edge_id']
    citing = row['施引W号']
    cited = row['被引W号']
    is_selected = row['是否已选为共同样本']

    key = f"{citing}__{cited}"
    in_baseline = key in your_edges

    results.append({
        'edge_id': edge_id,
        'citing_short': citing,
        'cited_short': cited,
        '是否已选为共同样本': is_selected,
        '是否在116条边基线中': '是' if in_baseline else '否',
        '施引期刊': row['施引期刊'],
        '被引期刊': row['被引期刊'],
        '年份差': row['年份差(施引-被引)'],
        '两端同刊': row['两端同刊'],
        '失败原因': '' if in_baseline else 'network_coverage_missing',
    })

with open('30条候选边核查表.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

in_count = sum(1 for r in results if r['是否在116条边基线中'] == '是')
selected = sum(1 for r in results if '是' in r['是否已选为共同样本'])
print(f"共{len(results)}条候选，其中{in_count}条在基线中，{selected}条已选为共同样本")