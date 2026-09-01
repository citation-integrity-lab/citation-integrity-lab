# 共享数据 Schema 草案 v0.1

这是本项目的交换格式建议，不是上游算法的原生输入，也不是已经存在的数据。字段随实际样例小步调整。

| 表 | 标识与基础字段 | 说明 |
|---|---|---|
| papers | paper_id, title, publication_year, venue_id, source | paper_id 唯一；年份/期刊缺失时为空 |
| authors | author_id, display_name, source | 不能仅按姓名合并 |
| institutions | institution_id, display_name, source | 保留来源标识符 |
| venues | venue_id, display_name, venue_type, source | 区分期刊、会议等 |
| citations | citing_paper_id, cited_paper_id, source | 一行一个已观测论文对；两者顺序不能反 |
| authorships | paper_id, author_id, author_order, source | 联合标识署名关系 |
| affiliations | paper_id, author_id, institution_id, source | 论文时点的机构证据，不用当前单位自动回填 |
| citation_contexts | instance_id, citing_paper_id, cited_paper_id, context, evidence, raw_label, source_locator | 可选；同一论文对可有多个引用位置 |
| semantic_outputs | instance_id, predicted_label, score, score_type, model_version, run_id, missing_reason | 保留无法判断；score 不默认是校准概率 |

source_locator 写页码、段落或数据库记录定位；没有该字段的表可附独立来源索引。source 不能只写“互联网”。

## 校验原则

- 表内 ID 唯一、引用与署名的外键能对上；无法对齐的数据单独登记。
- 图采样若只保留两端均在图内的边，要报告过滤前后数量。
- 区分一篇论文多次提及与一条论文引用边，不默认重复计数。
- 论文级到期刊级的聚合另写转换说明，保留时间口径。
- 真实案例可用内部 ID；导出共享版时另做去标识映射，不公开映射表。

当前没有给这些表填虚构的研究数据。需要示例时使用明显的 `synthetic:` 前缀并在文件标题注明合成数据。
