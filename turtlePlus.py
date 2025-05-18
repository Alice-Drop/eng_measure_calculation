import turtle as tt

class LineModes:
    solid = "solid"
    dotted = "dotted"
    none = "none"

class Colors:
    black = "black"
    white = "white"
    red = "red"
    blue = "blue"

class DEFAULT:
    LINE_WIDTH = 5
    DOTTED_LINE_LENGTH = 10  # 虚线的每个实线部分多长
    DOTTED_GAP = 10  # 虚线的实线间隔多大
    DOT_DIAMETER = 15


SCALE = 1.0


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

    return ((x_2-x_1)**2 + (y_2-y_1)**2)**(1/2)

def fd(length, line_width=DEFAULT.LINE_WIDTH, line_color=Colors.black, line_mode=LineModes.solid,
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


def goto(target_point: (list or tuple), line_mode=LineModes.solid, line_width=DEFAULT.LINE_WIDTH, line_color=Colors.black,
         if_dot_at_end=True, dot_color=Colors.black, dot_diameter=DEFAULT.DOT_DIAMETER,
         dotted_line_length=DEFAULT.DOTTED_LINE_LENGTH, dotted_gap=DEFAULT.DOTTED_GAP):

    target_point[0] *= SCALE
    target_point[1] *= SCALE

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

    if if_dot_at_end:
        tt.dot(dot_diameter, dot_color)

def test():
    goto([0, 0], line_mode=LineModes.none)
    tt.setheading(0)

    fd(300, line_mode="dotted", line_color=Colors.blue)
    tt.right(90)
    fd(200)
    tt.right(90)
    fd(300)
    tt.right(90)
    fd(200)


if __name__ == "__main__":
    test()
    set_scale(0.5)
    test()

    tt.done()
