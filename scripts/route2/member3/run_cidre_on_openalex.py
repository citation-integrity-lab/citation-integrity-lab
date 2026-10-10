# ============================================================
# 学术引文不端识别项目-成员3
# 功能：从 OpenAlex 获取论文数据，构建引文网络，简化版异常检测，
#       绘制 Ego-Network，导出数据包
# ============================================================

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import networkx as nx
import cidre
from collections import Counter
import csv
import matplotlib.pyplot as plt


# ============================================================
# 一、配置
# ============================================================
API_KEY = ""     # 请替换为自己的 OpenAlex API Key


# ============================================================
# 二、获取 OpenAlex 数据
# ============================================================
params = {
    "filter": "publication_year:2022-2024",
    "per-page": 200,
}
url = "https://api.openalex.org/works"
response = requests.get(url, params=params)

if response.status_code != 200:
    print(f"请求失败: {response.status_code}")
    exit()

data = response.json()
works = data.get("results", [])
print(f"获取到 {len(works)} 篇论文")


# ============================================================
# 三、构建引用网络
# ============================================================
G = nx.DiGraph()

# 3.1 添加所有论文节点
for work in works:
    paper_id = work.get("id")
    if paper_id:
        G.add_node(paper_id)

# 3.2 统计引用边
edge_counts = Counter()
for work in works:
    citing = work.get("id")
    if not citing:
        continue
    for cited in work.get("referenced_works", []):
        if cited:
            edge_counts[(citing, cited)] += 1


# 论文ID -> 发表年份 的字典，给后面过滤倒挂边使用
year_map = {}
for work in works:
    pid = work.get("id")
    if pid:
        year_map[pid] = work.get("publication_year", None)
# 3.3 把边加入图：跳过自引用 + 跳过年份倒挂边，只保留两端都在图中的边
for (citing, cited), count in edge_counts.items():
    if citing == cited:  # 跳过自引用
        continue
    # 跳过年份倒挂：引用论文发表年份 < 被引论文发表年份
    citing_year = year_map.get(citing)
    cited_year = year_map.get(cited)
    if citing_year and cited_year and citing_year < cited_year:
        continue
    if citing in G and cited in G:
        G.add_edge(citing, cited, weight=count)


print(f"\n网络构建完成：节点数 = {G.number_of_nodes()}，边数 = {G.number_of_edges()}")

if G.number_of_edges() < 5:
    print("\n边数太少，CIDRE可能无法检测出群体。建议增加数据量。")
else:
    print("\n网络数据充足，可以尝试运行CIDRE。")



# ---------- 数据质量检查：年份倒挂、自引用、重复边 ----------
print("\n===== 引文网络数据质量检查 =====")
# 论文ID -> 发表年份 的字典

# 1. 年份倒挂检查：引用论文年份 < 被引论文年份
reverse_edges = []
for (citing, cited) in edge_counts:
    citing_year = year_map.get(citing)
    cited_year = year_map.get(cited)
    if citing_year and cited_year and citing_year < cited_year:
        reverse_edges.append((citing, cited, citing_year, cited_year))

print(f"发现年份倒挂边数量: {len(reverse_edges)}")
for e in reverse_edges[:10]:
    print(f"  {e[0].split('/')[-1]} ({e[2]}) -> {e[1].split('/')[-1]} ({e[3]})")

# 2. 自引用检查
self_cites = [(c, d) for (c, d) in edge_counts if c == d]
print(f"自引用边数量: {len(self_cites)}")

# 3. 重复边检查（同一对节点多次引用）
duplicates = {k: v for k, v in edge_counts.items() if v > 1}
print(f"重复边数量: {len(duplicates)}")
if len(duplicates) > 0:
    print("前5组重复边：")
    for idx, (k, v) in enumerate(list(duplicates.items())[:5]):
        print(f"  {k[0].split('/')[-1]} → {k[1].split('/')[-1]} 重复次数:{v}")

print("===== 数据质量检查结束 =====\n")


