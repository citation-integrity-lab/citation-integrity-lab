# 引用语义与标注研究

研究问题：引用上下文中的具体主张，是否得到被引原文的支持？这与主题相似度、引用意图和研究者动机是不同任务。

## Sarol 等，2024

Assessing citation integrity in biomedical publications: corpus annotation and NLP models。

该工作标注了100篇高被引生物医学论文相关的3,063个引用实例，结合引用上下文和证据进行核验。最佳流程使用 BM25、MonoT5 重排与微调 MultiVerS，不是简单比较两个摘要。[论文记录](https://pubmed.ncbi.nlm.nih.gov/38924508/)

[作者代码与数据](https://github.com/ScienceNLP-Lab/Citation-Integrity)按被引论文划分训练、开发、测试，分别涉及70、10、20篇。原始标签与官方划分应保留。

## 可复用方法

先检索证据，再判断支持关系，最后分析错误。实验中必须分开衡量检索缺失与判别错误，避免把没有检索到支持误判成原文不支持。

## 本项目中的衔接

[语义方法档案](../../methods/semantic/README.md)记录固定上游来源；[标注原则](../../data/annotation.md)说明原始标签、未知类别和质量控制；[评估协议](../../benchmarks/README.md)约束数据拆分与指标。
