def ensureInput(txt: str, mode: int = 0, auto_end_word="\n", customize_warning: str = "请正确输入！", wanted_type: type = str,
                accept_empty=False, accepted_values=None, necessary_components=None):
    """
    要求用户输入，如果不符合要求则要从用户重新输入，直到内容有效。
    只传入输入提示语txt，则仅检查是否为空。


    :param txt: 输入用的文本
    :param auto_end_word: 自动在末尾添加一个结束语，比如换行。
    :param mode: 0表示如果用户输入有问题，会把警告语和问题拼合在一起输出
                 1 表示是只输出警告语
    :param customize_warning: 警告语
    :param wanted_type:
    :param accepted_values: 限定只有某些值是合法的。

    :param accept_empty: 是否允许用户输入空的。默认是不允许。
    :param necessary_components:
    :return: None
    """
    flag = 0
    result = ""
    count = 0

    if not txt.endswith(auto_end_word):
        txt += auto_end_word

    while not flag:
        if count == 0:
            # 第一次不要加警告语。
            result = input(txt)
        else:
            count += 1
            if mode == 0:
                result = input(customize_warning + txt)
            elif mode == 1:
                result = input(customize_warning)
            else:
                raise ValueError(f"Invalid mode '{mode}' for ensureInput.")

        check_result = []

        # print(f"输入了{result}")
        if (len(result) > 0) :
            # 默认要检查输入非空
            check_result.append(1)  # 指出非空/允许非空检测通过

            if accepted_values is not None:
                # print("检测到需检查的合法参数列表传入")
                if result in accepted_values:
                    check_result.append(1)
                else:
                    check_result.append(0)

            if necessary_components is not None:
                for component in necessary_components:
                    if component not in result:
                        check_result.append(0)
                    else:
                        check_result.append(1)

        else:
            # 如果为空，如果允许那没问题，否则一票否决
            if accept_empty:
                check_result.append(1)
            else:
                check_result.append(0)

        # print(check_result)
        for item in check_result:
            if not item:
                # 有任意一项不满足则结束本次，再次提问。
                flag = 0
                break
            else:
                flag = 1

    return wanted_type(result)


if __name__ == "__main__":
    ensureInput("请输入输入exit：", accepted_values=["exit"])

    ensureInput("请输入含有字母a的内容：", necessary_components=["a"])
