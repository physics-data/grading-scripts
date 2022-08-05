#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import pandas as pd
import sys

def fformat(f: float):
    if float(int(f)) == f:
        return f"{int(f)}"
    else:
        return f"{f:0.2f}"

# coefficient of late submission
def decay_coeff(late_days: int):
    if late_days == 0:
        return 1
    return min(0.9, 0.95 ** late_days)


def grade(
    csv_df: pd.DataFrame, xls_df: pd.DataFrame, late_df: pd.DataFrame, assignment_name: str,
    white_raw: int, white_percent: int, black_raw: int, black_percent: int,
    grader: str
) -> pd.DataFrame:

    print(f"Generating grade of {assignment_name} by {grader}")

    assert white_raw >= 0 and black_raw >= 0, "full raw score must be >= 0"
    # check if black & white box are both scored
    has_black, has_white = black_percent != 0, white_percent != 0
    if not has_black:
        print(f"WARNING: not scoring BLACK-BOX")
    if not has_white:
        print(f"WARNING: not scoring WHITE-BOX")

    assert white_percent + black_percent == 100, "black + white must be 100"

    # read input files
    late_df = late_df.query("迟交作业 == @assignment_name")
    # merge all data into one df
    merged = xls_df.merge(csv_df, on=["学号", "姓名"])
    merged = merged.merge(late_df, on=["学号", "姓名"])

    print(f"All late submissions for {assignment_name}: {late_df}")

    # generate for each student
    for i, l in merged.iterrows():
        black, white, note = l["黑盒成绩"], l["白盒成绩"], l["备注"]
        # check score
        if black > black_raw:
            print(f"WARNING: line {l} black-box overflow: {fformat(black)}/{black_raw}")
        if white > white_raw:
            print(f"WARNING: line {l} white-box overflow: {fformat(white)}/{white_raw}")
        # check submit status
        if (type(note) == float and math.isnan(note)) or (note == "nan" or note == ""):
            note = "无"
        submitted = not math.isnan(black) and not math.isnan(white)

        late_days = l["迟交天数"]
        late_submission = not math.isnan(late_days) and late_days > 0

        if submitted:
            # generate comment
            grade = 0
            detail = ""
            if has_black:
                grade += black / black_raw * black_percent
                detail += f"黑盒：{fformat(black)}/{black_raw}\n"
            if has_white:
                grade += white / white_raw * white_percent
            detail += f"总分：{fformat(grade)}\n评语：{note}\n"""
            if late_submission:
                coeff = decay_coeff(late_days)
                grade *= coeff
                detail += f"迟交天数：{late_days}\n迟交系数{coeff}"
            if grader != "":
                detail += f"\n评阅人：{grader}"
        else:
            grade = 0
            detail = "未提交"

        # workaround for web learning
        input_grade = min(grade, 100)

        merged.loc[i, "成绩"] = grade
        merged.loc[i, "提交作业状态"] = "已交"
        merged.loc[i, "成绩（录入项）"] = input_grade
        merged.loc[i, "评语（录入项）"] = detail

    return merged


if __name__ == '__main__':
    print('This file cannot be directly executed.', file=sys.stderr)
    exit(1)
