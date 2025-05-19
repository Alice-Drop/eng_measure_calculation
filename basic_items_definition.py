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


def LineDataItem(length, component_points: list, alpha=None):
    # 注意，这些线段都是只有在
    return {
        LineDataKeys.length: length,
        LineDataKeys.component_points: component_points,
        LineDataKeys.alpha: alpha
    }
