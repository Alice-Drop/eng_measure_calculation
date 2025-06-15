import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem, \
    QPushButton, QFileDialog, QLineEdit, QMessageBox, QHBoxLayout

import load_data, Traversing


class MainWindow:
    def __init__(self):
        DEFAULT_PATH = "/Users/alice/PycharmProjects/eng_measure_calculation/data/connectingTraverse_test_data.json"
        self.path = DEFAULT_PATH
        self.accuracy = 3
        self.son_windows = []

        self.ui = QWidget()
        self.ui.setWindowTitle("工程测量计算")
        self.ui.resize(400, 250)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        div_path = QWidget()
        div_path.setLayout(QHBoxLayout())
        label_path = QLabel("输入路径")
        txt_path = QLineEdit(self.path, readOnly=True)
        btn_import = QPushButton("...")
        btn_import.setMaximumWidth(100)
        btn_import.clicked.connect(self.get_path)

        div_path.layout().addWidget(label_path)
        div_path.layout().addWidget(txt_path)
        div_path.layout().addWidget(btn_import)
        self.main_layout.addWidget(div_path)


        div_accuracy = QWidget()
        div_accuracy.setLayout(QHBoxLayout())
        label_accuracy = QLabel("保留几位小数？")
        self.input_accuracy = QLineEdit("3")
        self.input_accuracy.setMaximumWidth(200)
        div_accuracy.layout().addWidget(label_accuracy)
        div_accuracy.layout().addWidget(self.input_accuracy)

        self.main_layout.addWidget(div_accuracy)

        btn_start = QPushButton("开始内业计算")
        btn_start.clicked.connect(self.start_traverse)
        btn_start.setStyleSheet("background-color: rgb(83,138,247);margin: 20px 5px;padding: 10px;border-radius: 5px;border:none;")
        self.main_layout.addWidget(btn_start)

        self.ui.setLayout(self.main_layout)




    def get_path(self):
        data_path = QFileDialog.getOpenFileName(self.ui, filter="json文件 *.json", dir="./")[0]
        self.path =  data_path

    def start_traverse(self):

        # global global_windows_main
        if (not self.path) or (not os.path.exists(self.path)):
            QMessageBox.warning(self.ui, "警告", "未选择正确数据文件。")

        else:
            accuracy = int(self.input_accuracy.text())
            if (not accuracy) or (accuracy < 0):
                accuracy = 3
            self.accuracy = accuracy

            data = load_data.load_user_data(self.path)

            points_report, lines_report = Traversing.connectionTraverse_calculate_V3(data, accuracy)

            window_1 = TableViewer(points_report, points_report[0][0])
            window_1.move(100, 200)
            window_2 = TableViewer(lines_report, lines_report[0][0])
            window_2.move(200, 300)
            self.son_windows.append(window_1)
            self.son_windows.append(window_2)
            window_1.show()
            window_2.show()


class TableViewer(QWidget):
    def __init__(self, data, title="TableViewer", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(1000, 300)

        layout = QVBoxLayout()

        label = QLabel("数据")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(data[0]))


        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(round(value, 6)) if isinstance(value, float) else str(value))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        table.setAlternatingRowColors(True)

        layout.addWidget(table)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.ui.show()
    global_windows = []
    app.exec()
