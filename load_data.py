import json

from angle_mangement import Angle
from basic_items_definition import MeasureDataKeys, PointDataKeys


def load_closedTraverse_test_data():
    with open("./data/closedTraverse_test_data.json", 'r') as f:
        data = json.load(f)
        return data

def load_user_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
        recovery_angle_obj(data)
        return data

def recovery_angle_obj(data):
    # 把用json读进来的数据里面被按平为字符串的Angle复原
    data[MeasureDataKeys.start_line_angle_alpha] = Angle(data[MeasureDataKeys.start_line_angle_alpha])
    for point in data[MeasureDataKeys.points]:
        point[PointDataKeys.beta_angle] = Angle(point[PointDataKeys.beta_angle])

    data[MeasureDataKeys.end_line_angle_alpha] = Angle(data[MeasureDataKeys.end_line_angle_alpha])