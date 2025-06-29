import math
from angle_mangement import Angle, AngleDirection
from basic_items_definition import *
from testing_data import connectingTraverse_test_data


def the_coming_alpha(current_alpha, beta_here, beta_direction=AngleDirection.left_beta):
    # print(f"正在计算下一条线的角度：从{current_alpha}转过{beta_direction}的{beta_here}")
    turning_angle_value = 180 - beta_here.valueDEC()
    # print(f"这是在计算点之后的这条线的alpha，当前alpha为{current_alpha}")
    if beta_direction == AngleDirection.left_beta:
        next_alpha_value = current_alpha.valueDEC() - turning_angle_value
    else:
        next_alpha_value = current_alpha.valueDEC() + turning_angle_value
    next_alpha_value = round(next_alpha_value, 6)
    next_alpha_value %= 360
    # print(f"得到下一条线为{next_alpha_value}\n")
    return Angle(str(next_alpha_value))


def get_last_alpha(first_alpha, points_data):
    """
    根据已知开始信息，折过这几个转折点这些角之后，得到的线的角度
    :param first_alpha:
    :param points_data:
    :return:
    """
    alpha = None
    print()
    for i in range(len(points_data)):
        point = points_data[i]

        beta = point[PointDataKeys.beta_angle]
        direction = point[PointDataKeys.beta_angle_direction]
        if i == 0:
            alpha = the_coming_alpha(first_alpha, beta, direction)
        else:
            alpha = the_coming_alpha(alpha, beta, direction)

    return alpha


def sin_deg(deg):
    return math.sin(math.radians(deg))


def cos_deg(deg):
    return math.cos(math.radians(deg))


def next_pos(pos, delta: list, v: list, accuracy=3):
    """
    计算下一个点
    :param pos: 上一点坐标
    :param delta: 差值
    :param v: 修正值
    :return:
    """
    previous_x, previous_y = pos
    delta_x, delta_y = delta
    v_x, v_y = v
    print(f"正在修正，此时v为{v_x}、{v_y}, delta为{delta_x}、{delta_y}"
          f"修正的增量Δx ={delta_x + v_x}， Δy ={delta_y + v_y}")
    return [round(previous_x + delta_x + v_x, accuracy), round(previous_y + delta_y + v_y, accuracy)]


def true_delta(measured_delta:list, v: list, accuracy=3):
    delta_x, delta_y = measured_delta
    v_x, v_y = v
    return [round(delta_x + v_x, accuracy), round(delta_y + v_y, accuracy)]


def forward_calculation(start_point_pos: list, alpha: Angle, length):
    """
    # 坐标正算，即用起始点的坐标和相关信息，算目标点的坐标
    # 注意，α是以正北方向为0，而不是数学上的。
    # 另外，这部分都是按照工程坐标系的
        x（正北）
        ↑
        • —→ y（正东）

    :param start_point_pos: 起始点的坐标
    :param alpha: 要正算的这段线段的方位角
    :param length: 要正算的这段线段的长度
    :return: 返回正算的这段线段的终点的坐标
    """

    # 注意，计算时统一用十进制小数来算，毕竟实际中也是用这个来算的，误差都在允许范围内。
    # 而且理论上十进制小数精度更高。

    # print(f"开始坐标正算。当前线段方位角为{alpha.valueDEC()}, 线段长度{length}")

    # print(cos_deg(alpha.valueDEC()))
    print(f"坐标正算，开始点{start_point_pos}")
    delta_x = cos_deg(alpha.valueDEC()) * length

    delta_y = sin_deg(alpha.valueDEC()) * length
    print(f"delta_x:{delta_x}  delta_y:{delta_y}")
    return [start_point_pos[0] + delta_x, start_point_pos[1] + delta_y]


def forward_calculation_get_delta(alpha: Angle, length):
    delta_x = cos_deg(alpha.valueDEC()) * length
    delta_y = sin_deg(alpha.valueDEC()) * length
    return [delta_x, delta_y]


def get_accuracy(point, line):
    # 根据传入的一个点和一条线来确定精度。
    pos = point[PointDataKeys.pos]
    length = line[LineDataKeys.length]
    # 暂停开发。改用别的。


def cal_alphas_roughly(first_alpha, points):
    """
    用于v3。初步计算各个线段的α'。

    :return:
    """
    alphas = []
    for i in range(len(points)):
        point = points[i]

        beta = point[PointDataKeys.beta_angle]
        if type(beta) is not Angle:
            beta = Angle(beta)
        direction = point[PointDataKeys.beta_angle_direction]
        if i == 0:
            alpha = the_coming_alpha(first_alpha, beta, direction)
        else:
            alpha = the_coming_alpha(alphas[-1], beta, direction)
        alphas.append(alpha)

    return alphas


if __name__ == "__main__":
    alpha_AB = Angle("237'59'30'")
    alpha_B1 = the_coming_alpha(alpha_AB, Angle("99'1'0'"), AngleDirection.left_beta)

    alpha_12 = the_coming_alpha(alpha_B1, Angle("167'45'36'"))
    print(f"alpha_B1:{alpha_B1.valueDEC()} alpha_12:{alpha_12.valueDEC()}")
    point_1_pos = forward_calculation([2507.698, 1215.637],
                                      alpha_B1,  # 157.00833\
                                      225.848)
    print(point_1_pos)

    print(forward_calculation(point_1_pos,  # [2299.7909872186856, 1303.8526059909495],
                              alpha_12,  # 144.768333
                              136.026))

    start_alpha = connectingTraverse_test_data[MeasureDataKeys.start_line_angle_alpha]
    points = connectingTraverse_test_data[MeasureDataKeys.points]
    print(f"开始测试角度求一次计算最后alpha：{get_last_alpha(start_alpha, points)}")
