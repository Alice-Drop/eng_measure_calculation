class MathAngle:
    # 数学上的象限角，0°为正东方向（也是x轴方向）
    def __init__(self, angle):
        self.type = MathAngle
        self.value = angle


def strongInt(obj):
    digi_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]  # int不能处理带小数点的str
    if type(obj) is int:
        return obj
    elif type(obj) is float:
        return int(obj)
    elif type(obj) is str:
        valid_part = ""
        for i in range(len(obj)):
            char = obj[i]
            if char in digi_chars:
                valid_part += char
            else:
                break
        return int(valid_part)
    else:
        print(type(obj))
        return int(obj)


def parseDMS(string: str) -> list:
    # 解析文本格式的DMS角度，返回°、'、''。目前仅支持整数的角
    # print(f"传入内容{string}，希望转换为DMS的列表")
    part_cont = string.count("'")
    deg = minute = second = 0
    if (part_cont == 0) or (part_cont == 1):  # 如 45 或45'
        deg = strongInt(string)
    elif part_cont == 2:  # 如 45'32‘
        deg, minute = strongInt(string.split("'")[0]), strongInt(string.split("'")[1])
    elif part_cont == 3:  # 如 45'32‘56’
        deg, minute, second = strongInt(string.split("'")[0]), strongInt(string.split("'")[1]), strongInt(
            string.split("'")[2])
    else:
        raise ValueError(f"Warning! Too many \"\'\" in DMS text {string}.")

    return [deg, minute, second]


def DMStoStr(DMS_data: list):
    string = ""
    for item in DMS_data:
        string += str(item)
        string += "'"
    return string


class AngleFormats:
    DMS = "DMS"
    DEC = "DEC"


class DMS:
    # 使用度分秒格式的角
    def __init__(self, string: str):
        self.string = string
        self.is_negative = "-" in string
        self.value = parseDMS(string)

    def toDEC(self):
        # print(f"to dec, {self.value}, is_negative:{self.is_negative}")
        if self.is_negative:
            dec_value = abs(self.value[0]) + self.value[1] * (1 / 60) + self.value[2] * (1 / 3600)
            # print(dec_value)
            dec_value = - dec_value
        else:
            dec_value = self.value[0] + self.value[1] * (1 / 60) + self.value[2] * (1 / 3600)
        dec_value = round(dec_value, 7)  # 避免float精度问题
        return DEC(str(dec_value))

    def toStr(self):
        string = ""
        for item in self.value:
            string += str(item)
            string += "'"
        return string


class DEC:
    # 十进制的角，
    def __init__(self, string: str):
        self.string = string
        self.is_negative = "-" in string
        self.value = float(string)

    def toDMS(self):
        deg = minute = second = 0
        abs_value = abs(self.value)  # 负数除法有问题，需要用绝对值来算再手动加上负

        deg = int(abs_value)
        deg_rest = abs_value - deg
        float_minute = deg_rest * 60
        # print(f"\n正在尝试转换{self.value}为DMS")
        # print(f"度：{deg}, 剩下内容：{deg_rest}")
        if deg_rest != 0:
            minute = int(float_minute)
            minute_rest = float_minute - minute
            # print(f"分：{minute}, 剩下内容：{minute_rest}")

            if minute_rest != 0:
                # print(minute)
                # print(f"剩下的min {minute_rest}")
                second = strongInt(minute_rest * 60)
                # print(f"秒：{second},")

        if self.is_negative:
            deg = - deg  # 按照人的习惯，只用在角那里是负的就好了。

        result_txt = f"{str(deg)}'{minute}'{str(second)}'"
        # print(f"{result_txt}")
        return DMS(result_txt)

    def toStr(self):
        return self.string


class AngleTypes:
    unsigned = "AngleTypes.unsigned"
    eng_beta = "AngleTypes.eng_beta"
    eng_alpha = "AngleTypes.eng_alpha"  # 方位角
    # 数学的笛卡尔坐标系角度，以正东方向为0，逆时针为正
    math_east_angle = "AngleTypes.math_east_angle"


def eng_angle_to_math_angle(angle_value: float):
    return (-angle_value + 90) % 360


