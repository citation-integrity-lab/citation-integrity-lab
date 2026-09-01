# Citation Integrity Lab
## 学术引文诚信研究共享库

[![Repository checks](https://github.com/citation-integrity-lab/citation-integrity-lab/actions/workflows/check.yml/badge.svg)](https://github.com/citation-integrity-lab/citation-integrity-lab/actions/workflows/check.yml)

围绕**学术引文不端行为的识别、解释与治理**，沉淀可追溯的文献调研、数据规范、方法复现、实验评估和案例证据。

研究项目：基于大模型语义理解与知识图谱推理的学术引文不端行为识别及治理研究。

本库按研究内容和成果类型组织，不绑定人员分工或短期任务。文献、方法、实验和案例各自保留来源与版本，并通过链接关联。

> 异常信号不等于学术不端认定。内容相关、结构密集或存在合作关系，都需要放在具体证据和正常学术行为背景下解释。

## 项目研究什么

| 研究环节 | 核心问题 | 主要成果 |
|---|---|---|
| 引用语义核验 | 具体引用陈述能否得到被引原文支持？ | 标签定义、证据定位、错误分析 |
| 引文网络分析 | 哪些引用模式超出合理的比较基准？ | 候选群体、网络指标与局部关系 |
| 学术知识图谱 | 论文、作者、机构、期刊如何关联？ | 有出处、带时点的实体与关系 |
| 多源证据融合 | 语义、结构和行为证据能否相互补充？ | 可解释的候选排序与不确定性 |
| 实验评估 | 方法在何种数据与条件下有效？ | 基线比较、消融、误报和复现记录 |
| 治理衔接 | 如何把研究输出转成可复核材料？ | 证据清单、复核流程与使用边界 |

完整说明见[项目概览](docs/project_overview.md)与[技术路线](docs/research_map.md)。

## 按目的查找

| 想找什么 | 入口 |
|---|---|
| 了解项目、开始参与 | [快速导航](docs/start_here.md) · [研究路线图](docs/roadmap.md) |
| 文献和调研方法 | [文献库](literature/README.md) · [检索与精读协议](literature/search_protocol.md) |
| 数据来源、字段和标注 | [数据目录](data/README.md) · [共享 Schema](data/schema.md) · [标注原则](data/annotation.md) |
| 方法原理与复现入口 | [方法库](methods/README.md) · [方法登记表](methods/catalog.json) |
| 如何设计实验 | [评估协议](benchmarks/README.md) · [实验记录](experiments/README.md) |
| 案例证据与治理 | [案例库](cases/README.md) · [治理与复核](governance/README.md) |
| 项目成果到哪一步 | [项目状态](docs/status.md) · [研究讨论记录](discussions/README.md) |
| 提交成果 | [贡献指南](CONTRIBUTING.md) · [模板](templates/README.md) |
| 核对来源与使用权限 | [来源核验](docs/source_audit.md) · [来源指纹](docs/source_manifest.json) · [维护说明](docs/maintenance.md) |

## 当前可用内容

已整理研究框架、四个专题的调研入口、数据与标注约定、六类方法说明、评估协议和证据模板。CIDRE 与 Citation-Integrity 官方代码来源已登记固定 commit 和仓库声明的许可证。

**当前尚未提交基线运行日志、真实检测结果或经独立复核的实验指标。** 方法登记和 CI 通过只说明资料与仓库结构经过检查，不代表算法已复现。

## 目录

```text
docs/          项目概览、路线图、状态与维护
literature/    专题调研、检索方法和来源
data/          数据目录、Schema、标注与数据卡
methods/       语义、网络、图谱和证据融合方法
benchmarks/    评估设计、指标与对照规则
experiments/   可复现的单次运行与结果记录
cases/         脱敏案例与人工复核材料
governance/    证据标准、复核流程和使用边界
discussions/   研究问题、决策与阶段总结
templates/     文献、数据、方法、实验、案例模板
.github/       协作模板与文档检查工作流
scripts/       仓库资料检查工具
```

## 参与和检查

复制[对应模板](templates/README.md)，补充来源、内容与局限，放入相应主题目录，通过 Pull Request 供他人复核。无需同时承担所有研究环节。

```bash
git clone https://github.com/citation-integrity-lab/citation-integrity-lab.git
cd citation-integrity-lab
python scripts/check_repository.py
```

私有仓库需要已获授权的 GitHub 账号。文档检查使用 Python 3.10+ 标准库，不安装研究模型、不下载数据、不调用外部模型。

原始全文、非公开资料、真实身份映射和大型数据通过有权限控制的存储管理；不要上传密钥、模型权重或授权不明的材料。本库暂不统一授予开源许可。
