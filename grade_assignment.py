#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import pandas as pd
import grade_util

@click.command(help="Automatically generate grading for web learning.")
@click.argument("input_csv", type=click.Path(exists=True, dir_okay=False))
@click.argument("late_csv", type=click.Path(exists=True, dir_okay=False))
@click.argument("assignment_name", type=click.STRING)
@click.argument("output_xls", type=click.Path(exists=True, dir_okay=False, writable=True))
@click.option("-w", "--white-raw", type=click.INT, default=20, help="full raw score (white box)")
@click.option("-W", "--white-percent", type=click.IntRange(0, 100), default=20, help="white box precentage")
@click.option("-b", "--black-raw", type=click.INT, default=80, help="full raw score (black box)")
@click.option("-B", "--black-percent", type=click.IntRange(0, 100), default=80, help="black box precentage")
@click.option("-g", "--grader", type=click.STRING, default="", help="name of grader")
def grade(
    input_csv: str, output_xls: str, late_csv: str, assignment_name: str,
    white_raw: int, white_percent: int, black_raw: int, black_percent: int,
    grader: str
):

    csv_df = pd.read_csv(input_csv)
    late_df = pd.read_csv(late_csv)
    xls_df = pd.read_excel(output_xls)

    result = grade_util.grade(csv_df, xls_df, late_df, assignment_name, white_raw, white_percent, black_raw, black_percent, grader)

    result.to_excel(output_xls, index=False, columns=["学生作业id", "学号", "姓名", "提交作业状态", "成绩（录入项）", "评语（录入项）"])


if __name__ == "__main__":
    grade()