# ============================================================
# 四、简化版异常群体检测 V1 + V2双版本
# ============================================================
print("\n开始简化版异常检测...")

def calculate_scores(G):
    """V1原始版本：入度比例*2 + 互惠比例*1.5 + 内部密度*1.0"""
    results = {}
    for node in G.nodes():
        in_deg = G.in_degree(node, weight='weight')
        out_deg = G.out_degree(node, weight='weight')
        # 互惠性（双向引用比例）
        reciprocals = 0
        for neighbor in G.neighbors(node):
            if G.has_edge(neighbor, node):
                reciprocals += 1
        recip_ratio = reciprocals / (G.out_degree(node) + 1e-6)
        # 入度异常（被引比例）
        total_in = sum(dict(G.in_degree(weight='weight')).values())
        in_ratio = in_deg / (total_in + 1e-6)
        # 内部密度（邻居之间互相引用比例）
        neighbors = list(G.neighbors(node))
        internal_edges = 0
        for i, n1 in enumerate(neighbors):
            for n2 in neighbors[i+1:]:
                if G.has_edge(n1, n2) or G.has_edge(n2, n1):
                    internal_edges += 1
        max_possible = len(neighbors) * (len(neighbors) - 1) / 2 if len(neighbors) > 1 else 1
        internal_density = internal_edges / (max_possible + 1e-6)
        # 综合得分 V1
        score = in_ratio * 2 + recip_ratio * 1.5 + internal_density
        results[node] = {
            'in_degree': in_deg,
            'out_degree': out_deg,
            'recip_ratio': recip_ratio,
            'internal_density': internal_density,
            'total_score': score
        }
    return results


def calculate_scores_v2(G):
    """V2改进版本：全局最大入度归一化；调整权重：入度2.0，互惠2.0，内部密度0.5"""
    results = {}
    # 先算全局最大入度，用于归一化
    max_in = max([G.in_degree(n, weight='weight') for n in G.nodes()]) or 1

    for node in G.nodes():
        in_deg = G.in_degree(node, weight='weight')
        out_deg = G.out_degree(node, weight='weight')

        # 互惠性
        reciprocals = 0
        for neighbor in G.neighbors(node):
            if G.has_edge(neighbor, node):
                reciprocals += 1
        recip_ratio = reciprocals / (G.out_degree(node) + 1e-6)

        # 入度归一化（用绝对值除以全局最大值）
        in_ratio = in_deg / max_in

        # 内部密度
        neighbors = list(G.neighbors(node))
        internal_edges = 0
        for i, n1 in enumerate(neighbors):
            for n2 in neighbors[i+1:]:
                if G.has_edge(n1, n2) or G.has_edge(n2, n1):
                    internal_edges += 1
        max_possible = len(neighbors) * (len(neighbors) - 1) / 2 if len(neighbors) > 1 else 1
        internal_density = internal_edges / (max_possible + 1e-6)

        # V2 权重调整：入度2.0，互惠2.0，内部密度0.5
        score = in_ratio * 2.0 + recip_ratio * 2.0 + internal_density * 0.5
        results[node] = {
            'in_degree': in_deg,
            'out_degree': out_deg,
            'recip_ratio': recip_ratio,
            'internal_density': internal_density,
            'total_score': score
        }
    return results


# 同时计算两套得分
scores_v1 = calculate_scores(G)      # 旧版V1
scores_v2 = calculate_scores_v2(G)   # 新版V2

sorted_nodes_v1 = sorted(scores_v1.items(), key=lambda x: x[1]['total_score'], reverse=True)
sorted_nodes_v2 = sorted(scores_v2.items(), key=lambda x: x[1]['total_score'], reverse=True)

# 打印V1 Top5（原有控制台输出不变，绘图仍然使用V1的top1节点）
scores = scores_v1
sorted_nodes = sorted_nodes_v1

