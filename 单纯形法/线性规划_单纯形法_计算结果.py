'''整数规划问题：使用单纯形法计算产品最大利润'''
import sys
import numpy as np

class SimplexSolver:
    def __init__(self, input_data):
        self.input_data = input_data
        self.tableau = None
        self.basic_vars = None
        self.non_basic_vars = None

    def initialize_tableau(self):
        # 提取输入数据
        c1 = self.input_data['gear_profit']  # 目标函数系数 x1
        c2 = self.input_data['bearing_profit']  # 目标函数系数 x2

        # 约束系数
        a11, a12 = self.input_data['gear_A'], self.input_data['bearing_A']
        a21, a22 = self.input_data['gear_B'], self.input_data['bearing_B']
        b1 = self.input_data['inventory_A']
        b2 = self.input_data['inventory_B']

        # 构建初始单纯形表 (标准形式: max c^T x, s.t. Ax <= b, x >= 0)
        # 添加松弛变量 s1, s2
        self.tableau = np.array([
            [1, -c1, -c2, 0, 0, 0],   # 目标函数行
            [0, a11, a12, 1, 0, b1],  # 约束1
            [0, a21, a22, 0, 1, b2]   # 约束2
        ])

        # 初始基变量 (松弛变量)
        self.basic_vars = [3, 4]  # s1, s2 的索引
        self.non_basic_vars = [1, 2]  # x1, x2 的索引

    def solve(self):
        self.initialize_tableau()

        while True:
            # 检查最优性 (目标行中是否有负系数)
            obj_row = self.tableau[0, 1:-1]
            entering_col = np.argmin(obj_row) + 1  # +1 跳过第一列

            if obj_row[entering_col-1] >= 0:
                break  # 达到最优解

            # 选择离基变量 (最小比率检验)
            ratios = []
            for i in range(1, len(self.tableau)):
                if self.tableau[i, entering_col] > 0:
                    ratios.append(self.tableau[i, -1] / self.tableau[i, entering_col])
                else:
                    ratios.append(np.inf)

            leaving_row = np.argmin(ratios) + 1  # +1 跳过目标行

            # 更新基变量
            leaving_var = self.basic_vars[leaving_row-1]
            self.basic_vars[leaving_row-1] = entering_col
            self.non_basic_vars.remove(entering_col)
            self.non_basic_vars.append(leaving_var)

            # 高斯消元 (主元行归一化)
            pivot = self.tableau[leaving_row, entering_col]
            self.tableau[leaving_row, :] /= pivot

            # 消去其他行
            for i in range(len(self.tableau)):
                if i != leaving_row:
                    factor = self.tableau[i, entering_col]
                    self.tableau[i, :] -= factor * self.tableau[leaving_row, :]

        # 提取结果
        solution = np.zeros(4)  # x1, x2, s1, s2
        for i, var in enumerate(self.basic_vars):
            solution[var-1] = self.tableau[i+1, -1]

        x1 = solution[0]
        x2 = solution[1]
        max_profit = self.tableau[0, -1]

        return {
            "生产量": {
                "齿轮": x1,
                "轴承": x2
            },
            "最大利润": max_profit,
            "约束条件": {
                "约束1": f"{self.input_data['gear_A']}*x1 + {self.input_data['bearing_A']}*x2 <= {self.input_data['inventory_A']}",
                "约束2": f"{self.input_data['gear_B']}*x1 + {self.input_data['bearing_B']}*x2 <= {self.input_data['inventory_B']}",
                "约束3": "x1 >= 0",
                "约束4": "x2 >= 0"
            }
        }

def LpProblem_solve(input_data):
    try:
        solver = SimplexSolver(input_data)
        return solver.solve()
    except Exception as e:
        print(f"求解错误：{str(e)}")
        return {
            "生产量": {
                "齿轮": "错误",
                "轴承": "错误"
            },
            "最大利润": "错误",
            "约束条件": {
                "约束1": "错误",
                "约束2": "错误",
                "约束3": "错误",
                "约束4": "错误"
            }
        }

if __name__ == "__main__":
    if True:
        # 测试数据
        input_data = {
            'gear_A': 3,
            'gear_B': 2,
            'gear_profit': 120,
            'bearing_A': 1,
            'bearing_B': 4,
            'bearing_profit': 100,
            'inventory_A': 3000,
            'inventory_B': 3000
        }
        result = LpProblem_solve(input_data)
        print("调试结果:", result)
        print(f"生产计划：齿轮 {result['生产量']['齿轮']:.0f} 件，轴承 {result['生产量']['轴承']:.0f} 件")
        print(f"最大利润：{result['最大利润']:.0f} 元")
        print(f"约束条件：{input_data['gear_A']} * x1 + {input_data['bearing_A']} * x2 <= {input_data['inventory_A']};")
        print(f"        {input_data['gear_B']} * x1 + {input_data['bearing_B']} * x2 <= {input_data['inventory_B']};")
        print(f"        x1 >= 0 ; x2 >= 0")
    sys.exit()