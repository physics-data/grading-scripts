# 课程评分脚本

请先使用 `python3 -m pip install -r requirements.txt` 安装依赖。

## 小作业

```bash
python3 ./assignment.py result.csv wlxt.xls [-b 100] [-w 20] [-B 80] [-W 20] [-g harry]
```

其中 `result.csv` 是 (classroom-helper)[https://github.com/jiegec/classroom-helper] 生成的 CSV 文件，`wlxt.xls` 是网络学堂导出的作业成绩模板。结果将写入 `wlxt.xls` 中。

参数：

* `-b/-B`：黑盒原始分和在总分的占比（默认为 100/80）
* `-w/-W`：白盒原始分和在总分的占比（默认为 20/20）
* `-g`：评阅人姓名（出现在评语最后）

如果 `wlxt.csv` 中找不到对应同学的分数，或者黑盒为 `N/A`，则将标记为“未交”。否则，将标记为“已交”，并相应给出分数和评语。
