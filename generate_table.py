# import aliceCSV
from basic_items_definition import *

POINT_TABLE_HEAD = ["点号", "角度观测值（夹角β）", "改正数", "改正后角值", "x坐标", "y坐标"]


def generate_points_table(raw_points, corrected_points, v_beta):
    table = [POINT_TABLE_HEAD]
    if len(raw_points) != len(corrected_points):
        raise ValueError("警告，在分析数据时发现严重内部错误，可能出现点数据对齐错误，运行终止。")
    for i in range(len(raw_points)):
        raw_point = raw_points[i]
        corrected_point = corrected_points[i]
        table.append([
            corrected_point[PointDataKeys.name],
            raw_point[PointDataKeys.beta_angle],
            v_beta,
            corrected_point[PointDataKeys.beta_angle],
            corrected_point[PointDataKeys.pos][0],
            corrected_point[PointDataKeys.pos][1]
        ])

    return table


def show_table(table):
    for row in table:
        string = ""
        for col in row:
            string += str(col) + "\t"
        print(string)
