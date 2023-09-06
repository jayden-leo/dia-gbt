import matplotlib.pyplot as plt
import numpy as np

# 任务和指标的标签
tasks = ['Cooking', 'Logistics', 'Assembly', 'Cleaning']
indicators = ['Parse_sep', 'Plausible_sep', 'Parse_conti', 'Plausible_conti']
"""
# penguin_means = {
#     'Parse_sep': (1054, 1090, 1129, 1188),
#     'Parse_conti': (1054, 1087, 1130, 1185),
#     'Plausible_sep': (843, 912, 1052, 1090),
#     'Plausible_conti': (843, 907, 1030, 1041)
"""
# 模拟数据（示例数据）
data = [
    [1054, 1090, 1129, 1188],
    [843, 912, 1052, 1042],
    [0, 1059, 1053, 1153],
    [0, 874, 1013, 1022]
]

data_percent = [
    [98.04, 98.82, 98.08, 99.66],
    [78.41, 82.68, 91.39, 87.42],
    [0, 96.01, 91.48, 96.72],
    [0, 79.23, 88.01, 85.74]
]

# 设置图表的尺寸
plt.figure(figsize=(8, 5))

# 绘制柱状图
for i in range(len(indicators)):
    plt.bar(np.arange(len(tasks)) + i * 0.2, data[i], width=0.15, label=indicators[i])

# 添加标签和标题

y_ticks = np.linspace(0, 1600, 11)
plt.yticks(y_ticks)
plt.ylabel('Number of Training Instructions')
plt.xticks(np.arange(len(tasks)) + 0.2 * (len(indicators) - 1) / 2, tasks)
plt.legend()

# 在每个柱子上标注百分比
for i in range(len(indicators)):
    for j in range(len(tasks)):
        if j == 0:
            if i == 2 or i == 3:
                continue
        plt.text(j + i * 0.2, data[i][j] + 10, f'{data_percent[i][j]:.1f}%', ha='center', fontsize=8)
# 设置图例在左上方
plt.legend(loc='upper left')
# 显示图表
plt.show()
