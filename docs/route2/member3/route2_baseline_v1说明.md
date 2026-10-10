# route2_baseline_v1 版本说明

## 一、版本信息
- 创建日期：2026-10-06
- 维护人：成员3
- 数据源：OpenAlex
- 查询条件：publication_year:2022-2024, per-page:200
- 取数时间：2026-10-05（本次运行）

## 二、网络规模
- 节点数：200（其中104个有边）
- 边数：116条（清洗后）
- 清洗规则：剔除10条年份倒挂边、跳过10条自引用边、重复边0条
- 说明：200为OpenAlex取数节点总数；116条边表的端点并集为104，即实际有引用关系的节点。此前出现的105为早期运行残留，已作废。正式基线以 route2_baseline_v1_nodes_104.csv 为准。

## 三、文件清单
- final_edges_no_selfcite.csv（116条边表）
- final_top_candidates_v2.csv（V2 Top10候选表）
- run_cidre_on_openalex.py（清洗脚本）
- route2_baseline_v1_nodes_104.csv（104个唯一节点清单）
- red_doi_to_w_mapping.csv（RED 30条映射，57个唯一节点）

## 四、文件哈希
### 4.1 final_edges_no_selfcite.csv
SHA256: 85fd4d6c4b35f7febea95a26fa906421cdacc0009227cdf443725f07f394f0e2

### 4.2 final_top_candidates_v2.csv
SHA256: 44d4e64180dd09f610a84001f6c5d3077464c4ba13a0d89ca65cb6ac9f8ea25d

### 4.3 run_cidre_on_openalex.py
SHA256: db620f0ee41ec03662b04ef6ac250277b745ce02d84282cfe311cfaf31cd45fb

### 4.4 route2_baseline_v1_nodes_104.csv
SHA256: fbef74100fd926b314ab917079ac05932109d9bffcea521478494bcee11cc406

### 4.5 red_doi_to_w_mapping.csv
SHA256: 7305ea2f6775ca3a899dd9913d3fa5e91fc947e8120cff8bcb62b037447eb637


## 五、使用说明
- 后续实验统一使用本版本，不再通过实时API覆盖
- 新增边沿用 edge_id + 6列格式
- 不做V3权重调整
