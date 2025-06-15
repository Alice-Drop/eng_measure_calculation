# 导线测量基础库
import copy
import angle_mangement
import testing_data
from angle_mangement import Angle
import calculate
from basic_items_definition import *
from testing_data import connectingTraverse_test_data
from typing import List
import show_data
import os
import drawing


def get_fx_fy(rel_pos, expected_pos):
    rel_x, rel_y = rel_pos
    exp_x, exp_y = expected_pos
    f_x = rel_x - exp_x
    f_y = rel_y - exp_y

    return [f_x, f_y]


def get_fx_fy_v2(exp_delta: List[int], start_pos: List[int], end_pos: List[int]):
    exp_delta_x, exp_delta_y = exp_delta
    x_start, y_start = start_pos
    x_end, y_end = end_pos

    f_x = exp_delta_x - (x_end - x_start)
    f_y = exp_delta_y - (y_end - y_start)

    return [f_x, f_y]


def total_D(data_lines):
    result = 0
    for line in data_lines:
        result += line[LineDataKeys.length]
    return round(result, 5)


def get_v_beta(rel_angle, exp_angle, points):
    f_beta = exp_angle - rel_angle
    v_beta = - (f_beta / len(points))  # 注意公式！这里是负的)
    return v_beta

def get_points_beta_corrected(rel_angle, exp_angle, points):
    """
    利用f_β对点的β进行修正，返回修正后的点数据。高度集成化，已经不对外提供f_beta了
    :param rel_angle:
    :param exp_angle:
    :param points:
    :return:
    """
    f_beta = exp_angle - rel_angle
    v_beta = - (f_beta / len(points))  # 注意公式！这里是负的
    print(f"f_β={f_beta}, v_β = {v_beta}")
    new_points = copy.deepcopy(points)
    for point in new_points:
        print(f"正在修正点{point[PointDataKeys.name]}的β：{point[PointDataKeys.beta_angle]}")
        point[PointDataKeys.beta_angle] += Angle(str(v_beta))
        print(f"修正为{point[PointDataKeys.beta_angle]}")
    # print(f"函数中返回的平差后的数据{new_points}")
    return new_points


