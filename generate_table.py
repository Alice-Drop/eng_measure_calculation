import os

import aliceCSV
from basic_items_definition import *

POINT_TABLE_HEAD = ["点号", "角度观测值（夹角β）", "改正数", "改正后角值", "x坐标", "y坐标"]
LINE_TABLE_HEAD = ["线段名称", "坐标方位角α", "平距（线段长度）", "坐标增量x", "坐标增量y"]

def strong_is_float(string):
    if (type(string) is str) and ("." in string):
        accepted_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        for char in string:
            if char not in accepted_chars:
                return False
        return True
    else:
        return False


def generate_points_table(raw_points, corrected_points, v_beta):
    table = [POINT_TABLE_HEAD]
    if len(raw_points) != len(corrected_points):
        raise ValueError("警告，在分析数据时发现严重内部错误，可能出现点数据对齐错误，运行终止。")
    for i in range(len(raw_points)):
        raw_point = raw_points[i]
        corrected_point = corrected_points[i]
        v_beta_angle = Angle(str(v_beta))
        table.append([
            corrected_point[PointDataKeys.name],
            raw_point[PointDataKeys.beta_angle],
            v_beta_angle,
            corrected_point[PointDataKeys.beta_angle],
            corrected_point[PointDataKeys.pos][0],
            corrected_point[PointDataKeys.pos][1]
        ])
    aliceCSV.writeCSV(table, output_path="点分析.csv", sheet_encoding="UTF-8-sig")
    os.system("start ./点分析.csv")

    return table


def generate_lines_table(raw_lines, corrected_lines, v):
    table = [LINE_TABLE_HEAD]
    for i in range(len(raw_lines)):
        raw_line = raw_lines[i]
        corrected_line = corrected_lines[i]
        table.append([
            raw_line[LineDataKeys.name],
            corrected_line[LineDataKeys.alpha],
            corrected_line[LineDataKeys.length],

        ])


def show_table(table):
    print()
    for row in table:
        string = ""
        for col in row:
            if strong_is_float(col):
                string += f"{float(col):.3}\t"
                print(f"{col}通过Float")
            else:
                string += str(col) + "\t"
        print(string)

