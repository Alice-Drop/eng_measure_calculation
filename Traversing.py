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

        if len(traverse_data.get(MeasureDataKeys.points)) + 1 != len(traverse_data.get(MeasureDataKeys.line)):
            raise ValueError("警告，传入的点数量并非比线段数多1，请检查数据缺失问题。")

        # 在该点之前的
        previous_line_alpha = traverse_data.get(MeasureDataKeys.start_line_angle_alpha)
        data_points = traverse_data.get(MeasureDataKeys.points)
        data_lines = traverse_data.get(MeasureDataKeys.line)
        for i in range(len(data_points)):
            # 关键：每个点前面的这段线，比如一开始的AB是B前面的，α为已知。

            if i != len(data_points) - 1:
                # 如果是最后一个点就不需要算了，后面就是结尾的已知直线了。这个的目的只是算出各个点的初步计算的坐标

                point = data_points[i]
                point_pos = point[PointDataKeys.pos]
                print(f"正在处理点{point[PointDataKeys.name]}：{point_pos}")

                # 该点处的beta不重要，只是用来计算下一段线的alph，然后写入到data_lines里面
                beta_here = point.get(PointDataKeys.beta_angle)
                beta_direction = point.get(PointDataKeys.beta_angle_direction)

                next_line_alpha = calculate.next_alpha(previous_line_alpha, beta_here, beta_direction)
                next_line_data = data_lines[i]

                next_point = calculate.forward_calculation(point, previous_line_alpha,
                                                           next_line_data.get(LineDataKeys.length))
                ttp.goto(point[PointDataKeys.pos])
                tt.setheading(next_line_alpha.valueMath())
                ttp.fd(next_line_data.get(LineDataKeys.length))

                data_points[i+1][PointDataKeys.pos] = next_point

        print(f"初步计算结果：{traverse_data}")

    tt.done()


connectingTraverse_test_data = {
    MeasureDataKeys.measureType: MeasureType.ConnectingTraverse,  # 附合导线
    MeasureDataKeys.start_line_angle_alpha: Angle("237'59'30'"),  # 起始线段AB的角
    MeasureDataKeys.points: [
        PointDataItem([2570.689, 1215.637], "B", Angle("99'1'0'"),
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
        LineDataItem(None, ["A", "B"], Angle("237'59'30'")),
        LineDataItem(225.848, ["B", "1"]),
        LineDataItem(139.026, ["1", "2"]),
        LineDataItem(172.572, ["2", "3"]),
        LineDataItem(100.067, ["3", "4"]),
        LineDataItem(102.483, ["4", "C"]),
        LineDataItem(None, ["C", "D"], Angle("46'45'24'"))
    ],
    MeasureDataKeys.end_line_angle_alpha: Angle("46'45'24'")

}


if __name__ == "__main__":
    connectionTraverse_calculate(connectingTraverse_test_data)

