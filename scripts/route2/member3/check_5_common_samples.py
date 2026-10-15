import csv

# 读基线边表
baseline_edges = set()
baseline_nodes = set()
with open('final_edges_no_selfcite.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        baseline_edges.add(f"{row['citing_short']}__{row['cited_short']}")
        baseline_nodes.add(row['citing_short'])
        baseline_nodes.add(row['cited_short'])

# 读5条共同样本
samples = [
    ("edge:0013", "W4309506674", "W4308616064"),
    ("edge:0034", "W4283271244", "W4283381496"),
    ("edge:0062", "W4381681857", "W4318923555"),
    ("edge:0082", "W4323036511", "W4307425304"),
    ("edge:0104", "W4400089962", "W4384522480"),
]

print("5条共同样本在116条边基线中的覆盖情况：")
for eid, citing, cited in samples:
    key = f"{citing}__{cited}"
    citing_in = citing in baseline_nodes
    cited_in = cited in baseline_nodes
    edge_in = key in baseline_edges
    print(f"{eid}: citing={citing} 在基线={citing_in}, cited={cited} 在基线={cited_in}, 整条边在基线={edge_in}")