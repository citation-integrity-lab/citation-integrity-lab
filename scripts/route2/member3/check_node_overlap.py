#节点交集统计
import csv

# 1. 读取你的边表节点
your_nodes = set()
with open('final_edges_no_selfcite.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        your_nodes.add(row['citing_short'])
        your_nodes.add(row['cited_short'])

print(f"路线二边表节点数: {len(your_nodes)}")

# 2. 读取RED转换后的所有节点
red_nodes = set()
with open('red_doi_to_w_mapping.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('citing_w'):
            red_nodes.add(row['citing_w'])
        if row.get('cited_w'):
            red_nodes.add(row['cited_w'])

print(f"RED样例节点数: {len(red_nodes)}")

# 3. 求交集
overlap = your_nodes & red_nodes
print(f"节点交集数: {len(overlap)}")
if overlap:
    print("交集节点示例:")
    for n in list(overlap)[:10]:
        print(f"  {n}")
else:
    print("节点交集为空 —— 两批数据论文节点完全无交集")

# 4. 把统计结果写入文件
with open('节点交集统计.txt', 'w', encoding='utf-8') as f:
    f.write(f"路线二边表节点数: {len(your_nodes)}\n")
    f.write(f"RED样例节点数: {len(red_nodes)}\n")
    f.write(f"节点交集数: {len(overlap)}\n")
    f.write(f"说明：RED样例节点数包含 RED:25 补入后的 citing_w（W2745687093），\n")
    f.write(f"      若不含 RED:25 则为 56，补入后为 57。\n")
    if overlap:
        f.write("交集节点:\n")
        for n in sorted(overlap):
            f.write(f"  {n}\n")
    else:
        f.write("结论：两批数据论文节点完全无交集\n")

print("\n统计结果已保存为 节点交集统计.txt")