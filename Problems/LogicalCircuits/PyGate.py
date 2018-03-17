import time
from GP.Utilities.Node import Node
from GP.Utilities.Tree import Tree
from GP.GP import GP

function_set = [("NAND", 2)]
terminal_set = ["X", "Y"]
depth_range = (3, 4)

pop_init_method = "grow"
pop_size = 10
mutation_rate = 0.15
mutation_methods = ["delete", "change", "add"]
tournament_size = 4
elitism = True

found_solution = False
truth_table = \
    [
        [[0, 0], 0],
        [[0, 1], 1],
        [[1, 0], 1],
        [[1, 1], 0]
    ]

# truth_table = \
#     [
#         [[0, 0, 0], 1],
#         [[0, 0, 1], 0],
#         [[0, 1, 0], 1],
#         [[0, 1, 1], 0],
#         [[1, 0, 0], 1],
#         [[1, 0, 1], 0],
#         [[1, 1, 0], 1],
#         [[1, 1, 1], 1],
#     ]
total_combinations = 2 ** len(terminal_set)

gp = GP(depth_range, function_set, terminal_set, pop_size, tournament_size, mutation_methods, mutation_rate, elitism)
gp.initialize_population(pop_init_method)


def calculate_fitness_for_population(population: list):
    for individual in population:
        calculate_fitness_for_individual(individual)


def __solve_rec(inputs: list, gate: Node) -> int:
    if gate.type is "T":
        index_of_input = terminal_set.index(gate.label)
        return int(inputs[index_of_input])
    else:
        if gate.label is "NOT":
            return not __solve_rec(inputs, gate.children_list[0])
        if gate.label is "AND":
            return __solve_rec(inputs, gate.children_list[0]) and __solve_rec(inputs, gate.children_list[1])
        if gate.label is "OR":
            return __solve_rec(inputs, gate.children_list[0]) or __solve_rec(inputs, gate.children_list[1])
        if gate.label is "NAND":
            return not (__solve_rec(inputs, gate.children_list[0]) and __solve_rec(inputs, gate.children_list[1]))
        if gate.label is "NOR":
            return not (__solve_rec(inputs, gate.children_list[0]) or __solve_rec(inputs, gate.children_list[1]))
        if gate.label is "XOR":
            a = __solve_rec(inputs, gate.children_list[0])
            b = __solve_rec(inputs, gate.children_list[1])
            return ((not a) and b) or ((not b) and a)


def solve_circuit(inputs: list, circuit: Tree) -> int:
    """
    :param circuit:
    :param inputs: list of boolean number for each input (terminal) => [0, 1, 1, 0]
    :return: output of circuit
    """
    return int(__solve_rec(inputs, circuit.root))


def calculate_fitness_for_individual(circuit: Tree):
    global found_solution
    temp_fitness = 0
    for state in truth_table:
        if solve_circuit(state[0], circuit) is state[1]:
            temp_fitness += 1

    if temp_fitness is total_combinations:
        circuit.is_answer = True
        found_solution = True
        input("Found Solution in Generation : {0}".format(gp.generation))

    # temp_fitness /= circuit.depth + 1
    circuit.fitness = temp_fitness


def generate_population_information(population: list):
    average_fitness = 0
    for individual in population:
        average_fitness += individual.fitness
    average_fitness /= gp.population_size
    sorted_pop = sorted(population, key=lambda x: x.fitness)
    best_fitness = sorted_pop[-1].fitness
    worst_fitness = sorted_pop[0].fitness
    sorted_pop.clear()
    print("Generation  {0} : \n\tBest Fitness = {1}\n\tWorst Fitness = {2}\n\tAverage Fitness = {3}\n\n".format(
        gp.generation, best_fitness, worst_fitness, average_fitness
    ))


while True:
    tic = time.time()
    calculate_fitness_for_population(gp.population)
    generate_population_information(gp.population)
    if found_solution:
        gp.render_current_generation("output")
        break
    gp.evolve()
    tac = time.time()
    print(round(tac - tic, 6), " s elapsed")
