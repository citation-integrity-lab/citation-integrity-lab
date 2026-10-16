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
| `generate_node_list.py` | 从边表提取104个唯一节点清单 | route2_baseline_v1_nodes_104.csv |

## 二、按周工作记录

### 第1周（08-24 至 08-30）：文献调研与路线设计
- 完成引文卡特尔、CIDRE、Ego-Network等代表性方法的调研和比较。
- 明确路线二基本思路：先利用网络结构和异常互引指标发现可疑群体，再通过局部网络分析判断群体内部是否存在异常引用。
- 综合可复现性、公开代码和已有验证效果，确定将CIDRE作为路线二的核心baseline。
- 与成员4的分工明确：成员3负责找异常圈子，成员4负责解释圈子里的关系。
- 产出：方法调研结论、路线二技术方案、后续小规模原型验证计划。

### 第2周（08-31 至 09-06）：跑通CIDRE + Ego-Network案例
- 完成CIDRE环境搭建，用OpenAlex API取200篇论文数据。
- 构建引文网络，跑通简化版异常检测，得到Top1候选W4308616064。
- 用NetworkX的`ego_graph()`画了2跳Ego-Network图。
- 产出：CIDRE运行说明、可疑节点结果、Ego-Network图。

### 第3周（09-07 至 09-13）：修正Ego-Network + 自引用影响分析
- 把`ego_graph()`改成手动双向扩展（`predecessors`+`successors`），保证入边和出边都被包含。
- 去除自引用后重新计算，Top1从W4308616064（1.79）变为W4402754006（1.02）。
- 产出：修正后的2跳Ego图、去除自引用前后对比结果。

### 第4周（09-14 至 09-20）：数据质量清洗 + V2评分迭代
- 增加年份倒挂、自引用、重复边三项预检：发现10条倒挂、10条自引用、0条重复。
- 剔除倒挂边后，网络从130条边降到120条边，节点保持200。
- V2评分：入度改为全局最大入度归一化，权重调整为入度2.0、互惠2.0、内部密度0.5。
- 产出：清洗后边表、V2指标说明、V2 Top10候选表。

### 第5周（09-21 至 09-27）：基线冻结 + 字段映射初版
- 正式冻结`route2_baseline_v1`：200节点、116条边、104个有效节点。
- 生成`route2_baseline_v1_nodes_104.csv`和`route2_baseline_v1说明.md`（含全部SHA-256）。
- 完成路线一到路线二的字段映射初版：`citing_short`→`citing_doc_id`、`cited_short`→`cited_doc_id`。
- 产出：版本说明与哈希清单、字段映射表。

### 第6周（09-28 至 10-04）：接口试连 + 0命中排查
- RED 30条DOI→W号转换，30/30成功。
- PMC 0/5、RED 0/30，节点交集为0。
- 正向测试：用边表内已知边W4393935425→W4294189863验证，匹配成功，证明脚本逻辑正确。
- 确认0命中原因是两批数据源无交集（路线一为PMC/RED/SciFact，路线二为OpenAlex 2022-2024年200篇）。
- 产出：接口联调报告v3、接口联调结果v3、节点交集统计。

### 第7周（10-05 至 10-11）：独立复核 + 反向选样
- 成员2按固定提交`f1d82b3117fbc5b2b021d49ab8b358e67d7f0b17`独立复核，确认节点数104、RED节点数57、交集为0。
- 确认两处版本差异：说明文件中“105个有边节点”为旧值，以104为准；脚本哈希以当前提交版本`db620f0e...`为准。
- 成员4从网络侧反向选样，获得47条候选边，其中30条两端有PMC全文，与路线一形成5条共同样本。
- 产出：无新增脚本，确认接口冻结和基线版本。

### 第8周（10-12 至 10-18）：5条共同样本 + 30条候选边核查
- 新增`check_5_common_samples.py`、`check_30_candidates.py`、`compute_5sample_features.py`、`find_5_common_samples.py`。
- 跑通30条候选边核查表：30条全部在基线中，5条已选为共同样本。
- 跑通5条共同样本网络特征表：batch=`route2_baseline_v1_116edges`，score_v2为pending（施引方不在V2 Top10）。
- 产出：5共同样本网络特征表.csv、30条候选边核查表.csv、扩样设计说明.md。

## 三、使用说明

- 所有脚本均以`route2_baseline_v1_116edges`为正式基线，不再通过实时API覆盖该版本。
- 后续新增边沿用`edge_id + 6列格式`。
- 不做V3权重调整。
- `score_v2`只从`final_top_candidates_v2.csv`读取，未列入候选表的节点保持pending，不自行套公式。
