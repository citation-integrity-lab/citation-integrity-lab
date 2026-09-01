# 来源核验与研究口径

核查日期：2026-08-31。本文按材料和论断登记状态，不按提交人评价成果。

## 资料基础

| 编号 | 材料 | 本库用途 |
|---|---|---|
| S01 | 项目“学术引文不端治理”上下文 | 项目目标、研究对象和两路线设计 |
| S02 | plan(1).pdf | 数据集线索与联合分析原则 |
| S03 | 精读报告(1).docx | 网络方法摘要与候选参考 |
| S04 | 图算法对比表(1).xlsx | 方法定位与字段线索 |
| S05 | 调研报告.docx | 图谱、证据融合与治理线索 |

原始附件未重新分发，指纹见[source_manifest.json](source_manifest.json)。本库没有收录原始对话、预算和人员任务安排。

## 已核对的核心来源

- [Sarol 2024论文记录](https://pubmed.ncbi.nlm.nih.gov/38924508/)与[作者仓库](https://github.com/ScienceNLP-Lab/Citation-Integrity)。
- [SciCiteVal LREC 2026论文](https://aclanthology.org/2026.lrec-1.125/)与[作者数据卡](https://huggingface.co/datasets/birdie0111/SciCiteVal)。
- [CIDRE 2021论文](https://www.nature.com/articles/s41598-021-93572-3)与[官方仓库](https://github.com/skojaku/cidre)。
- [Gupta等2026预印本](https://arxiv.org/abs/2607.06528)：核对到研究存在与基本主题，未完成工件或性能核验。

两个官方代码来源的固定commit和仓库声明许可证见[方法登记表](../methods/catalog.json)。这是代码来源登记，不是已安装或运行的证明。

## 待核验清单

| 条目 | 当前证据缺口 | 进入正式结论前需要 |
|---|---|---|
| Scholarly Knowledge Graph Anomaly Detection via Relational Graph Neural Networks（材料称Zhang 2024 WWW） | 精确题名检索未找到匹配可靠出版记录 | DOI、正式会议条目或原文 |
| Multi-dimensional Evidence Fusion for Citation Misconduct Detection and Governance（材料称Li 2023 JCDL） | 同上 | 正式出处与对应实验表 |
| Davis 的Ego-Network报告 | 题名、年份、来源类型不够确定 | 原报告或可信存档 |
| Gupta方法的代码与数据公开性 | 原材料描述不一致，未取得完整运行工件 | 实际代码、数据版本及授权 |
| Gupta方法的具体相关系数与鲁棒性数字 | 未完成逐表核验 | 原文表号、数据、指标与设置 |
| COPE引用操纵讨论文件 | 已定位官方候选入口，尚未逐条精读 | 核对版本和原文后再总结具体建议 |

未检索到不等于证明文献不存在。存疑条目不进入正式效果对比，也不把性能数字当作项目已有结果。

## 统一口径

- 支持核验不等于摘要相似度，也不等于引用意图分类。
- 构造错误样本上的比例不能用作现实不端发生率。
- CIDRE的统计边关系不直接判定具体引用语义“多余”。
- SCC是通过有向路径相互可达，不等于两两直接互引。
- 闭世界子图仅限定保留边的端点，不能消除网络边界偏差。
- 候选群体、统计显著性、关系事实和人工结论分别记录。
- 旧材料中的风险级数与加权建议并非已验证标准，本库不直接采用。
