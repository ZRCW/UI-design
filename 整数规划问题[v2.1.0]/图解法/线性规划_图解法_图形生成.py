'''绘制图形'''
import sys
import numpy as np
import matplotlib.pyplot as plt
from pulp import LpProblem, LpVariable, LpMaximize


def LpProblem_solve_plot(input_data):
    model = LpProblem("Product_Profit_Maximization", LpMaximize)
    x1 = LpVariable("Gear", lowBound=0, cat="Integer")  # 齿轮
    x2 = LpVariable("Bearing", lowBound=0, cat="Integer")  # 轴承

    # 目标函数和约束
    model += input_data['gear_profit'] * x1 + input_data['bearing_profit'] * x2
    model += input_data['gear_A'] * x1 + input_data['bearing_A'] * x2 <= input_data['inventory_A']  # 原材料A
    model += input_data['gear_B'] * x1 + input_data['bearing_B'] * x2 <= input_data['inventory_B']  # 原材料B

    # 求解模型（获取可行解范围）
    model.solve()

    # 绘制约束条件
    x = np.linspace(0, 1500, 500)

    # 约束1: 3x1 + x2 <= 3000 → x2 <= -3x1 + 3000
    y1 = -input_data['gear_A']/input_data['bearing_A'] * x + input_data['inventory_A']/input_data['bearing_A']

    # 约束2: 2x1 + 4x2 <= 3000 → x2 <= -0.5x1 + 750
    y2 = -input_data['gear_B']/input_data['bearing_B'] * x + input_data['inventory_B']/input_data['bearing_B']

    # 坐标轴和约束线
    plt.figure(figsize=(10, 6))
    plt.plot(x, y1, label=f"{input_data['gear_A']}*x1 + {input_data['bearing_A']}*x2 ≤ {input_data['inventory_A']} (A)", color="blue")
    plt.plot(x, y2, label=f"{input_data['gear_B']}*x1 + {input_data['bearing_B']}*x2 ≤ {input_data['inventory_B']} (B)", color="green")

    # 可行解区域填充
    y_feasible = np.minimum(y1, y2)
    plt.fill_between(x, 0, y_feasible, where=(y_feasible >= 0), color="gray", alpha=0.3, label="Feasible domain")

    # 标注最优解点
    optimal_x1 = x1.varValue
    optimal_x2 = x2.varValue
    plt.scatter(optimal_x1, optimal_x2, color="red", label=f"Optimal solution({optimal_x1:.0f}, {optimal_x2:.0f})")

    # 图形设置
    plt.xlim(0, 1200)
    plt.ylim(0, 1200)
    plt.xlabel("gear production (x1)")
    plt.ylabel("bearing production (x2)")
    plt.title(f"LpProblem_solve_plot\n(Product_Profit_Maximization: {input_data['gear_profit']}*x1 + {input_data['bearing_profit']}*x2)")
    plt.grid(True)
    plt.legend()
    plt.savefig("线性规划_图解法_图像.png")  # 保存图像

    # 返回图片
    image_route = "线性规划_图解法_图像.png"
    return image_route


if __name__ == "__main__":
    if False:
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
        print(f"相对路径：{LpProblem_solve_plot(input_data)}")
        plt.show()
    sys.exit()
