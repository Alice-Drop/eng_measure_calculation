import turtle as tt

import testing_data


class LineModes:
    solid = "solid"
    dotted = "dotted"
    none = "none"

class Colors:
    black = "black"
    white = "white"
    red = "red"
    blue = "blue"


class Align:
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"

class VerticalAlign:
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"

class DEFAULT:
    LINE_WIDTH = 5
    DOTTED_LINE_LENGTH = 10  # 虚线的每个实线部分多长
    DOTTED_GAP = 10  # 虚线的实线间隔多大
    DOT_DIAMETER = 10

    FONT_HEIGHT = 8
    FONT_ALIGN = Align.LEFT
    FONT_COLOR = Colors.black
    FONT_FAMILY = "Arial"
    FONT_WEIGHT = "normal"
    FONT_VERTICAL_ALIGN = VerticalAlign.BOTTOM

class OffsetMode:
    none = "OffsetMode.none"
    at_start = "OffsetMode.at_start"
    center = "OffsetMode.center"


SCALE = 1.0
FONT_SCALING = False
OFFSET = [0, 0]


def set_scale(scale_value):
    global SCALE
    if scale_value <= 0:
        raise ValueError("缩放比例必须大于0")
    SCALE = scale_value


def get_scale():
    return SCALE


def distance(point_1: list, point_2: list):
    # 计算两点间距离
    x_1, y_1 = point_1
    x_2, y_2 = point_2

    x_1 *= SCALE
    x_2 *= SCALE
    y_1 *= SCALE
    y_2 *= SCALE

    x_1 += OFFSET[0]
    x_2 += OFFSET[0]
    y_1 += OFFSET[1]
    y_2+= OFFSET[1]

    return ((x_2-x_1)**2 + (y_2-y_1)**2)**(1/2)



def fd(length, line_width=DEFAULT.LINE_WIDTH, line_color=Colors.black, line_mode=LineModes.solid,
       write_name="", name_align=Align.LEFT, name_vertical_align=VerticalAlign.TOP,
       if_dot_at_end=True, dot_color=Colors.black, dot_diameter=DEFAULT.DOT_DIAMETER,
       dotted_line_length=DEFAULT.DOTTED_LINE_LENGTH, dotted_gap=DEFAULT.DOTTED_GAP):
    # 前进

    length *= SCALE

    line_width *= SCALE
    dot_diameter *= SCALE
    dotted_line_length *= SCALE
    dotted_gap *= SCALE

    tt.pencolor(line_color)
    tt.pensize(line_width)

    if line_mode == LineModes.solid:
        # 绘制实线
        tt.pendown()
        tt.fd(length)
    elif line_mode == LineModes.dotted:
        # 绘制虚线

        while length > 0:
            if length >= dotted_line_length:
                tt.pendown()
                tt.fd(dotted_line_length)
                length -= dotted_line_length
            else:
                tt.pendown()
                tt.fd(length)
                length = 0

            if length >= dotted_gap:
                tt.penup()
                tt.fd(dotted_gap)
                length -= dotted_gap
            else:
                tt.penup()
                tt.fd(length)
                length = 0

        '''
        times = length // (dotted_line_length + dotted_gap)
        if length % (dotted_line_length + dotted_gap) != 0:
            times += 1
        length_walked = 0
        for i in range(times):
            if i != times - 1:
                tt.pendown()
                tt.fd(dotted_line_length)
                tt.penup()
                tt.fd(dotted_gap)
                length_walked += dotted_line_length + dotted_gap
            else:
                # 此时是最后一次，就是除不尽的余的部分，需要注意是否有足够长度。
                if length - length_walked > dotted_line_length:
                    tt.pendown()
                    tt.fd(dotted_line_length)
                    length_walked += dotted_line_length
                else:
                    tt.fd(length - length_walked)

                # 剩下就是(可能存在的)虚线部分了。不需要下笔，只需要走过去。
                tt.penup()
                tt.fd(length - length_walked)
        '''

    elif line_mode == LineModes.none:
        # 不绘制线
        tt.penup()
        tt.fd(length)

    # 在末尾点一下
    if if_dot_at_end:
        tt.dot(dot_diameter, dot_color)

    if write_name:
        write(write_name, align=name_align, vertical_align=name_vertical_align)


