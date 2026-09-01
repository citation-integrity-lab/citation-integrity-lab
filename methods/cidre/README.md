# CIDRE：期刊群体分析

状态：`source_pinned`，尚未运行。方法元数据见[登记表](../catalog.json)。

- 论文：[Detecting anomalous citation groups in journal networks](https://www.nature.com/articles/s41598-021-93572-3)。
- 官方仓库：[skojaku/cidre](https://github.com/skojaku/cidre)。
- 固定commit：`5b582b77537407f7b975f80ffbebfa248f967611`。
- 仓库声明的代码许可证：Apache-2.0；检查日期2026-08-31。数据使用条件单独检查。

## 输入、输出与角色

输入为符合官方处理口径的期刊引用网络及必要时间信息；输出包括候选群体与相关分数。它是候选群体分析基线，不是单条引用语义判别器。

原方法以零模型识别超额引用，结合 donor/recipient 分数处理群体；不能用任意密度阈值实现后称为CIDRE。[原论文](https://www.nature.com/articles/s41598-021-93572-3)

## 复现需要补齐

1. 阅读固定版本的README和依赖，记录可实际安装的环境。
2. 核对年度网络、有效引用、边方向、权重和原始数据范围。
3. 在匹配输入要求的数据上执行官方流程，保留命令、日志和空结果。
4. 按[评估协议](../../benchmarks/README.md)说明与原实验的差异，再开展新数据适配。

截至当前没有验证安装或运行命令，因此不提供“复制即跑”的承诺。缺少时间字段或仅用小子图时，应标为简化演示，不声称忠实复现。
