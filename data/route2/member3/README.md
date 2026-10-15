# 路线二 成员3 数据说明

维护人：成员3
路径：data/route2/member3/

## 一、数据清单

| 文件 | 说明 | 生成日期 |
|------|------|----------|
| `final_edges_no_selfcite.csv` | 116条边表（清洗后），六列：edge_id、citing、cited、weight、citing_short、cited_short | 2026-10-05 |
| `final_top_candidates_v2.csv` | V2 Top10候选表，含入度、出度、互惠比例、内部密度、综合得分_v2 | 2026-10-05 |
| `route2_baseline_v1_nodes_104.csv` | 104个有效边节点清单 | 2026-10-06 |
| `route2_baseline_v1说明.md` | 基线版本说明，含全部文件SHA-256 | 2026-10-06 |
| `red_doi_to_w_mapping.csv` | RED 30条样例的DOI→W号映射，含补入RED:25后的57个唯一节点 | 2026-10-07 |
| `节点交集统计.txt` | 路线二104节点与RED 57节点交集为0的统计 | 2026-10-07 |
| `接口联调结果_v2.csv` | 接口联调结果v2（RED 30条匹配状态） | 2026-10-07 |
| `接口联调结果_v3.csv` | 接口联调结果v3（RED 30条 + POSITIVE_TEST正向测试） | 2026-10-08 |
| `5共同样本网络特征表.csv` | 5条共同样本的网络特征，batch=route2_baseline_v1_116edges，score_v2为pending | 2026-10-15 |
| `30条候选边核查表.csv` | 30条候选边逐条核查结果，30条全部在基线中，5条已选为共同样本 | 2026-10-15 |

## 二、关键时间节点

### 2026-10-05
- 生成 final_edges_no_selfcite.csv（116条边）和 final_top_candidates_v2.csv（V2 Top10）。
- 清洗规则：剔除10条年份倒挂边、跳过10条自引用边、重复边0条。

### 2026-10-06
- 冻结 route2_baseline_v1：200节点、116条边、104个有效节点。
- 生成 nodes_104.csv 和版本说明（含SHA-256）。

### 2026-10-07
- RED 30条DOI→W号转换完成（30/30成功）。
- 补入RED:25的citing_w（W2745687093），首次查询超时，重试后HTTP 200。
- 统计节点交集：104 vs 57，交集为0。

### 2026-10-08
- 接口联调结果v3：RED 30条0/30，POSITIVE_TEST匹配成功。
- 确认0命中的原因是两批数据源无交集，非代码问题。

### 2026-10-15
- 新增5共同样本网络特征表和30条候选边核查表。
- 5条共同样本全部在基线中，score_v2为pending（施引方不在V2 Top10）。
- 30条候选边全部在基线中，5条已选为共同样本。

## 三、使用说明

- 正式基线为 route2_baseline_v1（116条边、104个有效节点），不再通过实时API覆盖。
- 网络指标以 final_top_candidates_v2.csv 为准，未列入候选表的节点 score_v2 为 pending。
- 所有文件哈希见 route2_baseline_v1说明.md。