def goto(target_point: (list or tuple), line_mode=LineModes.solid, line_width=DEFAULT.LINE_WIDTH, line_color=Colors.black,
         write_name="", name_height=DEFAULT.FONT_HEIGHT, name_align=Align.LEFT, name_vertical_align=VerticalAlign.TOP,
         name_color=DEFAULT.FONT_COLOR,
         if_dot_at_end=True, dot_color=Colors.black, dot_diameter=DEFAULT.DOT_DIAMETER,
         dotted_line_length=DEFAULT.DOTTED_LINE_LENGTH, dotted_gap=DEFAULT.DOTTED_GAP):
    print(f"\n收到前往{target_point}的要求, line_mode {line_mode}")

    # 对目标点完成偏移
    target_point[0] += OFFSET[0]
    target_point[1] += OFFSET[1]
    print(f"加上偏移{OFFSET},为前往{target_point}")

    # 对目标点缩放
    target_point[0] *= SCALE
    target_point[1] *= SCALE
    print(f"加上缩放{SCALE}，确认为前往{target_point}")

    line_width *= SCALE
    dot_diameter *= SCALE
    dotted_line_length *= SCALE
    dotted_gap *= SCALE

    tt.pencolor(line_color)
    tt.pensize(line_width)

    if line_mode == LineModes.solid:
        # 绘制实线
        tt.pendown()
        tt.goto(target_point[0], target_point[1])
    elif line_mode == LineModes.dotted:
        # 绘制虚线
        length = distance(list(tt.position()), target_point)
        fd(length, line_width=line_width, line_color=line_color, line_mode=line_mode,
           if_dot_at_end=False,  # 注意不要在虚线绘制时点这个点，统一在本函数的结尾点。
           dotted_line_length=dotted_line_length, dotted_gap=dotted_gap)
        tt.penup()
        tt.goto(target_point[0], target_point[1])  # 确保抵达，避免角度带来的误差

    elif line_mode == LineModes.none:
        # 不绘制线
        tt.penup()
        tt.goto(target_point[0], target_point[1])
    print(f"已到达{target_point}")
    if if_dot_at_end:
        tt.dot(dot_diameter, dot_color)

    if write_name:
        write(write_name, font_height=name_height, align=name_align, vertical_align=name_vertical_align,
              font_color=name_color)


def write(string: str, pos=None, align=Align.LEFT, vertical_align=DEFAULT.FONT_VERTICAL_ALIGN,
          font_height=DEFAULT.FONT_HEIGHT, font_color=DEFAULT.FONT_COLOR,
          font_family=DEFAULT.FONT_FAMILY, font_weight=DEFAULT.FONT_WEIGHT):

    safe_padding = 10

    if FONT_SCALING:
        font_height = int(font_height * SCALE)
        safe_padding *= SCALE

    tt.penup()
    current_pos = tt.pos()
    current_heading = tt.heading()
    current_color = tt.pencolor()

    if pos is not None and pos != current_pos:
        tt.penup()
        tt.goto(pos)

    if vertical_align == VerticalAlign.TOP:
        tt.setpos(current_pos[0], current_pos[1] - font_height - safe_padding)
    elif vertical_align == VerticalAlign.MIDDLE:
        tt.setpos(current_pos[0], current_pos[1] - font_height / 2 - safe_padding)

    tt.pencolor(font_color)
    tt.write(string, align=align, font=(font_family, font_height, font_weight))

    # 恢复原来的位置和角度
    tt.penup()
    tt.setheading(current_heading)
    tt.goto(current_pos)
    tt.pencolor(current_color)


