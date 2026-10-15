import csv

your_edges = {}
with open('final_edges_no_selfcite.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = f"{row['citing_short']}__{row['cited_short']}"
        your_edges[key] = row['edge_id']

matched = []
with open('red_doi_to_w_mapping.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        citing = row.get('citing_w', '')
        cited = row.get('cited_w', '')
        if citing and cited:
            key = f"{citing}__{cited}"
            if key in your_edges:
                matched.append({
                    'citation_id': row['citation_id'],
                    'edge_id': your_edges[key],
                    'citing_short': citing,
                    'cited_short': cited,
                })

print(f"共找到 {len(matched)} 条共同样本")
for m in matched:
    print(m)