print("\n【V1原始评分】最可疑的节点（Top 5）:")
for i, (node, score) in enumerate(sorted_nodes_v1[:5]):
    print(f"  {i+1}. 节点: {node[:40]}...")
    print(f"    入度={score['in_degree']}, 出度={score['out_degree']}")
    print(f"    互惠比例={score['recip_ratio']:.2f}, 内部密度={score['internal_density']:.2f}")
    print(f"    综合得分={score['total_score']:.2f}")

# 打印V2 Top5，方便控制台直接对比
print("\n【V2改进评分】最可疑的节点（Top 5）:")
for i, (node, score) in enumerate(sorted_nodes_v2[:5]):
    print(f"  {i+1}. 节点: {node[:40]}...")
    print(f"    入度={score['in_degree']}, 出度={score['out_degree']}")
    print(f"    互惠比例={score['recip_ratio']:.2f}, 内部密度={score['internal_density']:.2f}")
    print(f"    综合得分={score['total_score']:.2f}")



# ============================================================
# 五、绘制 Top 1 节点的 Ego-Network（2跳范围，双向扩展）
# ============================================================
print("\n正在绘制 Top 1 嫌疑节点的 Ego-Network...")
top_node = sorted_nodes[0][0]
print(f"选择节点: {top_node}")

# 5.1 双向2跳扩展
ego_nodes = set([top_node])
neighbors_1 = set()

for neighbor in G.predecessors(top_node):   # 入边
    neighbors_1.add(neighbor)
for neighbor in G.successors(top_node):     # 出边
    neighbors_1.add(neighbor)

neighbors_2 = set(neighbors_1)
for n1 in neighbors_1:
    for neighbor in G.predecessors(n1):
        neighbors_2.add(neighbor)
    for neighbor in G.successors(n1):
        neighbors_2.add(neighbor)

ego_nodes = set([top_node]) | neighbors_1 | neighbors_2
ego_graph = G.subgraph(ego_nodes).copy()

# 5.2 绘图
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(14, 9))
pos = nx.shell_layout(ego_graph, nlist=[[top_node], list(ego_graph.nodes() - {top_node})])

node_colors = ['red' if n == top_node else 'skyblue' for n in ego_graph.nodes()]
nx.draw_networkx_nodes(ego_graph, pos, node_color=node_colors, node_size=400)

# 黑色边 + 灰色箭头
nx.draw_networkx_edges(ego_graph, pos, alpha=0.7, edge_color='black', arrows=False)
nx.draw_networkx_edges(
    ego_graph, pos, alpha=0.7, edge_color='gray',
    arrows=True, arrowsize=15, node_size=800
)

# 标签
labels = {n: n.split('/')[-1] for n in ego_graph.nodes()}
label_pos = {n: (pos[n][0], pos[n][1] + 0.50) for n in ego_graph.nodes()}
nx.draw_networkx_labels(ego_graph, pos, labels, font_size=9)

plt.title(f"Ego-Network (2跳范围) 中心: {top_node.split('/')[-1]}", fontsize=14)

plt.tight_layout()
plt.savefig("ego_network.png", dpi=600, bbox_inches='tight')
print("图已保存为 ego_network.png")




# ============================================================
# 六、导出数据包（供成员4使用）
# ============================================================
print("\n正在导出边列表供成员4使用...")

