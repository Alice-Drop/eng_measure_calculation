# -*- coding = "UTF-8" -*-
# aliceCSV v1.0.1
# @Author: AliceDrop
# License: MIT License

"""
This is a module to operate csv file as a list (two-dimensional table) basing on RFC 4180.
It is easy to use ,and has no dependent libraries.
"""


def parseLine(line: str, delimiter=","):
    """
    输入一行csv的内容，识别每一列，拆分成列表
    :param line: 准备拆分成列表的csv文件的某一行，是字符串形式
    :param delimiter: 分隔符
    :return: 返回按列拆分成的列表
    """
    output_list = []
    if '"' not in line:
        output_list = line.split(delimiter)
    else:
        division_list = line.split(delimiter)  # 先把整行通过逗号分割，可能会有不应分割的（用引号括起来的部分），
        quoting = False
        cache = ""
        for item in division_list:
            # print("item:", item)
            if quoting:  # 如果是引文状态，那么除非是读到末尾是引号也就是 ”, ，否则都是加到缓存里面拼起来  *****
                if item[-1] == '"':
                    cache += item
                    cache = cache[1:len(cache) - 1]  # 此时cache开头和结尾是双引号，需要去掉
                    cache = cache.replace('""', '"')  # 根据RFC 4180定义第7条，引文里面的双引号要变成两个，所以解读的时候要变回一个
                    output_list.append(cache)
                    cache = ""
                    quoting = False

                else:
                    cache += item
                    cache += delimiter  # 继续补回split去掉的分隔符

            else:  # 不是引文状态：
                if len(item) == 0:
                    output_list.append("")

                elif item[0] == '"':  # 如果第一项是引号，说明开始了一个引文  *****
                    if item[-1] == '"':  # 如果最后一项是 " ，那么就是说在引文里面没有逗号，引用在这个item里面就开始并结束，所以读到的这个item就是列表的一个列
                        item = item[1:len(item) - 1]  # 需要去掉开头和结尾的引号，提取出真正的内容
                        item = item.replace('""', '"')  # 根据RFC 4180定义第7条，引文里面的双引号要变成两个，所以解读的时候要变回一个
                        output_list.append(item)
                    else:  # 最后一项不是" ，那么就是说开始了一段引文，引文里有逗号所以拆成了几段，开quoting开始分析后面的  *****
                        quoting = True
                        cache += item
                        cache += delimiter  # 也就是说这里还是引文里面，逗号被split用掉了，所以要补上一个。
                else:  # 如果第一项不是引号，也就是说包含了 123"cde"f 之类的乱七八糟的格式，或者是不含引号的最普通的项，都是直接加到列表
                    output_list.append(item)

    return output_list


def parseCSV(csv_text: str, delimiter: str = ","):
    """
        把csv文件文本转为二维列表

        :param csv_text: csv文件文本内容
        :param delimiter: 分隔符
        :return: 二维列表
    """

    csv_text.replace("\r\n", "\n")  # 统一为\n为换行符
    table: list = csv_text.split("\n")  # 分割为列表

    for i in range(len(table)):
        table[i] = parseLine(table[i], delimiter)  # 遍历每一行，对每一行再次进行处理

    return table


def fixLineLength(csv_sheet):
    """
    根据RFC 4180 中csv文件的定义的第4条，每行应该含有相同数量的字段。因此对于数量对不上的要进行修复。

    :param csv_sheet: 用二维列表表示的csv文件
    :return:
    """
    max_length = 0
    for row in csv_sheet:  # 遍历每一行，获取最长的长度
        if len(row) > max_length:
            max_length = len(row)
    # print(max_length)
    for i in range(len(csv_sheet)):

        row: list = csv_sheet[i]  # 再次遍历每一行

        # print(f"开始处理第{i}行：{row}")
        # print(f"最大长度{max_length}-这一行的长度{len(row)}=" + str(max_length - len(row)))

        while len(row) < max_length:
            row.append("")  # 加上一个内容为空的列表项
            csv_sheet[i] = row  # 把更改提交

    return csv_sheet


def writeCSV(sheet, output_path="output.csv", delimiter=",", sheet_encoding="UTF-8", line_break="\n"):
    """
    把输入的二维列表输出为一个csv文件
    :param sheet: 一个二维列表
    :param output_path: 输出文件的路径
    :param delimiter:
    :param sheet_encoding: 输出文件使用的编码格式
    :param line_break: 输出文件使用的换行符
    """

    output = open(output_path, "w", encoding=sheet_encoding)
    for row in sheet:
        for i in range(len(row)):
            col = str(row[i])

            if '"' in col:  # 对是否要用引文进行判断
                output.write('"')  # 如果这一项里有引号，就用双引号括起来
                output.write(col.replace('"', '""'))  # 把字段里的引号变成两个引号（第一个用来转义）
                output.write('"')
            elif "," in col or "\n" in col or delimiter in col:  # 是否有特殊符号。注意有可能分隔符不是逗号，但根据标准逗号是必须要作特殊字符的。
                output.write('"')  # 如果这一项里有逗号或是换行符，就给它加上双引号。
                output.write(col)
                output.write('"')
            else:  # 如果上述情况都没有，那就是正常情况，直接字段写上去
                output.write(col)

            if i != len(row) - 1:  # 如果不是最后一项，就加上逗号
                output.write(delimiter)
        output.write(line_break)  # 换行

    output.close()


def fixCSV(path, output_path="output.csv", origin_delimiter=",", target_delimiter=",", origin_encoding="UTF-8",
           target_encoding="UTF-8", target_line_break="\n", fix_length=True):
    my_file = open(path, encoding=origin_encoding)
    csv_ext = my_file.read()
    table = parseCSV(csv_ext, delimiter=origin_delimiter)
    if fix_length:
        table = fixLineLength(table)
    writeCSV(table, output_path, target_delimiter, target_encoding, target_line_break)


if __name__ == "__main__":
    myFile = open("bugtest.csv", encoding="utf-8")
    myTable = parseCSV(myFile.read())
    print(myTable)

    fx = fixLineLength(myTable)

    print(fx)
