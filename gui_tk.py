import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json

# 假设这些函数是你已有的业务逻辑
import load_data
import Traversing

# 前面定义的 TableViewer 类复用（略去重复定义）


def log(content=""):
    if_log = False
    if if_log:
        print(content)


class TableViewer(tk.Toplevel):
    def __init__(self, data, title="TableViewer"):
        super().__init__()
        log(f"TableViewer被创建: {title}")
        self.title(title)
        self.geometry("1000x300")

        label = tk.Label(self, text="数据", font=("Arial", 14))
        label.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=[f"#{i}" for i in range(len(data[0]))], show="headings")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for i in range(len(data[0])):
            tree.heading(f"#{i}", text=f"列{i+1}")
            tree.column(f"#{i}", width=100, anchor="center")

        for row in data:
            formatted = [
                f"{v:.6f}" if isinstance(v, float) else str(v)
                for v in row
            ]
            tree.insert("", "end", values=formatted)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("工程测量计算")
        master.geometry("400x250")

        self.path = "./data/connectingTraverse_test_data.json"
        self.accuracy = 3
        self.son_windows = []

        # 输入路径部分
        frame_path = tk.Frame(master)
        frame_path.pack(fill="x", pady=10, padx=10)

        tk.Label(frame_path, text="输入路径").pack(side="left")
        self.txt_path = tk.Entry(frame_path, width=30)
        self.txt_path.insert(0, self.path)
        self.txt_path.configure(state="readonly")
        self.txt_path.pack(side="left", padx=5)

        btn_import = tk.Button(frame_path, text="...", command=self.get_path, width=5)
        btn_import.pack(side="left")

        # 精度输入
        frame_accuracy = tk.Frame(master)
        frame_accuracy.pack(fill="x", pady=10, padx=10)

        tk.Label(frame_accuracy, text="保留几位小数？").pack(side="left")
        self.entry_accuracy = tk.Entry(frame_accuracy, width=10)
        self.entry_accuracy.insert(0, "3")
        self.entry_accuracy.pack(side="left", padx=5)

        # 计算按钮
        self.btn_start = tk.Button(
            master,
            text="开始内业计算",
            command=self.start_traverse,
            width=20
        )
        self.btn_start.pack(pady=20)

    def get_path(self):
        path = filedialog.askopenfilename(title="选择JSON数据文件", filetypes=[("JSON文件", "*.json")])
        if path:
            self.path = path
            self.txt_path.configure(state="normal")
            self.txt_path.delete(0, "end")
            self.txt_path.insert(0, path)
            self.txt_path.configure(state="readonly")

    def start_traverse(self):
        if not self.path or not os.path.exists(self.path):
            messagebox.showwarning("警告", "未选择正确数据文件。")
            return

        try:
            accuracy = int(self.entry_accuracy.get())
            if accuracy < 0:
                accuracy = 3
        except ValueError:
            accuracy = 3
        self.accuracy = accuracy

        data = load_data.load_user_data(self.path)
        points_report, lines_report = Traversing.connectionTraverse_calculate_V3(data, accuracy)
        log(points_report[0][0])
        # window_1 = TableViewer(points_report, points_report[0][0])
        # window_1.geometry("+100+200")
        # window_2 = TableViewer(lines_report, lines_report[0][0])
        # window_2.geometry("+200+300")
        # self.son_windows.extend([window_1, window_2])
        # window_1.focus()
        # window_2.focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
