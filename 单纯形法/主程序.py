from PyQt6.QtWidgets import QApplication,QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("单元形法")
        self.setGeometry(100, 100, 800, 600)
        
        # 设置窗口图标
        self.setWindowIcon(QPixmap("icon.png"))
        
        # 设置窗口背景颜色
        self.setStyleSheet("background-color: lightblue;")
        
        # 设置窗口标题栏文本颜色
        self.setStyleSheet("QMainWindow { color: darkblue; }")

