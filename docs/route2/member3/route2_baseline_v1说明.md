# route2_baseline_v1 版本说明

## 一、版本信息
- 创建日期：2026-10-06
- 维护人：成员3
- 数据源：OpenAlex
- 查询条件：publication_year:2022-2024, per-page:200
- 取数时间：2026-10-05（本次运行）

## 二、网络规模
- 节点数：200（其中105个有边）
- 边数：116条（清洗后）
- 清洗规则：剔除10条年份倒挂边、跳过10条自引用边、重复边0条

## 三、文件清单
- final_edges_no_selfcite.csv（116条边表）
- final_top_candidates_v2.csv（V2 Top10候选表）
- run_cidre_on_openalex.py（清洗脚本）

## 四、文件哈希
(venv) PS D:\Python\cidre-main\examples\route2_baseline_v1> certutil -hashfile final_edges_no_selfcite.csv SHA256
SHA256 的 final_edges_no_selfcite.csv 哈希:
85fd4d6c4b35f7febea95a26fa906421cdacc0009227cdf443725f07f394f0e2
CertUtil: -hashfile 命令成功完成。

(venv) PS D:\Python\cidre-main\examples\route2_baseline_v1> certutil -hashfile final_top_candidates_v2.csv SHA256
SHA256 的 final_top_candidates_v2.csv 哈希:
44d4e64180dd09f610a84001f6c5d3077464c4ba13a0d89ca65cb6ac9f8ea25d
CertUtil: -hashfile 命令成功完成。

(venv) PS D:\Python\cidre-main\examples\route2_baseline_v1> certutil -hashfile run_cidre_on_openalex.py SHA256
SHA256 的 run_cidre_on_openalex.py 哈希:
42a3d01a589f6742a0f7444e9827b5afc7152f1dbd2158641a158d9a3ca206d1
CertUtil: -hashfile 命令成功完成。

## 五、使用说明
- 后续实验统一使用本版本，不再通过实时API覆盖
- 新增边沿用 edge_id + 6列格式
- 不做V3权重调整