def connectionTraverse_calculate(traverse_data: dict):

    print("开始分析......")
    if traverse_data.get(MeasureDataKeys.measureType) != MeasureType.ConnectingTraverse:
        print("警告，数据传入错误。")
    else:

        if len(traverse_data.get(MeasureDataKeys.points)) != len(traverse_data.get(MeasureDataKeys.lines)) + 1:
            raise ValueError("警告，传入的点数量并非比线段数多1，请检查数据缺失问题。")

        # 在该点之前的
        previous_line_alpha = traverse_data.get(MeasureDataKeys.start_line_angle_alpha)
        # 计算出的数据
        exp_data_points = copy.deepcopy(traverse_data.get(MeasureDataKeys.points))
        exp_data_lines = copy.deepcopy(traverse_data.get(MeasureDataKeys.lines))
        calculated_points = []
        for i in range(len(exp_data_points)):
            # 关键：每个点前面的这段线，比如一开始的AB是B前面的，α为已知。

            if i != len(exp_data_points) - 1:
                # 如果是最后一个点就不需要算了，后面就是结尾的已知直线了。这个的目的只是算出各个点的初步计算的坐标
                print(f"\n{i}.开始处理点{exp_data_points[i]}")
                if i == 0:
                    previous_line_alpha = traverse_data.get(MeasureDataKeys.start_line_angle_alpha)
                else:
                    # 注意，由于不会有AB的数据，第一段线的α是从外部来的，所以第一个点不用到线数据，会少一条，所以是i-1
                    previous_line_alpha = exp_data_lines[i - 1][LineDataKeys.alpha]
                print(f"确定当前的点上一条线的alpha为：{previous_line_alpha}")

                point = exp_data_points[i]
                beta = point[PointDataKeys.beta_angle]
                beta_direction = point[PointDataKeys.beta_angle_direction]
                coming_line_alpha = calculate.the_coming_alpha(previous_line_alpha, beta, beta_direction)
                # 把next alpha记录到下一条线
                coming_line = exp_data_lines[i]
                coming_line[LineDataKeys.alpha] = coming_line_alpha

                pos = point[PointDataKeys.pos]
                next_line_length = coming_line[LineDataKeys.length]
                print(f"准备坐标正算，坐标{pos},下个alpha{coming_line_alpha},下段线{coming_line[LineDataKeys.name]}长度为{next_line_length}")
                next_point_pos = calculate.forward_calculation(pos, coming_line_alpha, next_line_length)
                # 把next point写入
                next_point = exp_data_points[i + 1]
                next_point[PointDataKeys.pos] = next_point_pos
                print(f"写入后的next_point是否保持一致，1-4没有坐标？{next_point}")


                print(f"坐标正算结果：下一条线{"".join(coming_line[LineDataKeys.component_points])}的alpha为{coming_line_alpha}")
                print(f"下一个点{next_point[PointDataKeys.name]}坐标为{next_point[PointDataKeys.pos]}")

        print(f"初步计算结果：{exp_data_points}")
        rel_end_point = traverse_data[MeasureDataKeys.points][-1]
        exp_end_point = exp_data_points[-1]
        print(f"预测的C点：{exp_end_point} \n实际的C点：{rel_end_point}")
        f_x, f_y = get_fx_fy(rel_end_point[PointDataKeys.pos], exp_end_point[PointDataKeys.pos])
        print(f"fx {f_x}  f_y {f_y}")

        total_distance = total_D(exp_data_lines)
        print(f"全长{total_distance}")
        for i in range(len(exp_data_lines)):
            line = exp_data_lines[i]


