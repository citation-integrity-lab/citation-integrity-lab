# 仓库维护与访问

组织：[citation-integrity-lab](https://github.com/citation-integrity-lab)。
项目仓库：[citation-integrity-lab/citation-integrity-lab](https://github.com/citation-integrity-lab/citation-integrity-lab)。

## 维护原则

本库以项目问题与研究产物为中心。贡献者可在具体笔记中署名，但不把姓名、成员编号或短期任务作为主目录。

建议后续通过分支和 Pull Request 提交，文献变动核对来源，方法变动附运行依据。机器检查只覆盖文档链接与登记字段，不能替代内容审查。

## 访问和平台限制

研究内容保持私有；公开介绍若未来需要，应单独审查和制作，不自动公开本库或完整资料包。

初始化时组织为 GitHub Free。私有组织仓库的强制保护功能受账户方案限制；文档约定、模板和CI不等于已经启用强制审核。本次不修改组织套餐、既有成员权限或邀请新成员。参见[GitHub保护分支说明](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)。

## 检查工作流

`.github/workflows/check.yml` 在 push 和 pull_request 时运行 Python 标准库检查，不下载研究数据、不安装研究依赖，也不调用模型。GitHub Actions 版本固定到提交，权限仅为 contents: read。

运行记录与当前状态以[Actions页面](https://github.com/citation-integrity-lab/citation-integrity-lab/actions/workflows/check.yml)为准；配置存在本身不说明最近一次运行通过。

## 原始材料与许可证

附件指纹用于追溯，原件不在本库。代码和论文的许可证分别检查；官方仓库的代码许可不能自动覆盖第三方全文、模型权重或所有数据。源码未在本库重新分发。

全库暂不添加统一开源许可证。可分享摘要与模板不意味着原始资料可公开再分发。
