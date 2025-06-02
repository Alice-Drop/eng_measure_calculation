from basic_items_definition import (PointDataKeys, PointDataItem, LineDataKeys, LineDataItem,
                                    MeasureDataKeys, MeasureType)
import angle_mangement
from angle_mangement import Angle

closedTraverse_test_data = {
    MeasureDataKeys.measureType: MeasureType.ClosedTraverse,  # 闭合导线
    MeasureDataKeys.start_line_angle_alpha: Angle("180"),  # 起始线段AB的角
    MeasureDataKeys.points: [
        PointDataItem([200, 500], "1", Angle("38'15'0'"),
                      angle_mangement.AngleDirection.left_beta),
        PointDataItem([], "2", Angle("102'48'09'"),
                      angle_mangement.AngleDirection.right_beta),
        PointDataItem([], "3", Angle("78'51'15'"),
                      angle_mangement.AngleDirection.right_beta),
        PointDataItem([], "4", Angle("84'23'27'"),
                      angle_mangement.AngleDirection.right_beta),
        PointDataItem([200, 500], "1", Angle("132'12'45'"),  # Angle("93'57'45'"),
                      angle_mangement.AngleDirection.right_beta),
    ],
    MeasureDataKeys.lines: [
        LineDataItem(112.01, ["1", "2"]),
        LineDataItem(87.58, ["2", "3"]),
        LineDataItem(137.71, ["3", "4"]),
        LineDataItem(89.50, ["4", "1"]),
    ],
    MeasureDataKeys.end_line_angle_alpha: Angle("0")
}


closedTraverse_experiment_data = {
    MeasureDataKeys.measureType: MeasureType.ClosedTraverse,  # 闭合导线
    MeasureDataKeys.start_line_angle_alpha: Angle("180"),  # 起始线段AB的角
    MeasureDataKeys.points: [
        PointDataItem([200, 500], "1", Angle("38'15'0'"),
                      angle_mangement.AngleDirection.left_beta),
        PointDataItem([], "2", Angle("85'3'12'"),
                      angle_mangement.AngleDirection.right_beta),
        PointDataItem([], "3", Angle("157'12'47'"),
                      angle_mangement.AngleDirection.right_beta),
        PointDataItem([], "4", Angle("41'30'29'"),
                      angle_mangement.AngleDirection.right_beta),
        PointDataItem([200, 500], "1", Angle("114'33'41'"),  # Angle("93'57'45'"),
                      angle_mangement.AngleDirection.right_beta),
    ],
    MeasureDataKeys.lines: [
        LineDataItem(33.157, ["1", "2"]),
        LineDataItem(23.741, ["2", "3"]),
        LineDataItem(37.185, ["3", "4"]),
        LineDataItem(58.145, ["4", "1"]),
    ],
    MeasureDataKeys.end_line_angle_alpha: Angle("0")
}

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
    MeasureDataKeys.lines: [
        LineDataItem(225.848, ["B", "1"]),
        LineDataItem(139.026, ["1", "2"]),
        LineDataItem(172.572, ["2", "3"]),
        LineDataItem(100.067, ["3", "4"]),
        LineDataItem(102.483, ["4", "C"]),
    ],
    MeasureDataKeys.end_line_angle_alpha: Angle("46'45'24'")

}