# 6.1 完整边表（去自引用后的全局图）
with open('edges.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['edge_id', 'citing', 'cited', 'weight', 'citing_short', 'cited_short'])
    for i, (u, v, data) in enumerate(G.edges(data=True), start=1):
        w = data.get('weight', 1)
        edge_id = f"edge:{i:04d}"
        u_short = u.split('/')[-1]
        v_short = v.split('/')[-1]
        writer.writerow([edge_id, u, v, w, u_short, v_short])

# 6.2 中心节点数据包（五项指标）
print("\n 正在导出中心节点数据包...")
with open('center_node_package.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['指标', '数值'])
    writer.writerow(['节点ID', top_node])
    writer.writerow(['入度', scores[top_node]['in_degree']])
    writer.writerow(['出度', scores[top_node]['out_degree']])
    writer.writerow(['互惠比例', round(scores[top_node]['recip_ratio'], 4)])
    writer.writerow(['内部密度', round(scores[top_node]['internal_density'], 4)])
    writer.writerow(['综合异常得分', round(scores[top_node]['total_score'], 4)])
print("中心节点数据包已导出为 center_node_package.csv")

# 6.3 中心节点2跳Ego边数据
with open('center_node_ego_edges.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['citing', 'cited', 'weight'])
    for u, v, data in ego_graph.edges(data=True):
        w = data.get('weight', 1)
        writer.writerow([u, v, w])
print("中心节点2跳Ego边数据已导出为 center_node_ego_edges.csv")


# ============================================================
# 七、保存最终版本数据（统一口径）
# ============================================================
print("\n正在保存最终版本数据...")

# 7.1 最终边表
with open('final_edges_no_selfcite.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['edge_id', 'citing', 'cited', 'weight', 'citing_short', 'cited_short'])
    for i, (u, v, data) in enumerate(G.edges(data=True), start=1):
        w = data.get('weight', 1)
        edge_id = f"edge:{i:04d}"          # edge:0001 格式
        u_short = u.split('/')[-1]
        v_short = v.split('/')[-1]
        writer.writerow([edge_id, u, v, w, u_short, v_short])

# 7.2 Top候选节点列表及指标
# =========导出V1改进版候选节点列表==========
with open('final_top_candidates.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['排名', '节点ID', '入度', '出度', '互惠比例', '内部密度', '综合得分'])
    for i, (node, score) in enumerate(sorted_nodes[:10]):
        writer.writerow([
            i + 1,
            node,
            score['in_degree'],
            score['out_degree'],
            round(score['recip_ratio'], 4),
            round(score['internal_density'], 4),
            round(score['total_score'], 4)
        ])

print("最终边表已保存为 final_edges_no_selfcite.csv")
print("Top候选节点列表已保存为 final_top_candidates.csv")
# =========导出V2改进版候选节点列表==========
with open('final_top_candidates_v2.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['排名', '节点ID', '入度', '出度', '互惠比例', '内部密度', '综合得分_v2'])
    for i, (node, score) in enumerate(sorted_nodes_v2[:10]):
        writer.writerow([
            i + 1,
            node,
            score['in_degree'],
            score['out_degree'],
            round(score['recip_ratio'], 4),
            round(score['internal_density'], 4),
            round(score['total_score'], 4)
        ])
print("Top候选节点列表【V2改进版】已保存为 final_top_candidates_v2.csv")


# ============================================================
# 八、打印数据版本说明与对比结果
# ============================================================
print("\n 数据版本说明：")
print(f"  节点总数：{G.number_of_nodes()}")
print(f"  去除自引用后边数：{G.number_of_edges()}")
print(f"  最终Top 1节点：{top_node}")
print(f"  最终Top 1得分：{round(scores[top_node]['total_score'], 4)}")

print("\n去除自引用后的 Top 5:")
for i, (node, score) in enumerate(sorted_nodes[:5]):
    print(f"  {i+1}. {node[:40]}... 得分={score['total_score']:.2f}")

print("\n对比说明：")
print("  本次运行已去除自引用（citing == cited 的边被跳过）")
print(f"  去除自引用后网络边数：{G.number_of_edges()} 条")
print(f"  最终Top 1节点：{top_node.split('/')[-1]}")
print(f"  最终Top 1得分：{round(scores[top_node]['total_score'], 4)}")

# 获取并打印中心论文标题（带异常保护）
try:
    r = requests.get(f"https://api.openalex.org/works/{top_node.split('/')[-1]}", timeout=10)
    if r.status_code == 200:
        print(f"\n中心论文标题：{r.json().get('title', '未知')}")
    else:
        print(f"\n获取标题失败，状态码：{r.status_code}")
except Exception as e:
    print(f"\n获取标题时网络异常：{e}")
    print("（不影响前面已生成的数据和图表）")
