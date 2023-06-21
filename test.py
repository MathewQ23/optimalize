from meta_genetic_algorithm import genetic_algorithm
from optimize import compute_formula
import csv
from skopt import gp_minimize
from skopt.space import Real
from optimize import  fitness
def write_csv(file_path, columns, data):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        max_len = max(len(col_data) for col_data in data)
        for i in range(max_len):
            row = []
            for col_data in data:
                if i < len(col_data):
                    row.append(col_data[i])
                else:
                    row.append("")
            writer.writerow(row)


if __name__ == "__main__":
    file_path='data1.csv' #数据文件
    result_path='result.csv' #结果验证文件
    parameter_path = 'output.csv'  # 参数文件
    # 列名
    columns = ['b', 'k', 'm']
    data = {col: [] for col in columns}

    with open(parameter_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for col in columns:
                data[col].append(float(row[col]))

    best_b=data['b']
    best_k=data['k']
    best_m=data['m']
    X,RC=compute_formula(file_path,best_b, best_k, best_m)

    # 指定要写入的文件路径


    # 将多个列表打包成一个元组的列表
    data = list(zip(best_b, best_k, best_m))

    # 打开文件，使用 'w' 模式表示写入模式
    with open(parameter_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['b', 'k', 'm'])  # 写入表头
        writer.writerows(data)  # 写入数据

    header = ['X', 'RC1', 'RC2', 'RC3']
    # 组合数据
    data_x = [X] + RC
    # 写入 CSV 文件
    write_csv(result_path, header, data_x)
    print("结果验证已写入到文件:", result_path)
    # space = [Real(low=0.0, high=10.0, name='b'),
    #          Real(low=-0.0, high=10.0, name='k'),
    #          Real(low=0.0, high=1.0, name='m')]
    # res = gp_minimize(fitness, space, n_calls=10)  # n_calls指定迭代次数
    #
    # # 打印最优解和最优值
    # print("Best solution: ", res.x)
    # print("Best value: ", res.fun)
