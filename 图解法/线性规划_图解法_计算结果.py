'''整数规划问题：计算产品最大利润'''
import sys
from pulp import LpMaximize, LpProblem, LpVariable # pulp库导入（优化目标，问题实例，决策变量）


def LpProblem_solve(input_data):
    try:
        # 初始化线性规划模型（问题名称，优化方向）
        model = LpProblem("产品最大利润", LpMaximize)

        # 定义变量（修改cat可改为线性规划问题）
        x1 = LpVariable("齿轮生产量", lowBound=0, cat="Integer")  # 齿轮生产量（变量名称，变量下限，变量类型）
        x2 = LpVariable("轴承生产量", lowBound=0, cat="Integer")  # 轴承生产量（变量名称，变量下限，变量类型）

        # 定义目标函数
        model += input_data['gear_profit'] * x1 + input_data['bearing_profit'] * x2  # max Z = 120 * x1 + 100 * x2

        # 添加约束条件(“+=” 为添加目标表达式和线性约束的运算符)
        model += input_data['gear_A'] * x1 + input_data['bearing_A'] * x2 <= input_data[
            'inventory_A'], "原材料A"  # 原材料A约束（约束表达式，约束名称）
        model += input_data['gear_B'] * x1 + input_data['bearing_B'] * x2 <= input_data[
            'inventory_B'], "原材料B"  # 原材料B约束（约束表达式，约束名称）

        # 求解模型
        model.solve()

        # 输出结果

        return {
            "生产量": {
                "齿轮": x1.varValue,
                "轴承": x2.varValue
            },
            "最大利润": model.objective.value(),
            "约束条件": {
                "约束1": f"{input_data['gear_A']}*x1 + {input_data['bearing_A']}*x2 <= {input_data['inventory_A']}",
                "约束2": f"{input_data['gear_B']}*x1 + {input_data['bearing_B']}*x2 <= {input_data['inventory_B']}",
                "约束3": "x1 >= 0",
                "约束4": "x2 >= 0"
            }
        }
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
        result = LpProblem_solve(input_data)  # 传入测试数据
        print("调试结果:", result)
        print(
            f"生产计划：齿轮 {result['生产量']['齿轮']:.0f} 件，轴承 {result['生产量']['轴承']:.0f} 件")  # 获取变量 xi 的最优解值
        print(f"最大利润：{result['最大利润']:.0f} 元")  # 获取目标函数的最优值
        print(f"约束条件：{input_data['gear_A']} * x1 + {input_data['bearing_A']} * x2 <= {input_data['inventory_A']};")
        print(f"        {input_data['gear_B']} * x1 + {input_data['bearing_B']} * x2 <= {input_data['inventory_B']};")
        print(f"        x1 >= 0 ; x2 >= 0")
    sys.exit()

