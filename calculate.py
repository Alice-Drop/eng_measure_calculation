import math
from angle_mangement import Angle, AngleDirection
from basic_items_definition import PointDataKeys, PointDataItem


def next_alpha(current_alpha, beta_here, beta_direction=AngleDirection.left_beta):
    turning_angle_value = 180 - beta_here.valueDEC()
    if beta_direction == AngleDirection.left_beta:
        next_alpha_value = current_alpha.valueDEC() - turning_angle_value
    else:
        next_alpha_value = current_alpha.valueDEC() + turning_angle_value

    return Angle(str(next_alpha_value))


def sin_deg(deg):
    return math.sin(math.radians(deg))


def cos_deg(deg):
    return math.cos(math.radians(deg))


def forward_calculation(start_point: list, alpha: Angle, length):
    """
    # 坐标正算，即用起始点的坐标和相关信息，算目标点的坐标
    # 注意，α是以正北方向为0，而不是数学上的。
    # 另外，这部分都是按照工程坐标系的
        x（正北）
        ↑
        • —→ y（正东）

    :param start_point:
    :param alpha:
    :param length:
    :return:
    """

    # 注意，计算时统一用十进制小数来算，毕竟实际中也是用这个来算的，误差都在允许范围内。
    # 而且理论上十进制小数精度更高。

    # print(f"开始坐标正算。当前线段方位角为{alpha.valueDEC()}, 线段长度{length}")

    # print(cos_deg(alpha.valueDEC()))
    print(start_point)
    delta_x = cos_deg(alpha.valueDEC()) * length

    delta_y = sin_deg(alpha.valueDEC()) * length
    # print(f"delta_x:{delta_x}  delta_y:{delta_y}")
    return [start_point[PointDataKeys.pos][0] + delta_x, start_point[PointDataKeys.pos][1] + delta_y]


if __name__ == "__main__":
    alpha_AB = Angle("237'59'30'")
    alpha_B1 = next_alpha(alpha_AB, Angle("99'1'0'"), AngleDirection.left_beta)

    alpha_12 = next_alpha(alpha_B1, Angle("167'45'36'"))
    print(alpha_B1.valueDEC())
    print(forward_calculation(PointDataItem([2507.698, 1215.637], "test 0", Angle("99'01'00'")),
                              alpha_B1,
                              225.848))

    print(forward_calculation(PointDataItem([2299.7909872186856, 1303.8526059909495], "test 1", Angle("167'45'36'")),
                              alpha_12,
                              136.026))
