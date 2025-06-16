import os

from basic_items_definition import *
from gui_tk import TableViewer

POINT_TABLE_HEAD = ["点号", "角度观测值（夹角β）", "改正数", "改正后角值", "x坐标", "y坐标"]

def log(content=""):
    if_log = False
    if if_log:
        print(content)


def strong_is_float(string):
    if (type(string) is str) and ("." in string):
        accepted_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        for char in string:
            if char not in accepted_chars:
                return False
        return True
    else:
        return False


def safe_start_data_file(path):
    try:
        os.system(f"start {path}")
    except PermissionError:
        log(f"警告，由于未关闭上次生成的文件，程序无法自动打开生成的表格“{path}”，新文件已生成，请关闭excel后自行打开新文件")

def generate_points_table(raw_points, corrected_points, v_beta):
    """
    输出一个csv格式的分析报告。
    :param raw_points: 各个点
    :param corrected_points:
    :param v_beta:
    :return:
    """
    output_path = "./点分析.csv"
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

    return table


def generate_points_table_v3(points, v_beta, accuracy=3):
    """
    输出一个csv格式的分析报告。
    :param points: 各个点
    :param corrected_points:
    :param v_beta:
    :return:
    """
    output_path = "./点分析.csv"
    table = [POINT_TABLE_HEAD]
    for i in range(len(points)):
        point = points[i]
        v_beta_angle = Angle(str(v_beta))
        table.append([
            point[PointDataKeys.name],
            point[PointDataKeys.beta_angle],
            v_beta_angle,
            point[PointDataKeys.beta_angle],
            f"{point[PointDataKeys.pos][0]:.{accuracy}f}",
            f"{point[PointDataKeys.pos][1]:.{accuracy}f}"
        ])

    return table


LINE_TABLE_HEAD = ["线段名称", "坐标方位角α", "平距（线段长度）", "坐标增量Δ'x（未改正）", "坐标增量Δ'y（未改正）",
                   "改正后的坐标增量Δx", "改正后的坐标增量Δy"]


def generate_lines_table(raw_lines, corrected_lines, accuracy=3):
    output_path = "线段分析.csv"
    table = [LINE_TABLE_HEAD]
    for i in range(len(raw_lines)):
        raw_line = raw_lines[i]
        corrected_line = corrected_lines[i]
        table.append([
            raw_line[LineDataKeys.name],
            corrected_line[LineDataKeys.alpha],
            f"{corrected_line[LineDataKeys.length]:.{accuracy}f}",  # 平距（线段长度）
            f"{corrected_line[LineDataKeys.rough_delta_x]:.{accuracy}f}",
            f"{corrected_line[LineDataKeys.rough_delta_y]:.{accuracy}f}",
            f"{corrected_line[LineDataKeys.true_delta_x]:.{accuracy}f}",
            f"{corrected_line[LineDataKeys.true_delta_y]:.{accuracy}f}"
        ])

    return table

def generate_lines_table_v3(lines, accuracy=3):
    # 新版本，为v3设计，线的数据都是由line来的
    output_path = "线段分析.csv"
    table = [LINE_TABLE_HEAD]
    for i in range(len(lines)):
        line = lines[i]
        # log(f"正在读取line:{line}")
        table.append([
            line[LineDataKeys.name],
            line[LineDataKeys.alpha],
            f"{line[LineDataKeys.length]:.{accuracy}f}",  # 平距（线段长度）
            f"{line[LineDataKeys.rough_delta_x]:.{accuracy}f}",
            f"{line[LineDataKeys.rough_delta_y]:.{accuracy}f}",
            f"{line[LineDataKeys.true_delta_x]:.{accuracy}f}",
            f"{line[LineDataKeys.true_delta_y]:.{accuracy}f}"
        ])

    return table

def show_table(table, accuracy=3):
    log()
    for row in table:
        string = ""
        for col in row:
            if strong_is_float(col):
                string += f"{float(col):.{accuracy}f}\t\t\t\t"
                log(f"{col}通过Float")
            else:
                string += str(col) + "\t\t"
        log(string)
    if "点" in table[0][0]:
        title = "各点数据"
    else:
        title = "各线段数据"
    table_window = TableViewer(table, title)
    return table_window

