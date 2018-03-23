from GP.Utilities import Node
from GP.Utilities.Tree import Tree
from graphviz import Digraph
from copy import deepcopy
from GP.HyperParameters import HyperParameters as hp
import random


class GP:
    def __init__(self, depth_range: tuple, function_set: list, terminal_set: list, population_size: int,
                 tournament_size: int,
                 mutation_methods: list, mutation_rate: float, elitism: bool):
        """
        :param depth_range: specifies a max depth range for initializing population and controlling depths surpass
        :param function_set: is a list of tuples which hold pairs of [(label , number_of_children)]
        :param terminal_set: is a list of terminal labels like ["X" , "Y" , "Z"]
        :param population_size: size of the population
        :param tournament_size: size of the tournament used for selection
        :param mutation_methods: a list of strings containing different types of mutation methods
        :param mutation_rate: chance of each newly born child in new population which can mutate
        :param elitism: a boolean which reserves a spot in new population for the elite member of last generation
        """

        # region Depth Range
        if depth_range[0] > depth_range[1]:
            raise Exception("Invalid Depth Range, First Value Must Be Smaller Than Second")
        elif depth_range[0] < 2:
            raise Exception("Invalid Depth Range, Minimum Depth is 2")
        else:
            self.depth_range: tuple = depth_range
            self.min_depth = self.depth_range[0]
            self.max_depth = self.depth_range[1]
        # endregion

        # region Population
        self.population: list = []  # list of trees as individuals

        if population_size < 2:
            raise Exception("population size must be greater or equal to 2")
        else:
            self.population_size: int = population_size
        # endregion

        #  region Functions and Terminals
        self.function_set: list = function_set
        self.terminal_set: list = terminal_set
        #  endregion

        # region Selection
        self.tournament_size: int = tournament_size
        self.elitism: bool = elitism
        #  endregion

        #  region Mutation
        self.mutation_algorithms: list = mutation_methods
        self.mutation_rate: float = mutation_rate
        #  endregion

        # region Generation
        self.generation = 0
        # endregion

    """ public functions """

    def initialize_population(self, initialization_method: str, shuffle: bool = True):

        if initialization_method is "full":

            for i in range(self.population_size):
                rand_depth = random.randrange(self.depth_range[0], self.depth_range[1] + 1)
                temp_tree = Tree(rand_depth, self.function_set, self.terminal_set)
                temp_tree.populate_random_tree("full")
                self.population.append(temp_tree)

        elif initialization_method is "grow":

            for i in range(self.population_size):
                rand_depth = random.randrange(self.depth_range[0], self.depth_range[1] + 1)
                temp_tree = Tree(rand_depth, self.function_set, self.terminal_set)
                temp_tree.populate_random_tree("grow")
                self.population.append(temp_tree)

        # ramped (or ramped half and half) is a combination of both "grow" and "full"
        elif initialization_method is "ramped":

            for i in range(0, int(self.population_size / 2)):
                rand_depth = random.randrange(self.depth_range[0], self.depth_range[1] + 1)
                temp_tree = Tree(rand_depth, self.function_set, self.terminal_set)
                temp_tree.populate_random_tree("grow")
                self.population.append(temp_tree)

            for i in range(int(self.population_size / 2), self.population_size):
                rand_depth = random.randrange(self.depth_range[0], self.depth_range[1] + 1)
                temp_tree = Tree(rand_depth, self.function_set, self.terminal_set)
                temp_tree.populate_random_tree("full")
                self.population.append(temp_tree)

        else:
            raise Exception("Invalid Algorithm for initializing population")
        if shuffle:
            random.shuffle(self.population)

    def evolve(self):
        # creating new population
        new_population: list = [None] * self.population_size

        # region elitism handing
        start_index = 0
        if self.elitism:
            start_index = 1
            # finding the most elite member of last generation and sending it directly to new generation
            new_population[0] = deepcopy(max(self.population, key=lambda x: x.fitness))
        # endregion

        for i in range(start_index, self.population_size):
            parent_1, parent_2 = self.__tournament_selection()
            new_population[i] = self.__cross_over(parent_1, parent_2)
            self.mutate(new_population[i])

        self.population = new_population
        self.generation += 1

    def mutate(self, parent: Tree):
        if (self.mutation_algorithms is None) or (self.mutation_algorithms is []):
            return
        elif random.random() > self.mutation_rate:
            return

        rand_mutation_method: str = self.mutation_algorithms[random.randrange(0, self.mutation_algorithms.__len__())]

        # todo not sure about correct names for these types of mutations
        if rand_mutation_method is "delete":  # delete children underneath and attach random terminals to it
            self.__mutate_delete(parent)
        elif rand_mutation_method is "change":  # change the label of the node with respect to its max_num_of_children
            self.__mutate_change(parent)
        elif rand_mutation_method is "add":  # adds a whole new tree as one of its children
            self.__mutate_add(parent)
        elif rand_mutation_method is "exchange":  # change the type (function to terminal and otherwise)
            pass  # todo implement this
        else:
            raise Exception("Invalid Algorithm for Mutation")

        parent.is_mutated = True
        parent.update_tree()
        if parent.depth > self.max_depth:
            parent.reshape_max_depth(self.max_depth)

    def render_current_generation(self, folder_name: str):
        """
        this function render the current generation in PNG format with some extra information
        :param folder_name:
        :return:
        """
        g = Digraph()
        g.format = 'png'
        g.directory = folder_name + "/Generation " + str(self.generation)
        counter = 1

        for tree in self.population:
            g.clear()
            info = '"00_comment_00" [label="G : {0}\nF : {1}\nD : {2}\nW : {3}\nn : {4}" , shape="box" , color="white"]'.format(
                self.generation, tree.fitness, tree.depth, tree.width, tree.number_of_nodes_in_tree
            )
            g.body.append(info)
            g.body.append(tree.print_graph())
            g.render("Individual {0}".format(counter))
            counter += 1

    """ private Functions """

    def __tournament_selection(self):
        temp_tournament: list = []

        while len(temp_tournament) is not self.tournament_size:
            rand_index = random.randrange(0, self.population_size)

            temp_tree: Tree = self.population[rand_index]
            if temp_tree not in temp_tournament:
                temp_tournament.append(temp_tree)

        temp_tournament = sorted(temp_tournament, key=lambda x: x.fitness, reverse=True)

        return deepcopy(temp_tournament[0]), deepcopy(temp_tournament[1])

    def __cross_over(self, parent_1: Tree, parent_2: Tree) -> Tree:
        # getting a random node from parent_2
        temp_node = parent_2.get_random_node().copy()

        # region generating a index range for parent_1
        depth_min_range = hp.GP.cross_over_min_range
        depth_max_range = int(hp.GP.cross_over_min_range_multiplier * parent_1.number_of_nodes_in_tree)
        if depth_min_range >= depth_max_range:
            raise Exception("Invalid Range for crossover replacement : (", depth_min_range, " , ", depth_max_range, ")")

        if depth_max_range is 1:
            depth_max_range += 1
        depth_range = (depth_min_range, depth_max_range)
        # endregion

        parent_1.select_random_node_and_replace(depth_range, temp_node)

        # update and reshape the tree if needed
        parent_1.update_tree()
        if parent_1.depth > self.max_depth:
            parent_1.reshape_max_depth(self.max_depth)
        return parent_1

    def __mutate_delete(self, parent: Tree):
        rand_node_index = random.randrange(0, parent.number_of_nodes_in_tree)
        temp_node: Node = parent.get_node(rand_node_index)

        if temp_node is None:
            raise Exception("Invalid Node Index")
        while temp_node.type is "T":
            rand_node_index = random.randrange(0, parent.number_of_nodes_in_tree)
            temp_node = parent.get_node(rand_node_index)

        for i in range(temp_node.max_num_of_children):
            temp_node.children_list[i] = parent.generate_random_terminal()

    def __mutate_change(self, parent: Tree):
        rand_node_index = random.randrange(0, parent.number_of_nodes_in_tree)
        temp_node: Node = parent.get_node(rand_node_index)

        # make sure excluding current terminal won't break our lovely program
        if (temp_node.type is "T") and (self.terminal_set.__len__() > 1):
            temp_remaining_terminals = [t for t in self.terminal_set if t is not temp_node.label]
            temp_node.label = temp_remaining_terminals[random.randrange(0, temp_remaining_terminals.__len__())]
        if (temp_node.type is "F") and (self.function_set.__len__() > 1):
            # generating a list of tuples from remaining function excluding current function label
            temp_remaining_functions = [
                f_tpl[0] for f_tpl in self.function_set
                if (f_tpl[0] is not temp_node.label) and (f_tpl[1] is temp_node.max_num_of_children)
            ]
            if temp_remaining_functions.__len__() > 0:
                temp_node.label = temp_remaining_functions[random.randrange(0, temp_remaining_functions.__len__())]

    def __mutate_add(self, parent: Tree):
        rand_node_index = random.randrange(1, parent.number_of_nodes_in_tree)
        temp_node: Node = parent.get_node(rand_node_index)

        while temp_node.type is "T":
            rand_node_index = random.randrange(0, parent.number_of_nodes_in_tree)
            temp_node: Node = parent.get_node(rand_node_index)

        final_depth = parent.depth if hp.GP.mutate_add_depth < 2 else hp.GP.mutate_add_depth
        temp_tree = Tree(final_depth, self.function_set, self.terminal_set)
        temp_tree.populate_random_tree(["grow", "full"].__getitem__(random.randrange(0, 2)))
        temp_node.children_list[random.randrange(0, temp_node.max_num_of_children)] = temp_tree.root

    def __mutate_exchange(self, parent: Tree):
        pass
