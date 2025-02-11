#!/usr/bin/env python3
import re
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap, QIcon, QDragEnterEvent, QDropEvent


import merge_brochure
import merge_duplex


class FileDropLabel(QLabel):
    file_dropped = Signal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText("将文件拖放到此区域")
        self.setStyleSheet("""
            border: 1px ridge;
            padding: 20px;
        """)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        paths = [url.toLocalFile() for url in urls]
        self.file_dropped.emit(paths)


class FileDropApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("双面打印和小册子打印")
        self.resize(500, 400)
        self.setWindowIcon(QIcon('bell.ico'))  # 假设你的图标文件名为 icon.ico

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 创建拖放区域
        self.drop_label = FileDropLabel()
        self.drop_label.file_dropped.connect(self.handle_drop)
        self.layout.addWidget(self.drop_label)

        # 创建按钮面板
        button_layout = QHBoxLayout()
        self.process_btn_duplex = QPushButton("双面打印")
        self.process_btn_duplex.clicked.connect(self.process_files_duplex)
        button_layout.addWidget(self.process_btn_duplex)

        self.process_btn_brochure = QPushButton("小册子打印")
        self.process_btn_brochure.clicked.connect(self.process_files_brochure)
        button_layout.addWidget(self.process_btn_brochure)

        self.clear_btn = QPushButton("清除")
        self.clear_btn.clicked.connect(self.clear_files)
        button_layout.addWidget(self.clear_btn)

        self.layout.addLayout(button_layout)

        self.file_paths = []

    @Slot(list)
    def handle_drop(self, paths):
        self.file_paths = paths
        file_list = "\n".join(self.file_paths)
        self.drop_label.setText(f"已选择文件：\n{file_list}")

    def process_files_duplex(self):
        if self.file_paths:
            print("正在处理文件：")
            for path in self.file_paths:
                print(f"处理文件：{path}")
                merge_duplex.main(path)
            QMessageBox.information(self, "处理完成", "文件处理完成！")
        else:
            QMessageBox.warning(self, "无文件", "请先拖放文件到指定区域")

    def process_files_brochure(self):
        if self.file_paths:
            print("正在处理文件：")
            for path in self.file_paths:
                print(f"处理文件：{path}")
                merge_brochure.main(path)
            QMessageBox.information(self, "处理完成", "文件处理完成！")
        else:
            QMessageBox.warning(self, "无文件", "请先拖放文件到指定区域")

    def clear_files(self):
        self.file_paths = []
        self.drop_label.setText("将文件拖放到此区域")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileDropApp()
    window.show()
    sys.exit(app.exec())


