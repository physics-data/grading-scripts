# 课程评分脚本

请先使用 `python3 -m pip install -r requirements.txt` 安装依赖。

## 小作业

```bash
python3 ./grade_assignment.py result.csv late.csv aplusb wlxt.xls [-b 80] [-w 20] [-B 80] [-W 20] [-g harry]
```

参数：

* `result.csv` 是 [classroom-helper](https://git.tsinghua.edu.cn/physics-data/vscode-course-helper) 生成的 CSV 文件
* `late.csv` 是迟交 CSV 文件，包含四列：`学号`、`姓名`、`迟交作业`、`迟交天数`
* `aplusb` 替换为作业名称（用于匹配 `late.csv` 的记录）
* `wlxt.xls` 是网络学堂导出的作业成绩模板（结果将原地写入其中）

选项：

* `-b/-B`：黑盒原始分和在总分的占比（默认为 80/80）
* `-w/-W`：白盒原始分和在总分的占比（默认为 20/20）
* `-g`：评阅人姓名（出现在评语最后）

如果 `wlxt.csv` 中找不到对应同学的分数，或者黑盒为 `N/A`，则将标记为“未交”。否则，将标记为“已交”，并相应给出分数和评语。
