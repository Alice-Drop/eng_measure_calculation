# 导线测量基础库

import angle_mangement
from angle_mangement import Angle
import calculate
import turtle as tt
import turtlePlus as ttp
from basic_items_definition import PointDataItem, PointDataKeys, LineDataKeys, LineDataItem

class MeasureType:
    ClosedTraverse = "ClosedTraverse"  # 闭合导线
    ConnectingTraverse = "ConnectingTraverse"  # 附合导线


class MeasureDataKeys:
    measureType = "type"
    start_line_angle_alpha = "start_line_angle_alpha"  # 开始直线的方位角α_AB
    points = "points"
    line = "line"
    end_line_angle_alpha = "end_line_angle_alpha"




def total_f():
    pass

def k():
    # k为
    pass


def connectionTraverse_calculate(traverse_data: dict):
    dot_diameter = 10
    ttp.set_scale(0.3)

    print("开始分析......")
    if traverse_data.get(MeasureDataKeys.measureType) != MeasureType.ConnectingTraverse:
        print("警告，数据传入错误。")
    else:

        if len(traverse_data.get(MeasureDataKeys.points)) != len(traverse_data.get(MeasureDataKeys.line)) + 1:
            raise ValueError("警告，传入的点数量并非比线段数多1，请检查数据缺失问题。")

        # 在该点之前的
        previous_line_alpha = traverse_data.get(MeasureDataKeys.start_line_angle_alpha)
        data_points = traverse_data.get(MeasureDataKeys.points)
        data_lines = traverse_data.get(MeasureDataKeys.line)
        for i in range(len(data_points)):
            # 关键：每个点前面的这段线，比如一开始的AB是B前面的，α为已知。

            if i != len(data_points) - 1:
                # 如果是最后一个点就不需要算了，后面就是结尾的已知直线了。这个的目的只是算出各个点的初步计算的坐标
                print(f"\n{i}.开始处理点{data_points[i]}")
                if i == 0:
                    previous_line_alpha = traverse_data.get(MeasureDataKeys.start_line_angle_alpha)
                else:
                    # 注意，由于不会有AB的数据，第一段线的α是从外部来的，所以第一个点不用到线数据，会少一条，所以是i-1
                    previous_line_alpha = data_lines[i - 1][LineDataKeys.alpha]
                print(f"确定当前的点上一条线的alpha为：{previous_line_alpha}")

                point = data_points[i]
                beta = point[PointDataKeys.beta_angle]
                beta_direction = point[PointDataKeys.beta_angle_direction]
                coming_line_alpha = calculate.the_coming_alpha(previous_line_alpha, beta, beta_direction)
                # 把next alpha记录到下一条线
                coming_line = data_lines[i]
                coming_line[LineDataKeys.alpha] = coming_line_alpha

                pos = point[PointDataKeys.pos]
                next_line_length = coming_line[LineDataKeys.length]
                print(f"准备坐标正算，坐标{pos},下个alpha{coming_line_alpha},下段线{coming_line[LineDataKeys.name]}长度为{next_line_length}")
                next_point_pos = calculate.forward_calculation(pos, coming_line_alpha, next_line_length)
                # 把next point写入
                next_point = data_points[i + 1]
                next_point[PointDataKeys.pos] = next_point_pos

                print(f"坐标正算结果：下一条线{"".join(coming_line[LineDataKeys.component_points])}的alpha为{coming_line_alpha}")
                print(f"下一个点{next_point[PointDataKeys.name]}坐标为{next_point[PointDataKeys.pos]}")

        print(f"初步计算结果：{traverse_data}")

    tt.done()


connectingTraverse_test_data = {
    MeasureDataKeys.measureType: MeasureType.ConnectingTraverse,  # 附合导线
    MeasureDataKeys.start_line_angle_alpha: Angle("237'59'30'"),  # 起始线段AB的角
    MeasureDataKeys.points: [
        PointDataItem([2507.698, 1215.637], "B", Angle("99'1'0'"),
                      angle_mangement.AngleDirection.left_beta),
        PointDataItem([], "1", Angle("167'45'36'"),
                      angle_mangement.AngleDirection.left_beta),
        PointDataItem([], "2", Angle("123'11'24'"),
                      angle_mangement.AngleDirection.left_beta),
        PointDataItem([], "3", Angle("189'20'36'"),
                      angle_mangement.AngleDirection.left_beta),
        PointDataItem([], "4", Angle("179'59'18'"),
                      angle_mangement.AngleDirection.left_beta),
        PointDataItem([2166.646, 1757.344], "C", Angle("129'27'24'"),
                      angle_mangement.AngleDirection.left_beta),
    ],
    MeasureDataKeys.line: [
        LineDataItem(225.848, ["B", "1"]),
        LineDataItem(139.026, ["1", "2"]),
        LineDataItem(172.572, ["2", "3"]),
        LineDataItem(100.067, ["3", "4"]),
        LineDataItem(102.483, ["4", "C"]),
    ],
    MeasureDataKeys.end_line_angle_alpha: Angle("46'45'24'")

}


if __name__ == "__main__":
    connectionTraverse_calculate(connectingTraverse_test_data)

