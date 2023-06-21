import numpy as np
import csv

def weight_function(individual,weights):
    fitness_w = sum(weight * value for weight, value in zip(weights, individual))
    return fitness_w

def read_csv_columns_f(file_path, f_prefix):
    data = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        f_columns = [header for header in headers if header.startswith(f_prefix)]
        for f_column in f_columns:
            data[f_column] = []
            csvfile.seek(0)  # 将文件指针移动到表头的位置
            next(reader)  # 跳过表头行
            for row in reader:
                data[f_column].append(row[f_column])
    return data

def read_csv_columns_tx(file_path, columns):
    data = {column: [] for column in columns}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for column in columns:
                data[column].append(row[column])
    return data

# 适应度函数示例，假设为最小化问题
def fitness(csv_file,b, k, m):
    # 计算适应度值，根据具体问题定义

    # 示例文件路径、F 列的前缀和 T、X 列的表头
    f_prefix = 'F'
    tx_headers = ['T', 'X']

    # 读取 F 列和 T、X 列数据
    data_f= read_csv_columns_f(csv_file, f_prefix)
    data_tx = read_csv_columns_tx(csv_file, tx_headers)

    RC_j = []  # 存放每个样品对应的RC
    E_j = []  # 存放每个样品的误差
    j = 0
    for key, value in data_f.items():
        bj = b[j]
        kj = k[j]
        mj = m[j]
        # 再遍历F1的每一个值,i
        RC_i = []  # 存放每个因子对应的RC
        x_sum = 0
        for i, data in enumerate(value):
            x = float(data_tx['X'][i])
            t = float(data_tx['T'][i])
            # 计算每个因子对应的BC
            BC = float(data) * bj
            # 计算每个因子对应的MC
            MC = BC * mj * (1 - np.exp(-kj * t))
            # 计算每个因子对应的RC
            RC = BC - MC
            RC_i.append(RC)
            x_sum=x_sum+x
        # 计算每个因子的权重
        '''
        weight = []
        sum_RC=sum(RC_i)
        for num in X:
            weight.append(float(num) / x_sum)
        # 计算每个样品的RC
        RC_i_weight=weight_function(RC_i,weight)
        RC_j.append(RC_i_weight)
        '''
        RC_j.append(sum(RC_i))
        # 计算每个样品的误差
        #E_j.append(((RC_j[j] - x )/ x) ** 2)
        E_j.append(abs((RC_j[j] - x_sum)))
        # 计算所有样品总的误差
        E = sum(E_j)
        j = j + 1
    return E

def compute_formula(csv_file, b, k, m):
    # 计算适应度值，根据具体问题定义

    # 示例文件路径、F 列的前缀和 T、X 列的表头
    f_prefix = 'F'
    tx_headers = ['T', 'X']

    # 读取 F 列和 T、X 列数据
    data_f = read_csv_columns_f(csv_file, f_prefix)
    data_tx = read_csv_columns_tx(csv_file, tx_headers)

    RC_j = []  # 存放每个样品对应的RC
    RC_j_list = []  # 存放计算的RC lis
    j = 0
    for key, value in data_f.items():
        bj = b[j]
        kj = k[j]
        mj = m[j]
        # 再遍历F1的每一个值,i
        RC_i = []  # 存放每个因子对应的RC

        for i, data in enumerate(value):
            x = float(data_tx['X'][i])
            t = float(data_tx['T'][i])
            # 计算每个因子对应的BC
            BC = float(data) * bj
            # 计算每个因子对应的MC
            MC = BC * mj * (1 - np.exp(-kj * t))
            # 计算每个因子对应的RC
            RC = BC - MC
            RC_i.append(RC)
        # 计算每个样品的RC
        RC_j.append(sum(RC_i))
        RC_j_list.append(RC_i)
    return data_tx['X'],RC_j_list
