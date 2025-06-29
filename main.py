
import Traversing
import gui_tk

import gui

import tkinter as tk


def parse_pos_txt(pos_txt: str, pos_type=int):
    # 把用户输入进来的文本形式的坐标转换为列表形式
    pos_txt = pos_txt.replace("(", "").replace(")", "").replace("[", "").replace("]", "")
    pos_txt = pos_txt.replace("，", ",")

    pos = []
    if pos_type == int:
        pos = [int(item) for item in pos_txt.split(",")]
    elif pos_type == float:
        pos = [float(item) for item in pos_txt.split(",")]

    print(pos)

    return pos

"""def main():
    with open("example_connectingTraverse.json", "w", encoding="UTF-8") as my_file:
        json.dump(Traversing.connectingTraverse_test_data, my_file,
                  indent=3,
                  default=angle_mangement.angle_to_json)

    print("欢迎使用")
    choice = ensureInput("需要执行什么操作？\n1.使用内置数据进行内业测量\n2.手动输入数据\n", accepted_values=["1", "2"])

    if choice == "1":
        choice = ensureInput("选择模式：\n1.闭合导线测量\n2.附合导线测量", accepted_values=["1", "2"])
        if choice == "1":
            start_point_pos = parse_pos_txt(input("请输入已知的起始点B的坐标："))
            start_alpha_angle = angle_mangement.Angle(input("请输入已知开始线段AB的方位角α_AB（如使用度分秒格式，用'当作° ' ''即可）："))
        elif choice == "2":
            # 附合导线测量
            start_point_pos = parse_pos_txt(input("请输入已知的起始点B的坐标："))
            start_alpha_angle = angle_mangement.Angle(
                input("请输入已知开始线段AB的方位角α_AB\n（如使用度分秒格式，用'当作° ' ''即可， 比如 46'45'24' ）："))

            points = []
            point_count = 1
            while 1:

                start_point_answer = input(f"请输入第{point_count}个未知点处与上一条线的转折角β_{point_count}。或者直接按下回车来结束输入。\n")
                if len(start_point_answer) == 0:  # 如果输入为空
                    break

                beta = angle_mangement.Angle(start_point_answer)
                direction = ensureInput(f"这个转折角是：\nL.左角\nR.右角\n", accepted_values=["L", "R"])

                points.append(Traversing.PointDataItem([], point_count, beta, direction))
                print("\n")

            end_alpha_angle = angle_mangement.Angle(
                input("请输入已知结束线段CD的方位角α_CD\n（如使用度分秒格式，用'当作° ' ''即可， 比如 46'45'24' ）："))

            traverse_data = {
                MeasureDataKeys.measureType: MeasureType.ConnectingTraverse,
                MeasureDataKeys.start_line_angle_alpha: start_alpha_angle,  # 起始线段AB的角
                MeasureDataKeys.points: points,
                MeasureDataKeys.end_line_angle_alpha: end_alpha_angle
            }

def main_v2():
    print("请传入目标数据：")
    #data_path = QFileDialog.getOpenFileName(None, filter="json文件 *.json",dir="./")[0]
    data_path = "/Users/alice/PycharmProjects/eng_measure_calculation/data/connectingTraverse_test_data.json"
    print(str(data_path))
    if os.path.exists(str(data_path)):
        data = load_data.load_user_data(data_path)
        #accuracy = input("保留的精度？（默认保留3位小数，如无异议直接按下回车）")
        accuracy = 3
        if not accuracy:
            accuracy = 3
        else:
            accuracy = int(accuracy)

        points_report, lines_report = Traversing.connectionTraverse_calculate_V3(data, accuracy)
        return [points_report, lines_report]

    else:
        QMessageBox.warning(None, "警告", "警告！未正确指定文件。软件将退出。")
        return []


def main_v3():
    app = QApplication([])

    main_window = gui.MainWindow()
    main_window.ui.show()

    for sheet in data:
        print(sheet)
        window = gui.TableViewer(sheet, sheet[0][0])
        print(f"已经产生窗口，{window}")
        window.show()
        time.sleep(1) 
    app.exec()
"""

def main_v4():
    root = tk.Tk()
    app = gui_tk.MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    global_windows_main = []
    main_v4()