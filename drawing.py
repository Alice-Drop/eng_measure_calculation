import turtle as tt
import turtlePlus as ttp
from basic_items_definition import *
from typing import List


def eng_angle_to_math_angle(eng_angle):
    return (90 - eng_angle) % 360


def eng_to_math_pos(pos):
    """
    工程坐标
    x
    ↑
     -→ y

    数学坐标
    y
    ↑
     -→ x

     y = eng_x, x = eng_x
    :param pos:
    :return:
    """
    return [pos[1], pos[0]]


def get_points_pos(points: list):
    # 从列表里装着的PointsItem里提取出各个点的坐标。顺便把工程角转换也包括进去
    result = []
    for point in points:
        result.append(eng_to_math_pos(point[PointDataKeys.pos]))
    return result


def draw(corrected_point_data):
    dot_diameter = 10

    points_pos = get_points_pos(corrected_point_data)
    ttp.ensure_appearance(points_pos, ttp.OffsetMode.center)
    ttp.FONT_SCALING = True

    ttp.SCALE = 1
    print(f"当前scale: {ttp.SCALE}")

    ttp.write("start")
    count = 0
    for point in corrected_point_data:
        print(f"在{point[PointDataKeys.name]}点{point[PointDataKeys.pos]}，offset为{ttp.OFFSET}")
        math_pos = eng_to_math_pos(point[PointDataKeys.pos])
        if count == 0:
            ttp.goto(math_pos, line_mode=ttp.LineModes.none,
                     write_name=point[PointDataKeys.name], name_height=16,
                     name_color=ttp.Colors.blue, name_align=ttp.Align.CENTER)
        else:
            ttp.goto(math_pos,
                     write_name=point[PointDataKeys.name], name_height=16,
                     name_color=ttp.Colors.blue, name_align=ttp.Align.CENTER)
        count += 1

    tt.done()


if __name__ == "__main__":
    # draw()
    pass
