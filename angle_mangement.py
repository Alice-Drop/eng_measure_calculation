class MathAngle:
    # 数学上的象限角，0°为正东方向（也是x轴方向）
    def __init__(self, angle):
        self.type = MathAngle
        self.value = angle


def strongInt(obj):
    if type(obj) is int:
        return obj
    elif type(obj) is float:
        return obj // 1
    elif type(obj) is str:
        valid_part = ""
        for i in range(len(obj)):
            char = obj[i]
            if char.isdigit():
                valid_part += char
            else:
                break
        return int(valid_part)
    else:
        print(type(obj))
        return int(obj)


def parseDMS(string: str) -> list:
    # 解析文本格式的DMS角度，返回°、'、''。目前仅支持整数的角
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
        self.value = parseDMS(string)

    def toDEC(self):
        dec_value = self.value[0] + self.value[1] * (1 / 60) + self.value[2] * (1 / 3600)
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
        self.value = float(string)

    def toDMS(self):
        deg = minute = second = 0
        deg = self.value // 1
        deg_rest = self.value % 1
        if deg_rest != 0:
            minute = deg_rest * 60
            minute_rest = round(minute % 1, 6)

            if minute_rest != 0:
                minute = minute // 1
                # print(f"剩下的min{minute_rest}")
                second = round(minute_rest * 60, 6)  # 用四舍五入解决了浮点数精度问题

        return DMS(f"{str(deg)}'{str(minute)}'{str(second)}'")

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
        self.string = string
        self.angle_type = angle_type
        if "'" in string:
            self.format = AngleFormats.DMS
            self.data = DMS(string)
        else:
            self.format = AngleFormats.DEC
            self.data = DEC(string)

    def valueDMS(self):
        if self.format == AngleFormats.DMS:
            return self.data.value
        else:
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
            if angle_format_1 == angle_format_2:
                if angle_format_1 == AngleFormats.DMS:
                    value_1 = self.valueDMS()
                    value_2 = other.valueDMS()
                    result = [value_1[0] + value_2[0],  # 不用担心长度问题，在创建时即使是0秒也创建了的
                              value_1[1] + value_2[1],
                              value_1[2] + value_2[2]
                              ]
                else:
                    value_1 = self.valueDEC()
                    value_2 = other.valueDEC()
                    result = value_1 + value_2

                return Angle(str(result))
            else:
                value_1 = self.valueDEC()
                value_2 = other.valueDEC()
                result = value_1 + value_2
                return Angle(str(result))
        else:
            raise TypeError(f"警告！无法把Angle与{type(other)} {other}相加。")

    def __sub__(self, other):
        if isinstance(other, Angle):  # 都是Angle对象
            angle_format_1 = self.format
            angle_format_2 = other.format
            if angle_format_1 == angle_format_2:
                if angle_format_1 == AngleFormats.DMS:
                    value_1 = self.valueDMS()
                    value_2 = other.valueDMS()
                    result = [value_1[0] - value_2[0],  # 不用担心长度问题，在创建时即使是0秒也创建了的
                              value_1[1] - value_2[1],
                              value_1[2] - value_2[2]
                              ]
                else:
                    value_1 = self.valueDEC()
                    value_2 = other.valueDEC()
                    result = value_1 - value_2

                return Angle(str(result))
            else:
                value_1 = self.valueDEC()
                value_2 = other.valueDEC()
                result = value_1 - value_2
                return Angle(str(result))
        else:
            raise TypeError(f"警告！无法把Angle与{type(other)} {other}相加。")

    def __truediv__(self, other):
        if (type(other) is int) or (type(other) is float):
            return self.valueDEC() / other

    def __str__(self):
        return f"_Angle:{DMStoStr(self.valueDMS())}({self.valueDEC()})"

    def __repr__(self):
        return self.__str__()


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
    angle_1 = Angle("120'30'52'")
    print(angle_1.valueDEC())
    print(angle_1.valueDMS())
    angle_2 = Angle("45.50")
    print(angle_1 - angle_2)