def connectionTraverse_calculate_v2(traverse_data: dict, wanted_accuracy: int):
    # 对附合导线进行分析。需要传入一个精度。
    print("开始分析......")
    if 1 + 1 == 3:  #traverse_data.get(MeasureDataKeys.measureType) != MeasureType.ConnectingTraverse:
        print("警告，数据传入错误。")
    else:

        if len(traverse_data.get(MeasureDataKeys.points)) != len(traverse_data.get(MeasureDataKeys.lines)) + 1:
            raise ValueError("警告，传入的点数量并非比线段数多1，请检查数据缺失问题。")

        # 先对夹角进行平差 这部分已经通过验收，非常准确。
        raw_points = traverse_data[MeasureDataKeys.points]
        beta_correction_points_data = copy.deepcopy(raw_points)
        print(f"初始的点数据，夹角未平差{beta_correction_points_data}")
        first_alpha = traverse_data[MeasureDataKeys.start_line_angle_alpha]
        rel_end_alpha = traverse_data[MeasureDataKeys.end_line_angle_alpha]

        calculated_end_alpha = calculate.get_last_alpha(first_alpha, beta_correction_points_data)
        print(f"验证：first:{first_alpha} \n rel_end:{rel_end_alpha} exp_end{calculated_end_alpha}\n")
        beta_correction_points_data = get_points_beta_corrected(rel_end_alpha, calculated_end_alpha, beta_correction_points_data)
        v_beta = get_v_beta(rel_end_alpha, calculated_end_alpha, beta_correction_points_data)
        v_beta = round(v_beta, 6)

        print(f"平差后的点数据{beta_correction_points_data}")

        # 计算Δx、Δy，得到f_x、f_y，最后平差
        previous_line_alpha = traverse_data.get(MeasureDataKeys.start_line_angle_alpha)
        corrected_points = beta_correction_points_data  # 使用β平差后的点
        raw_lines = traverse_data[MeasureDataKeys.lines]
        corrected_lines = copy.deepcopy(raw_lines)

        total_delta_x = 0
        total_delta_y = 0

        delta_data = []
        print("\n-----开始进行坐标的平差和计算-----")
        for i in range(len(corrected_points)):
            # 关键：每个点前面的这段线，比如一开始的AB是B前面的，α为已知。
            if i != len(corrected_points) - 1:
                # 如果是最后一个点就不需要算了，后面就是结尾的已知直线了。这个的目的只是算出各个点的初步计算的坐标
                print(f"\n{i}.开始处理点{corrected_points[i]}")
                if i == 0:
                    previous_line_alpha = traverse_data.get(MeasureDataKeys.start_line_angle_alpha)
                else:
                    previous_line_alpha = corrected_lines[i - 1][LineDataKeys.alpha]

                # 注意，由于不会有AB的数据，第一段线的α是从外部来的，所以第一个点不用到线数据，会少一条，所以是i-1
                # previous_line_alpha =
                print(f"确定当前的点上一条线的alpha为：{previous_line_alpha}")
                point = corrected_points[i]
                beta = point[PointDataKeys.beta_angle]
                beta_direction = point[PointDataKeys.beta_angle_direction]
                print(f"准备分析，内容为：beta {beta}  beta_direction  {beta_direction}")
                coming_alpha = calculate.the_coming_alpha(previous_line_alpha, beta, beta_direction)

                coming_line = corrected_lines[i]
                coming_line[LineDataKeys.alpha] = coming_alpha  # 把之前算出的下一条线的α记录，为计算下一条线的角度提供依据
                coming_line_length = coming_line[LineDataKeys.length]
                # 用坐标正算算出长度
                delta_x, delta_y = calculate.forward_calculation_get_delta(coming_alpha, coming_line_length)
                delta_x = round(delta_x, wanted_accuracy)
                delta_y = round(delta_y, wanted_accuracy)
                print(f"在该点处的坐标正算结果是，Δ'x ={delta_x}， Δ'y ={delta_y}")
                total_delta_x += delta_x
                total_delta_y += delta_y
                delta_data.append([delta_x, delta_y])
        print(f"完成坐标正算，ΣΔx' = {total_delta_x}, ΣΔy' = {total_delta_y}")
        start_point = corrected_points[0]
        start_pos = start_point[PointDataKeys.pos]
        end_point = corrected_points[-1]
        end_pos = end_point[PointDataKeys.pos]
        f_x, f_y = get_fx_fy_v2([total_delta_x, total_delta_y], start_pos, end_pos)
        f_x = round(f_x, wanted_accuracy)
        f_y = round(f_y, wanted_accuracy)

        print(f"算出的f_x：{f_x}, f_y:{f_y}")

        # 开始对每条线进行平差，算出该点坐标
        print(f"\n开始平差、计算坐标")
        total_distance = total_D(corrected_lines)
        for i in range(len(corrected_points)):
            point = corrected_points[i]
            if i != len(corrected_points) - 1:
                print(f"对第{i}点{point[PointDataKeys.name]}进行分析，计算下一点。")
                pos = point[PointDataKeys.pos]

                coming_line = corrected_lines[i]
                coming_line_length = coming_line[LineDataKeys.length]
                v_x = (coming_line_length / total_distance) * (-f_x)  # 注意！v是与f正负相反的！
                v_y = (coming_line_length / total_distance) * (-f_y)
                print(f"即对{coming_line[LineDataKeys.name]}进行处理")
                next_point_pos = calculate.next_pos(pos, delta_data[i], [v_x, v_y])
                next_point = corrected_points[i + 1]
                next_point[PointDataKeys.pos] = next_point_pos
                coming_line[LineDataKeys.rough_delta_x], coming_line[LineDataKeys.rough_delta_y] = delta_data[i]
                coming_line[LineDataKeys.true_delta_x], coming_line[LineDataKeys.true_delta_y] = (
                    calculate.true_delta(delta_data[i], [v_x, v_y]))
                print(f"下一点{next_point[PointDataKeys.name]}平差后坐标为{next_point_pos}")

        print(f"已完成，正在生成表格......")
        show_data.show_table(show_data.generate_points_table(raw_points, corrected_points, v_beta))
        show_data.show_table(show_data.generate_lines_table(raw_lines, corrected_lines, wanted_accuracy), wanted_accuracy)
        drawing.draw(corrected_points)
        os.system("pause")