class Angle:
    def __init__(self, string: str, angle_type=AngleTypes.eng_alpha):
        # print(f"受要求创建{string}为角度")
        string = string.replace("_Angle:", "")
        self.string = string
        self.angle_type = angle_type
        if string.count("'") > 1:    # 之前是if ""' in ，但是没照顾到45'也是正确写法
            self.format = AngleFormats.DMS
            self.data = DMS(string)
            # print(f"有', 为DMS, {self}\n")
        else:
            string = string.replace("'", "")  # 由于可能有45'这样的写法，把他当成输进来一个45就是了
            self.format = AngleFormats.DEC
            self.data = DEC(string)
            # print(f"没有', 为DEC, {self}\n")

    def valueDMS(self):
        if self.format == AngleFormats.DMS:
            return self.data.value
        else:
            # print(f"正在执行valueDMS,检测到需要toDMS，DMS的结果为{self.data.toDMS()}，结果为{self.data.toDMS().value}")
            return self.data.toDMS().value

    def valueDEC(self):
        if self.format == AngleFormats.DEC:
            return self.data.value
        else:
            return self.data.toDEC().value

    def valueMath(self, wanted_format=AngleFormats.DEC):
        if (self.angle_type == AngleTypes.math_east_angle) \
                or (self.format == AngleTypes.unsigned) \
                or (self.format == AngleTypes.eng_beta):
            return self.valueDEC()
        elif self.angle_type == AngleTypes.eng_alpha:
            return eng_angle_to_math_angle(self.valueDEC())

    def __add__(self, other):
        if isinstance(other, Angle):  # 都是Angle对象
            angle_format_1 = self.format
            angle_format_2 = other.format

            value_1 = self.valueDEC()
            value_2 = other.valueDEC()
            result = value_1 + value_2
            result = round(result, 7)
            return Angle(str(result))

        else:
            raise TypeError(f"警告！无法把Angle与{type(other)} {other}相加。")

    def __sub__(self, other):
        print(f"正在进行角度相减：{self}, {other}")
        if isinstance(other, Angle):  # 都是Angle对象
            angle_format_1 = self.format
            angle_format_2 = other.format

            value_1 = self.valueDEC()
            value_2 = other.valueDEC()
            result = value_1 - value_2
            result = round(result, 7)
            print(f"相减结果：{result}")
            return Angle(str(result))
        else:
            raise TypeError(f"警告！无法把Angle与{type(other)} {other}相加。")

    def __truediv__(self, other):
        if (type(other) is int) or (type(other) is float):
            return round(self.valueDEC() / other, 7)

    def __str__(self):
        return f"_Angle:{DMStoStr(self.valueDMS())}"

    def __repr__(self):
        return f"_Angle:{DMStoStr(self.valueDMS())}({self.valueDEC()}°)"


class AngleDirection:
    left_beta = "left_beta"
    right_beta = "right_beta"


def angle_to_json(obj):
    if isinstance(obj, Angle):
        return f"_Angle:{obj.string}"
    else:
        print(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def json_txt_to_angle(txt: str):
    if txt.startswith("_Angle:"):
        return Angle(txt.replace("_Angle:", ""))
    else:
        raise ValueError(f"{txt} is not a json sign of Angle.")


if __name__ == "__main__":

    # 测试strongInt
    print(strongInt("-1.6"))


    angle_1 = Angle("-120'30'52'")
    print(angle_1)
    print(angle_1.valueDMS())
    angle_2 = Angle("45.50")
    print(angle_1 - angle_2)

    # 追加稳定性测试
    angle_3 = Angle("99.0166667")
    print(f"3:{angle_3}, 文本为{angle_3.string}")
    angle_3 = Angle("99.01833336666667")
    print(f"3:{angle_3}, 文本为{angle_3.string}")

    # 测试4
    print("测试4")
    angle_4 = Angle("38'14'24'")
    angle_5 = Angle("38'15'0'")
    print(f" {angle_4.format},{angle_5.format}")
    print(f"4 {angle_4-angle_5}")

    # 基础正负测试
    print("基础正负测试")
    print(f"{Angle("-120'30'52'")}, {Angle("-120'30'52'").valueDEC()}")
    print(f"{Angle("-99.0166667")}, {Angle("-99.0166667").valueDMS()}")



