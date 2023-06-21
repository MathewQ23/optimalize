from meta_genetic_algorithm import genetic_algorithm
from optimize import compute_formula
import csv


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
    file_path='data.csv' #数据文件
    result_path='result.csv' #结果验证文件
    parameter_path = 'output.csv'  # 参数文件
    population_size = 1000  # 种群大小
    max_generations = 10 # 最大迭代次数
    best_b, best_k, best_m, best_fitness = genetic_algorithm(file_path,population_size,max_generations)
    X,RC=compute_formula(file_path,best_b, best_k, best_m)

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
    print("参数已写入到文件:", parameter_path)
    print("Best value for b:", best_b)
    print("Best value for k:", best_k)
    print("Best value for m:", best_m)
    print("Best fitness:", best_fitness)
    print("RC:",RC)
    print("X:",X)
