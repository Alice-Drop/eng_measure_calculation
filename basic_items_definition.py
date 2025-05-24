import angle_mangement
from angle_mangement import Angle

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
    alpha = "LineDataKeys.alpha"
    name = "LineDataKeys.name"
    true_delta_x = "LineDataKeys.true_delta_x"  # 修正后的delta
    true_delta_y = "LineDataKeys.true_delta_y"
    init_delta_x = "LineDataKeys.init_delta_x"  # 未用v修正的、刚通过坐标正算算出来的delta，
    init_delta_y = "LineDataKeys.init_delta_y"



def LineDataItem(length, component_points: list, alpha=None):
    # 注意，这些线段都是只有在
    return {
        LineDataKeys.length: length,
        LineDataKeys.component_points: component_points,
        LineDataKeys.alpha: alpha,
        LineDataKeys.name: "".join(component_points)
    }


class MeasureType:
    ClosedTraverse = "ClosedTraverse"  # 闭合导线
    ConnectingTraverse = "ConnectingTraverse"  # 附合导线


class MeasureDataKeys:
    measureType = "type"
    start_line_angle_alpha = "start_line_angle_alpha"  # 开始直线的方位角α_AB
    points = "points"
    lines = "lines"
    end_line_angle_alpha = "end_line_angle_alpha"