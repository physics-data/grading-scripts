#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import click
import pandas as pd


def fformat(f: float):
    if float(int(f)) == f:
        return f"{int(f)}"
    else:
        return f"{f:0.2f}"


@click.command(help="Automatically generate grading for web learning.")
@click.argument("input_csv", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_xls", type=click.Path(exists=True, dir_okay=False, writable=True))
@click.option("-w", "--white-raw", type=click.INT, default=20, help="full raw score (white box)")
@click.option("-W", "--white-percent", type=click.IntRange(0, 100), default=20, help="white box precentage")
@click.option("-b", "--black-raw", type=click.INT, default=100, help="full raw score (black box)")
@click.option("-B", "--black-percent", type=click.IntRange(0, 100), default=80, help="black box precentage")
@click.option("-g", "--grader", type=click.STRING, default="", help="name of grader")
def grade(
    input_csv: str, output_xls: str, white_raw: int, white_percent: int, black_raw: int, black_percent: int, grader: str
):
    assert white_raw >= 0 and black_raw >= 0, "full raw score must be >= 0"
    # check if black & white box are both scored
    only_white = 0
    if black_percent == 0:
        only_white = 1
        print(f"WARNING: ONLY WHITE-box is scoring")
    if white_percent == 0:
        only_white = -1
        print(f"WARNING: ONLY BLACK-box is scoring")
    assert white_percent + black_percent == 100, "black + white must be 100"
    csv_df = pd.read_csv(input_csv)
    xls_df = pd.read_excel(output_xls)
    merged = xls_df.merge(csv_df, on=["学号", "姓名"])

    # generate for each student
    for i, l in merged.iterrows():
        black, white, note = l["黑盒成绩"], l["白盒成绩"], l["备注"]
        # check score
        if black > black_raw:
            print(f"WARNING: line {l} blackbox overflow: {fformat(black)}/{black_raw}")
        if white > white_raw:
            print(f"WARNING: line {l} white overflow: {fformat(white)}/{white_raw}")
        # check submit status
        if (type(note) == float and math.isnan(note)) or (note == "nan" or note == ""):
            note = "无"
        submitted = not math.isnan(black) and not math.isnan(white)
        if submitted:
            if only_white == 1:
                grade = white / white_raw * white_percent
                detail = f"白盒：{fformat(white)}/{white_raw}\n总分：{fformat(grade)}\n评语：{note}"
            else:
                grade = black / black_raw * black_percent + white / white_raw * white_percent
                detail = (
                    f"黑盒：{fformat(black)}/{black_raw}\n白盒：{fformat(white)}/{white_raw}\n总分：{fformat(grade)}\n评语：{note}"
                )
            if grader != "":
                detail += f"\n评阅人：{grader}"
        else:
            grade = 0
            detail = "未提交"
        merged.loc[i, "提交作业状态"] = "已交"
        merged.loc[i, "成绩（录入项）"] = grade
        merged.loc[i, "评语（录入项）"] = detail

    # save back to xls
    merged.to_excel(output_xls, index=False, columns=["学生作业id", "学号", "姓名", "提交作业状态", "成绩（录入项）", "评语（录入项）"])


if __name__ == "__main__":
    grade()
