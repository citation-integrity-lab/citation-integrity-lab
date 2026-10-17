import csv
import networkx as nx

# 1. 建图
G = nx.DiGraph()
with open('final_edges_no_selfcite.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        G.add_edge(row['citing_short'], row['cited_short'],
                   weight=int(row['weight']), edge_id=row['edge_id'])

# 2. 读V2候选表
v2_scores = {}
with open('final_top_candidates_v2.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        node_id = row['节点ID'].split('/')[-1]
        v2_scores[node_id] = float(row['综合得分_v2'])

# 3. 5条共同样本
samples = [
    {'edge_id': 'edge:0013', 'citing': 'W4309506674', 'cited': 'W4308616064'},
    {'edge_id': 'edge:0034', 'citing': 'W4283271244', 'cited': 'W4283381496'},
    {'edge_id': 'edge:0062', 'citing': 'W4381681857', 'cited': 'W4318923555'},
    {'edge_id': 'edge:0082', 'citing': 'W4323036511', 'cited': 'W4307425304'},
    {'edge_id': 'edge:0104', 'citing': 'W4400089962', 'cited': 'W4384522480'},
]

def safe_round(x, ndigits=4):
    """None 直接返回 None，不报错"""
    if x is None:
        return None
    return round(x, ndigits)

results = []
for s in samples:
    u, v = s['citing'], s['cited']
    in_deg = G.in_degree(u, weight='weight')
    out_deg = G.out_degree(u, weight='weight')

    # 互惠比例：出度=0 时分母为0，记 None
    out_nb = list(G.successors(u))
    if out_deg == 0:
        recip_ratio = None
    else:
        recip = sum(1 for n in out_nb if G.has_edge(n, u))
        recip_ratio = recip / out_deg

    # 内部密度：出度≤1 时分母为0，记 None
    internal = 0
    for i, n1 in enumerate(out_nb):
        for n2 in out_nb[i+1:]:
            if G.has_edge(n1, n2) or G.has_edge(n2, n1):
                internal += 1
    if out_deg <= 1:
        internal_density = None
    else:
        max_possible = out_deg * (out_deg - 1) / 2
        internal_density = internal / max_possible

    # 2跳Ego子图
    ego = nx.ego_graph(G, u, radius=2)
    ego_nodes = ego.number_of_nodes()
    ego_edges = ego.number_of_edges()

    score_v2 = v2_scores.get(u, 'pending')

    results.append({
        'batch': 'route2_baseline_v1_116edges',
        'edge_id': s['edge_id'],
        'citing_short': u,
        'cited_short': v,
        'indegree': in_deg,
        'outdegree': out_deg,
        'reciprocity': safe_round(recip_ratio),
        'internal_density': safe_round(internal_density),
        'score_v2': score_v2,
        'ego_2hop_nodes': ego_nodes,
        'ego_2hop_edges': ego_edges,
    })

with open('5共同样本网络特征表.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("已保存为 5共同样本网络特征表.csv")
for r in results:
    print(r)
