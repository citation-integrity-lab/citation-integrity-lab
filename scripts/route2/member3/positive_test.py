import csv

# 从你的边表里挑一条真实存在的边（例如 edge:0001） 正向测试（用一条已知存在的真实边）
test_citing = "W4393935425"
test_cited = "W4294189863"

# 构造测试样本
test_key = f"{test_citing}__{test_cited}"

# 用和check_interface_samples_v3相同的匹配逻辑
your_edges = set()
with open('final_edges_no_selfcite.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = f"{row['citing_short']}__{row['cited_short']}"
        your_edges.add(key)

print(f"测试边: {test_citing} → {test_cited}")
print(f"测试边key: {test_key}")
print(f"是否在边表中: {test_key in your_edges}")
print()
if test_key in your_edges:
    print("正向测试通过：匹配脚本能正确识别存在的边")
else:
    print("正向测试失败：匹配逻辑有问题，需检查")