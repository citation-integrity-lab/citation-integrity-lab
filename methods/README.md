# 方法库

按算法角色和分析单位组织，保持方法来源、实现和运行记录可追溯。

| 方法 | 分析单位与用途 | 状态 | 档案 |
|---|---|---|---|
| 引用证据核验 | 引用实例；证据检索与支持判别 | 来源已固定，未运行 | [semantic](semantic/README.md) |
| CIDRE | 期刊网络；候选群体分析 | 来源已固定，未运行 | [cidre](cidre/README.md) |
| Ego-Network | 指定粒度节点；局部关系解释 | 方案 | [ego_network](ego_network/README.md) |
| 社区与可达性分析 | 有向图；社区、SCC等结构对照 | 方案 | [community](community/README.md) |
| 最小知识图谱 | 论文、作者、机构、期刊 | Schema方案 | [knowledge_graph](knowledge_graph/README.md) |
| 多源证据融合 | 引用、群体或案例，需明确映射 | 研究方案 | [evidence_fusion](evidence_fusion/README.md) |

机器登记见[catalog.json](catalog.json)，状态定义见[项目状态](../docs/status.md)。本库目前没有伪装成运行实现的空函数，也没有虚构结果。

## 新增或复现方法

复制[方法模板](../templates/method.md)，记录论文、上游、固定版本、许可、输入输出和适用边界。真正运行后另建[实验记录](../experiments/README.md)。第三方源码未经许可核查不直接拷贝；新增依赖放在该方法独立环境中，不把所有研究环境混在一起。
