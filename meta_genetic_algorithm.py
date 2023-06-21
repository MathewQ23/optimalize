import random
from optimize import fitness


# 遗传算法求解参数
def genetic_algorithm(csv_path, population_size, max_generations):
    mutation_rate = 0.6  # 变异率
    b_min = 0
    b_max = 10
    k_min = 0
    k_max = 10
    m_min = 0
    m_max = 1

    # 初始化种群
    population = []
    for _ in range(population_size):
        b = [random.uniform(b_min, b_max), random.uniform(b_min, b_max), random.uniform(b_min, b_max)]  # 选择b的取值
        k = [random.uniform(k_min, k_max), random.uniform(k_min, k_max), random.uniform(k_min, k_max)]  # 选择k的取值
        m = [random.uniform(m_min, m_max), random.uniform(m_min, m_max), random.uniform(m_min, m_max)]  # 选择m的取值
        individual = (b, k, m)
        population.append(individual)

    # 迭代优化
    for generation in range(max_generations):
        # 计算种群中每个个体的适应度值
        fitness_values = [fitness(csv_path, b, k, m) for b, k, m in population]

        # 选择操作，选择适应度较好的个体
        selected_population = []
        for _ in range(population_size):
            # 轮盘赌选择，根据适应度值进行选择
            fitness_inverse = [1 / fitness_value for fitness_value in fitness_values]
            selected_individual = random.choices(population, weights=fitness_inverse)[0]
            selected_population.append(selected_individual)

        # 交叉操作，生成新的个体
        offspring_population = []
        for _ in range(population_size):
            parent1, parent2 = random.choices(selected_population, k=2)
            offspring = (
                parent1[0] if random.random() < 0.5 else parent2[0],  # 交叉操作对b进行交叉
                parent1[1] if random.random() < 0.5 else parent2[1],  # 交叉操作对k进行交叉
                parent1[2] if random.random() < 0.5 else parent2[2]  # 交叉操作对m进行交叉
            )
            offspring_population.append(offspring)

        # 变异操作
        for i in range(population_size):
            if random.random() < mutation_rate:
                # 随机选择一个参数进行变异，假设在[0, 1]范围内进行变异
                offspring_population[i] = (
                    [random.random() for _ in range(3)],  # 生成三个新的随机值作为b的新取值
                    [random.random() for _ in range(3)],  # 生成三个新的随机值作为k的新取值
                    [random.random() for _ in range(3)]  # 生成三个新的随机值作为m的新取值
                )
        # 更新种群
        population = offspring_population

        # 找到最优解
        best_fitness = min(fitness_values)
        # print("变异后------------------")
        print("Generation:", generation)
        print("Best fitness:", best_fitness)
        print("------------------")

    # 选择最优解
    best_individual = min(population, key=lambda x: fitness(csv_path, x[0], x[1], x[2]))
    best_b, best_k, best_m = best_individual
    final_best_fitness = fitness(csv_path, best_b, best_k, best_m)
    print("Final best fitness:", final_best_fitness)

    return best_b, best_k, best_m, final_best_fitness