def auto_offset(points_pos, offset_mode=OffsetMode.none):
    result = 0
    if offset_mode == OffsetMode.none:
        result = [0, 0]
    elif offset_mode == OffsetMode.at_start:
        result = [-points_pos[0][0], -points_pos[0][1]]  # 这种情况下注意是负的
        print(f"已经设置偏移为第一个点{result}")
    elif offset_mode == OffsetMode.center:
        max_x = min_x = points_pos[0][0]
        max_y = min_y = points_pos[0][1]
        for pos in points_pos:
            x = pos[0]
            y = pos[1]

            if x > max_x:
                max_x = x
            elif x < min_x:
                min_x = x

            if y > max_y:
                max_y = y
            elif y < min_y:
                min_y = y
        print(f"正在计算偏移，max_x{max_x}, min_x{min_x}, max_y{max_y}, min_y{min_y}")
        result = [-(max_x + min_x) / 2, -(max_y + min_y) / 2]  # 这个也得是负的，是让中心点等效为0

    global OFFSET
    OFFSET = result
    print(f"自动offset已完成，设置为{result}")

    return result


def auto_scaling(points_pos):
    """
    传入若干个点，根据它所需的最大位置，选择一个合适的scale
    :param points_pos:
    :return:
    """

    # 注意！需要先计算offset再计算这个，因为offset没有依赖，但是这个依赖offset


    width = tt.window_width()
    height = tt.window_height()
    safe_padding_x = width * 0.1
    safe_padding_y = height * 0.1

    print(f"窗口大小：{width}, {height}")

    width -= 2 * safe_padding_x
    height -= 2 * safe_padding_y

    print(f"除去编剧，大小为{width}, {height}")

    max_x = min_x = points_pos[0][0] + OFFSET[0]
    max_y = min_y = points_pos[0][1] + OFFSET[1]

    for pos in points_pos:
        x = pos[0]
        y = pos[1]

        x += OFFSET[0]
        y += OFFSET[1]
        print(f"offset后点{x},{y}")
        if x > max_x:
            max_x = x
        elif x < min_x:
            min_x = x

        if y > max_y:
            max_y = y
        elif y < min_y:
            min_y = y
    print(f"正在计算scale，max_x{max_x}, min_x{min_x}, max_y{max_y}, min_y{min_y}")
    extreme_x = max(abs(max_x), abs(min_x))
    extreme_y = max(abs(max_y), abs(min_y))
    print(f"当前偏离原点最严重的x为{extreme_x}, y为{extreme_y},此即为核心图像大小")

    activate_width = extreme_x * 2
    activate_height = extreme_y * 2

    if extreme_x != 0:
        oa_x = width / activate_width
    else:
        oa_x = 1  # 理论上就是放大无数倍都看不到，那就没必要放大了

    if extreme_y != 0:
        oa_y = height / activate_height
    else:
        oa_y = 1

    if (oa_x < 1) or (oa_y < 1):  # 如果有某个不够用了，那自然是优先保证看得见全部点，就缩小显示比例
        result = min(oa_x, oa_y)
    else:
        result = min(oa_x, oa_y)

    global SCALE
    SCALE = result

    return result


def ensure_appearance(points_pos, offset_mode=OffsetMode.none):
    """
    传入要绘制的点，可以根据选择的策略自动使用offset来让内容剧中，并自动调整缩放为最佳尺寸
    :param points_pos: 需要绘制的点
    :param offset_mode: offset策略。可通过设置来改变显示窗口中心位置，让图像整体平移到一个更适合观看的位置。
                        OffsetMode.none为保持原样，即让系统原点位于窗口中心。
                        OffsetMode.at_start为把起始点作为窗口中心。
                        OffsetMode.center为把所有点组成的图像的中心位置作为窗口中心。
    :return: [offset, scale]
             返回计算出、并已经设置的最佳offset和缩放尺寸
    """
    offset = auto_offset(points_pos, offset_mode)
    scale = auto_scaling(points_pos)

    return [offset, scale]


def test():
    goto([0, 0], line_mode=LineModes.none, write_name="A")
    tt.setheading(0)

    fd(300, line_mode="dotted", line_color=Colors.blue, write_name="B")
    tt.right(90)
    fd(200, )
    tt.right(90)
    fd(300)
    tt.right(90)
    fd(200)


if __name__ == "__main__":

    test()
    set_scale(0.5)
    test()

    tt.done()
