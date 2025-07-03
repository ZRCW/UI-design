from PyQt6.QtWidgets import QApplication,QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from 线性规划_图解法_ui import Ui_MainWindow
from 线性规划_图解法_计算结果 import LpProblem_solve
from 线性规划_图解法_图形生成 import LpProblem_solve_plot
import sys


class Llieproblem(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def information_collect(self):
        # 数据收集
        return{
            'gear_A': int(self.gear_A.text()),
            'gear_B': int(self.gear_B.text()),
            'gear_profit': int(self.gear_profit.text()),
            'bearing_A': int(self.bearing_A.text()),
            'bearing_B': int(self.bearing_B.text()),
            'bearing_profit': int(self.bearing_profit.text()),
            'inventory_A': int(self.inventory_A.text()),
            'inventory_B': int(self.lineEdit_9.text())
        }

    def LpProblem_solve(self):
        # 调用数据计算结果函数
        input_data = self.information_collect()
        print(input_data)
        result = LpProblem_solve(input_data)
        self.x1_varValue.setText(str(result["生产量"]["齿轮"]))
        self.x2_varValue.setText(str(result["生产量"]["轴承"]))
        self.leMaxProfit.setText(str(result["最大利润"]))
        self.Constrain1.setText(str(result["约束条件"]["约束1"]))
        self.Constrain2.setText(str(result["约束条件"]["约束2"]))
        self.Constrain3.setText(str(result["约束条件"]["约束3"]))
        self.Constrain4.setText(str(result["约束条件"]["约束4"]))

    def LpProblem_solve_plot(self):
        # 调用图形绘制函数
        input_data = self.information_collect()
        image_route = LpProblem_solve_plot(input_data)
        image = QPixmap(image_route)
        scaled_image = image.scaled(
            self.plot.size(),  # 使用控件当前尺寸
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.plot.setPixmap(scaled_image)


# 启动入口
if __name__ == '__main__':
    if False:
        print(input_data)
        print(f"{image_route}")
    app = QApplication(sys.argv)					# 初始化应用
    m = Llieproblem()								# 创建界面
    m.show()										# 显示界面
    sys.exit(app.exec())							# 在主线程中退出