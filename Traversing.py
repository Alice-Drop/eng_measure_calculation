# 导线测量基础库

import angle_mangement
from angle_mangement import Angle
import turtle as tt
import turtlePlus as ttp

class MeasureType:
    ClosedTraverse = "ClosedTraverse"  # 闭合导线
    ConnectingTraverse = "ConnectingTraverse"  # 附合导线


class MeasureDataKeys:
    measureType = "type"
    start_line_angle_alpha = "start_line_angle_alpha"  # 开始直线的方位角α_AB
    points = "points"
    lengths = "lengths"
    end_line_angle_alpha = "end_line_angle_alpha"


class PointDataKeys:
    pos = "pos"
    name = "name"
    beta_angle = "beta_angle"
    beta_angle_direction = "beta_angle_direction"


def PointDataItem(pos: list, name, beta_angle: Angle,
                  direction=angle_mangement.AngleDirection.left_beta):
    result = {
        PointDataKeys.pos: pos,
        PointDataKeys.name: name,
        PointDataKeys.beta_angle: beta_angle,
        PointDataKeys.beta_angle_direction: direction
    }
    return result

class LineDataKeys:
    length = "LineDataKeys.length"
    component_points = "LineDataKeys.component_points"


def LineDataItem(length, component_points: list):
    return {
        LineDataKeys.length: length,
        LineDataKeys.component_points: component_points
    }


def total_f():
    pass

def k():
    # k为
    pass


def connectionTraverse_calculate(traverse_data: dict):
    dot_diameter = 10
    print("开始分析......")
    if traverse_data.get(MeasureDataKeys.measureType) != MeasureType.ConnectingTraverse:
        print("警告，数据传入错误。")
    else:
        ttp.goto([0, 0], line_mode=ttp.LineModes.none, dot_diameter=dot_diameter)
        tt.setheading(traverse_data.get(MeasureDataKeys.start_line_angle_alpha).valueMath())

        current_line_alpha =
        for :
            # 根据该点处的beta计算下一段线的
            current_line_alpha +=

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
    MeasureDataKeys.lengths: [
        LineDataItem(225.848, ["B", "1"]),
        LineDataItem(139.026, ["1", "2"]),
        LineDataItem(172.572, ["2", "3"]),
        LineDataItem(100.067, ["3", "4"]),
        LineDataItem(102.483, ["4", "C"])
    ],
    MeasureDataKeys.end_line_angle_alpha: Angle("46'45'24'")

}


if __name__ == "__main__":
    connectionTraverse_calculate(connectingTraverse_test_data)