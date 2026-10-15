# 路线二 成员3 脚本说明

维护人：成员3
路径：scripts/route2/member3/

## 一、脚本清单

| 脚本 | 用途 | 主要输出 |
|------|------|----------|
| `run_cidre_on_openalex.py` | 主脚本：从OpenAlex取数、构建引文网络、简化版异常检测、绘制Ego-Network、导出数据包 | final_edges_no_selfcite.csv、final_top_candidates_v2.csv、ego_network.png |
| `convert_ids_to_openalex.py` | 将RED样例的DOI批量转换为OpenAlex裸W号 | red_doi_to_w_mapping.csv |
| `fix_red25_and_check.py` | 补入RED:25的citing_w（首次查询超时，重试后HTTP 200取得W2745687093） | 更新red_doi_to_w_mapping.csv |
| `generate_interface_result_v2.py` | 生成接口联调结果v2（含RED 30条匹配状态和failure_status） | 接口联调结果_v2.csv |
| `generate_interface_result_v3.py` | 生成接口联调结果v3（含RED 30条+POSITIVE_TEST正向测试） | 接口联调结果_v3.csv |
| `check_node_overlap.py` | 统计路线二104个节点与RED 57个节点的交集 | 节点交集统计.txt |
| `positive_test.py` | 用边表内已知存在的边做正向测试，验证匹配脚本逻辑 | 控制台输出 |
| `check_5_common_samples.py` | 验证5条共同样本是否在116条边基线中 | 逐条覆盖情况 |
| `check_30_candidates.py` | 读取反向选样30条候选边xlsx，逐条核查是否在基线中 | 30条候选边核查表.csv |
| `compute_5sample_features.py` | 以route2_baseline_v1_116edges为基线，计算5条共同样本的网络特征 | 5共同样本网络特征表.csv |
| `find_5_common_samples.py` | 从RED映射表反向查找共同样本（本轮结果为0条，保留作为排查过程记录） | 控制台输出 |

## 二、关键时间节点

### 2026-09-28 至 2026-10-05
- 完成路线二基线构建，确定200节点、116条边（清洗后）。
- 数据质量预检：剔除10条年份倒挂边、跳过10条自引用边、重复边0条。
- 生成V1和V2两版评分，V2最终采用入度归一化×2.0 + 互惠比例×2.0 + 内部密度×0.5。

### 2026-10-06 至 2026-10-08
- 正式冻结 route2_baseline_v1：200节点、116条边、104个有效节点，保存全部文件SHA-256。
- 完成RED 30条样例的DOI→W号转换（30/30成功），并做PMC 5条和RED 30条的接口试连。
- 试连结果：PMC 0/5、RED 0/30，节点交集为0；正向测试通过，证明匹配脚本逻辑正确。
- 确认0命中的原因是两批数据源无交集（路线一为PMC/RED/SciFact，路线二为OpenAlex 2022-2024年200篇论文）。

### 2026-10-10 至 2026-10-11
- 成员2按固定提交 f1d82b3117fbc5b2b021d49ab8b358e67d7f0b17 独立复核，确认节点数104、RED节点数57、交集为0，与报告结论一致。
- 确认两处版本差异：说明文件中“105个有边节点”为早期数据旧值，正式以104为准；脚本哈希以当前提交版本为准。
- 成员4从网络侧反向选样，获得47条候选边，其中30条两端有PMC全文，与路线一形成5条共同样本。

### 2026-10-15
- 新增脚本：check_5_common_samples.py、check_30_candidates.py、compute_5sample_features.py、find_5_common_samples.py。
- 跑通30条候选边核查表（30条全部在基线中，5条已选为共同样本）。
- 跑通5条共同样本网络特征表（batch=route2_baseline_v1_116edges，score_v2为pending）。

## 三、使用说明

- 所有脚本均以 route2_baseline_v1_116edges 为正式基线，不再通过实时API覆盖该版本。
- 后续新增边沿用 edge_id + 6列格式。
- 不做V3权重调整。
