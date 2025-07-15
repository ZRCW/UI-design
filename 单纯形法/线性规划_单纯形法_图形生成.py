'''单纯形法迭代过程可视化'''
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pulp import LpProblem, LpVariable, LpMaximize

def LpProblem_solve_plot(input_data):
    # 创建问题实例
    model = LpProblem("Product_Profit_Maximization", LpMaximize)
    x1 = LpVariable("Gear", lowBound=0, cat="Integer")  # 齿轮
    x2 = LpVariable("Bearing", lowBound=0, cat="Integer")  # 轴承

    # 目标函数和约束
    model += input_data['gear_profit'] * x1 + input_data['bearing_profit'] * x2
    model += input_data['gear_A'] * x1 + input_data['bearing_A'] * x2 <= input_data['inventory_A']
    model += input_data['gear_B'] * x1 + input_data['bearing_B'] * x2 <= input_data['inventory_B']

    # 求解模型
    model.solve()

    # 绘制图形
    plt.figure(figsize=(12, 8))

    # 约束线
    x = np.linspace(0, 1500, 500)
    y1 = (-input_data['gear_A'] * x + input_data['inventory_A']) / input_data['bearing_A']
    y2 = (-input_data['gear_B'] * x + input_data['inventory_B']) / input_data['bearing_B']

    plt.plot(x, y1, label=f"{input_data['gear_A']}x1 + {input_data['bearing_A']}x2 ≤ {input_data['inventory_A']}", color='blue')
    plt.plot(x, y2, label=f"{input_data['gear_B']}x1 + {input_data['bearing_B']}x2 ≤ {input_data['inventory_B']}", color='green')

    # 可行域
    y_feasible = np.minimum(y1, y2)
    plt.fill_between(x, 0, y_feasible, where=(y_feasible >= 0), color='gray', alpha=0.3, label='Feasible Region')

    # 标注顶点
    vertices = []
    # 原点
    if 0 <= input_data['inventory_A'] and 0 <= input_data['inventory_B']:
        vertices.append((0, 0))
    # x1轴交点
    x1_max = min(input_data['inventory_A'] / input_data['gear_A'], input_data['inventory_B'] / input_data['gear_B'])
    if x1_max > 0:
        vertices.append((x1_max, 0))
    # x2轴交点
    x2_max = min(input_data['inventory_A'] / input_data['bearing_A'], input_data['inventory_B'] / input_data['bearing_B'])
    if x2_max > 0:
        vertices.append((0, x2_max))
    # 两约束的交点
    A = np.array([
        [input_data['gear_A'], input_data['bearing_A']],
        [input_data['gear_B'], input_data['bearing_B']]
    ])
    b = np.array([input_data['inventory_A'], input_data['inventory_B']])
    try:
        solution = np.linalg.solve(A, b)
        if solution[0] >= 0 and solution[1] >= 0:
            vertices.append(tuple(solution))
    except np.linalg.LinAlgError:
        pass

    # 绘制顶点
    for vertex in vertices:
        plt.scatter(vertex[0], vertex[1], color='red', s=100)
        plt.text(vertex[0], vertex[1], f'({vertex[0]:.0f}, {vertex[1]:.0f})', fontsize=10)

    # 最优解
    optimal_x1 = x1.varValue
    optimal_x2 = x2.varValue
    plt.scatter(optimal_x1, optimal_x2, color='gold', s=150, marker='*',
               label=f'Optimal Solution ({optimal_x1:.0f}, {optimal_x2:.0f})')

    # 图形设置
    plt.xlim(0, max(1200, optimal_x1 * 1.2))
    plt.ylim(0, max(1200, optimal_x2 * 1.2))
    plt.xlabel("Gear Production (x1)")
    plt.ylabel("Bearing Production (x2)")
    plt.title("Simplex Method Visualization\n(Feasible Region and Vertices)")
    plt.grid(True)
    plt.legend()

    # 保存图像
    plt.savefig("线性规划_单纯形法_图像.png")
    return "线性规划_单纯形法_图像.png"

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
        print(f"图像路径: {LpProblem_solve_plot(input_data)}")
        plt.show()
    sys.exit()