def connectionTraverse_calculate_V3(traverse_data: dict, wanted_accuracy: int):
    """
    # v3已通过验证。作为唯一标准。
    :param traverse_data:
    :param wanted_accuracy:
    :return: 返回两个数据表格。
    """
    print("开始分析......")
    if traverse_data.get(MeasureDataKeys.measureType) == MeasureType.ConnectingTraverse:
        print("传入的是附合导线测量数据。")
    elif traverse_data.get(MeasureDataKeys.measureType) == MeasureType.ClosedTraverse:
        print("传入的是闭合导线测量数据。")
    else:
        raise ValueError("警告，传入的不是允许的数据类型，或类型标记丢失。")

    if len(traverse_data.get(MeasureDataKeys.points)) != len(traverse_data.get(MeasureDataKeys.lines)) + 1:
        raise ValueError("警告，传入的点数量并非比线段数多1，请检查数据缺失问题。")

    # 先对夹角进行平差 这部分已经通过验收，非常准确。
    raw_points = traverse_data[MeasureDataKeys.points]
    corrected_points = copy.deepcopy(raw_points)
    print(f"初始的点数据，先据此正算，算出结尾线段的α，以此平差。")
    first_alpha = traverse_data[MeasureDataKeys.start_line_angle_alpha]
    rel_end_alpha = traverse_data[MeasureDataKeys.end_line_angle_alpha]

    roughly_alphas = calculate.cal_alphas_roughly(first_alpha, raw_points)
    print(f"计算出各个粗略方位角α'：{roughly_alphas}")

    f_beta = roughly_alphas[-1] - rel_end_alpha
    if f_beta.valueDEC() > 350:  # 把0 == 360的做进去
        f_beta -= Angle("360")

    true_alphas = []


    print(f"当前是闭合导线。开始平差")
    v_beta = 0

    for i in range(len(raw_points)):
        point = raw_points[i]
        if traverse_data[MeasureDataKeys.measureType] == MeasureType.ClosedTraverse:
            v_beta = -(f_beta / len(raw_points))  # 注意，这里的n可能不一定
        else:
            if point[PointDataKeys.beta_angle_direction] == angle_mangement.AngleDirection.right_beta:
                v_beta = f_beta / len(raw_points)
            else:
                v_beta = -(f_beta / len(raw_points))
        v_beta = round(v_beta, 6)

        beta_here = raw_points[i][PointDataKeys.beta_angle]
        direction = raw_points[i][PointDataKeys.beta_angle_direction]
        if i == 0:
            alpha = calculate.the_coming_alpha(first_alpha, beta_here, direction)
        else:
            alpha = calculate.the_coming_alpha(true_alphas[i-1], beta_here, direction)
        alpha += Angle(str(v_beta))
        corrected_beta_here = beta_here + Angle(str(v_beta))
        true_alphas.append(alpha)
        # print("信息：")
        # print(traverse_data[MeasureDataKeys.lines])
        if i != len(raw_points) - 1:  # 由于最后一段是不存在的、校准用的线，实际不存在，所以不能记录，或者说已经记录着end_line_alpha里了
            traverse_data[MeasureDataKeys.lines][i][LineDataKeys.alpha] = alpha  # 把平差后的准确结果记录
        print(f"此处{point[PointDataKeys.name]}点下一段线的α修正为{alpha} (此处beta{beta_here}修正为{corrected_beta_here})")

    print("角度平差完毕\n")

    delta_data_rough = []
    total_delta_rough = [0, 0]
    raw_lines = traverse_data[MeasureDataKeys.lines]
    for line in raw_lines:
        length = line[LineDataKeys.length]
        name = line[LineDataKeys.name]
        alpha: Angle = line[LineDataKeys.alpha]
        delta_x_rough = length * calculate.cos_deg(alpha.valueDEC())
        delta_y_rough = length * calculate.sin_deg(alpha.valueDEC())
        delta_x_rough = round(delta_x_rough, wanted_accuracy)
        delta_y_rough = round(delta_y_rough, wanted_accuracy)

        delta_data_rough.append([delta_x_rough, delta_y_rough])
        line[LineDataKeys.rough_delta_x] = delta_x_rough
        line[LineDataKeys.rough_delta_y] = delta_y_rough
        total_delta_rough[0] += delta_x_rough
        total_delta_rough[1] += delta_y_rough
        print(f"对于线段{name}, alpha={alpha}, Δx' = {delta_x_rough}, Δy'= {delta_y_rough}")
    print(f"总的结果ΣΔx'、ΣΔy'为{total_delta_rough}\n")

    f_x = f_y = 0
    first_point_pos = raw_points[0][PointDataKeys.pos]
    last_point_pos = raw_points[-1][PointDataKeys.pos]
    f_x = total_delta_rough[0] - (last_point_pos[0] - first_point_pos[0])
    f_y = total_delta_rough[1] - (last_point_pos[1] - first_point_pos[1])
    print(f"计算出f_x {f_x} f_y {f_y}\n")

    total_length = total_D(raw_lines)
    print(f"总长度为{total_length}")
    for i in range(len(raw_lines)):
        line = raw_lines[i]
        length = line[LineDataKeys.length]
        name = line[LineDataKeys.name]
        v_x_here = - (length / total_length) * f_x
        v_y_here = - (length / total_length) * f_y
        delta_x_true = line[LineDataKeys.rough_delta_x] + v_x_here
        delta_y_true = line[LineDataKeys.rough_delta_y] + v_y_here
        delta_x_true = round(delta_x_true, wanted_accuracy)
        delta_y_true = round(delta_y_true, wanted_accuracy)

        line[LineDataKeys.true_delta_x] = delta_x_true
        line[LineDataKeys.true_delta_y] = delta_y_true
        print(f"修正后的Δx_{name} = {delta_x_true} Δy_{name} = {delta_y_true}")
        start_point_of_this_line = raw_points[i]
        x_here = start_point_of_this_line[PointDataKeys.pos][0] + delta_x_true
        y_here = start_point_of_this_line[PointDataKeys.pos][1] + delta_y_true
        x_here = round(x_here, wanted_accuracy)
        y_here = round(y_here, wanted_accuracy)
        # 写入数据
        if i != len(raw_lines) - 1:  # 不是最后一条线段才写入，最后一条线段的话，结束点是已知的
            end_point_of_this_line = raw_points[i + 1]
            end_point_of_this_line[PointDataKeys.pos] = [x_here, y_here]

            print(f"此处的点{end_point_of_this_line[PointDataKeys.name]}的坐标为：{[x_here, y_here]}")

    print("处理完成！")
    # drawing.draw(raw_points)

    points_report = show_data.generate_points_table_v3(raw_points, v_beta, wanted_accuracy)
    lines_report = show_data.generate_lines_table_v3(raw_lines, wanted_accuracy)
    show_data.show_table(points_report)
    show_data.show_table(lines_report)
    print("分析结果已经保存为“点分析.csv”和“线段分析.csv”")

    return [points_report, lines_report]


if __name__ == "__main__":
    # connectionTraverse_calculate_v2(connectingTraverse_test_data, 3)
    # connectionTraverse_calculate_V3(testing_data.closedTraverse_test_data, 3)
    # connectionTraverse_calculate_V3(testing_data.closedTraverse_experiment_data, 3)
    connectionTraverse_calculate_V3(testing_data.connectingTraverse_test_data, 3)
    #connectionTraverse_calculate_v2(testing_data.connectingTraverse_test_data, 3)
