#!/bin/python3
import re
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import merge_brochure
import merge_duplex

class FileDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件拖放应用")
        self.root.geometry("500x400")
        
        # 初始化样式
        self.style = ttk.Style(theme="flatly")
        
        # 创建主界面布局
        self.create_widgets()
        self.file_paths = []

    def create_widgets(self):
        # 创建拖放区域
        self.drop_frame = ttk.Frame(self.root, padding=10)
        self.drop_frame.pack(fill=BOTH, expand=True, pady=20)
        
        self.drop_label = ttk.Label(
            self.drop_frame,
            text="将文件拖放到此区域",
            borderwidth=2,
            relief="ridge",
            padding=20,
            anchor="center",
            font=("Helvetica", 12),
            bootstyle="inverse-light"
        )
        self.drop_label.pack(fill=BOTH, expand=True)
        
        # # 注册拖放功能
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.handle_drop)
        
        # self.drop_label.bind("<Button-1>", self.handle_drop)

        # 创建按钮面板
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)
        
        # 处理按钮
        self.process_btn_duplex = ttk.Button(
            button_frame,
            text="双面打印",
            command=self.process_files_duplex,
            bootstyle="success",
            width=10
        )
        self.process_btn_duplex.pack(side=LEFT, padx=5, expand=True)

        self.process_btn_brochure = ttk.Button(
            button_frame,
            text="小册子打印",
            command=self.process_files_brochure,
            bootstyle="success",
            width=10
        )
        self.process_btn_brochure.pack(side=LEFT, padx=5, expand=True)

        # 清除按钮
        self.clear_btn = ttk.Button(
            button_frame,
            text="清除",
            command=self.clear_files,
            bootstyle="danger",
            width=10
        )
        self.clear_btn.pack(side=LEFT, padx=5, expand=True)

    def handle_drop(self, event):
        # 使用正则表达式提取带空格的路径
        files = re.findall(r'\{(.*?)\}', event.data)
        if files:
            self.file_paths = files
        else:
            self.file_paths = event.data.split()
        
        # 更新显示文本
        file_list = "\n".join(self.file_paths)
        self.drop_label.config(text=f"已选择文件：\n{file_list}")

    def process_files_duplex(self):
        if self.file_paths:
            print("正在处理文件：")
            for path in self.file_paths:
                print(f"处理文件：{path}")
                merge_duplex.main(path)
            # 这里可以添加实际的文件处理代码
            messagebox.showinfo("处理完成", "文件处理完成！")
        else:
            messagebox.showwarning("无文件", "请先拖放文件到指定区域")

    def process_files_brochure(self):
        if self.file_paths:
            print("正在处理文件：")
            for path in self.file_paths:
                print(f"处理文件：{path}")
                merge_brochure.main(path)
            # 这里可以添加实际的文件处理代码
            messagebox.showinfo("处理完成", "文件处理完成！")
        else:
            messagebox.showwarning("无文件", "请先拖放文件到指定区域")

    def clear_files(self):
        self.file_paths = []
        self.drop_label.config(text="将文件拖放到此区域")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FileDropApp(root)
    root.mainloop()
