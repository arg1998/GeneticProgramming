from GP.Utilities.Node import Node
import random
import queue


class Tree:
    """
    this class is representing an individual
    """

    def __init__(self, depth: int, function_set: list, terminal_set: list, root: Node = None):
        """
        :param depth: tha maximum depth of the tree
        :param function_set: is a list of tuples which hold pairs of [(label , number_of_children)]
        :param terminal_set: is a list of terminal labels like ["left" , "right" , "stay"]
        """

        if depth < 2:
            raise Exception("minimum value for depth is 2")
        self.depth = depth
        self.width = 0
        self.terminal_set = terminal_set
        self.functions = function_set
        self.root = root
        self.number_of_nodes_in_tree = 0
        self.fitness: float = 0.0
        self.is_answer: bool = False
        self.is_mutated: bool = False

        """"  private vars """
        # this list keeps track of random terminal and makes sure that all terminals are included at the beginning
        # because of randomness effect , we can miss a terminal , so we should keep an eye on non-included terminals
        self.__temp_terminals: list = []  # todo might break at some situations, find and fix them

    """public functions"""

    def generate_random_function(self) -> Node:
        """
        this function generates a random node with type of "F" and a random label from self.functions
        :return: a randomly generated function node with empty children_list
        """
        # rand_label is a tuple (node_label , number_of_children)
        rand_label = self.functions[random.randrange(0, len(self.functions))]
        return Node(None, rand_label[1], "F", rand_label[0], None, -1)

    def generate_random_terminal(self) -> Node:
        """
        this function generates a random node with type of "T" and a random label from self.terminals
        :return: a randomly generated terminal node
        """
        # each of terminal has been chosen at least one time so with the help of self.__temp_terminals
        # we can assure that for N (N = length of terminal_set) random selection , all terminals get included
        # and for [N + k]'th random selection, we are totally free to choose among all terminals

        if len(self.__temp_terminals) is len(self.terminal_set):
            # rand_label is a string containing a random terminal label
            rand_terminal = self.terminal_set[random.randrange(0, len(self.terminal_set))]
            return Node(None, 0, "T", rand_terminal, None, -1)
        else:
            while True:
                rand_terminal = self.terminal_set[random.randrange(0, len(self.terminal_set))]

                if rand_terminal in self.__temp_terminals:
                    continue
                else:
                    self.__temp_terminals.append(rand_terminal)
                return Node(None, 0, "T", rand_terminal, None, -1)

    def calculate_depth(self) -> int:
        """ calculate depth of the tree from starting at root node """
        self.depth = 0 if self.root is None else self.root.depth()
        return self.depth

    def calculate_width(self) -> int:
        """ calculates the width of each level and return the maximum one which is denoted as width of the tree"""
        __height: int = self.root.depth()  # finding how many levels we have
        __width_of_each_level: list = [0] * __height  # generating a list for holding each level's width
        self.__calculate_width(self.root, __width_of_each_level, 0)
        self.width = max(__width_of_each_level)  # selecting the maximum width for our purpose
        return self.width

    def populate_random_tree(self, method: str):
        """
        this function populate our tree randomly with tow different methods
        :param method: "full" a full tree which has (2^depth)-1 nodes , "grow" which is a randomly positioned tree
        :return:
        """
        if self.depth < 2:
            raise Exception("minimum depth for creating tree is 2")

        else:
            if self.root is None:
                self.root = self.generate_random_function()

            if method is "full":
                self.__populate_full_tree(self.root, 1)
            elif method is "grow":
                self.__populate_grow_tree(self.root, 1)
        # update information of the tree
        self.update_tree()

    def print_graph(self) -> str:
        """
        this functions generates a string which we can feed it to GraphViz Library
        to draw this tree
        :return:
        """
        if self.root is not None:
            return self.__print_graph()

    def update_tree(self):
        """
        this function will zero out all properties and recalculates them
        :return:
        """
        self.number_of_nodes_in_tree = 0
        self.depth = 0
        self.width = 0

        self.__update_index_ids()
        self.calculate_width()
        self.calculate_depth()

    def get_random_node(self) -> Node:
        """
        this function returns a random node with level-order traversal in our tree
        :return:
        """
        rnd_num = random.randrange(1, self.number_of_nodes_in_tree, 1)

        if self.root is not None:
            q = queue.Queue()
            q.put(self.root)

            while True:

                if q.empty():
                    break

                while q.qsize() > 0:
                    temp_node: Node = q.get()
                    if temp_node.index_id is rnd_num:
                        return temp_node

                    if temp_node.children_list is not None:
                        for i in range(len(temp_node.children_list)):
                            q.put(temp_node.children_list[i])
        else:
            return None

    def select_and_replace_node(self, rand_range: tuple, node: Node):
        """
        this function replaces a node with a randomly selected node
        :param rand_range: specifies the range of random number which can be from (0 to number_of_nodes_in_tree)
        :param node: the new Node to be replaced with old selected Node
        :return:
        """
        rnd_num = random.randrange(rand_range[0], rand_range[1], 1)
        self.__replace_node(rnd_num, self.root, node)

    def reshape_max_depth(self, new_depth: int):
        """
        this functions can perform branch-cutting if depth of the tree goes higher than max_depth
        all depth-crossed Nodes get deleted and replaced by a terminal in last level
        :param new_depth: the new depth to reshape the tree
        :return:
        """
        self.__temp_terminals.clear()
        self.__reshape_depth(self.root, 1, new_depth)
        self.update_tree()

    def get_node(self, level_order_index_id: int) -> Node:
        """
        this function returns a node by index , it uses level-order tree traversal
        :param level_order_index_id: target index
        :return: a node with given index or None if it doesn't exist
        """

        if level_order_index_id > self.number_of_nodes_in_tree:
            return None

        if self.root is not None:
            q = queue.Queue()
            q.put(self.root)

            while True:

                if q.empty():
                    break

                while q.qsize() > 0:
                    temp_node: Node = q.get()
                    if temp_node.index_id is level_order_index_id:
                        return temp_node

                    if temp_node.children_list is not None:
                        for i in range(len(temp_node.children_list)):
                            q.put(temp_node.children_list[i])
        else:
            return None

    """ private functions """

    def __populate_grow_tree(self, parent_node: Node, current_depth: int):
        """
        this function decides weather add a node by 65 percent chance or not
        it perform this action recursively
        :param parent_node:
        :param current_depth:
        :return:
        """
        # add terminal for the last level
        if current_depth is self.depth - 1:
            for i in range(parent_node.max_num_of_children):
                parent_node.children_list[i] = self.generate_random_terminal()

        # select weather add a function or a terminal
        else:
            for i in range(parent_node.max_num_of_children):
                # add a function
                if random.random() < 0.65:  # todo hardCoded hyperparameter
                    parent_node.children_list[i] = self.generate_random_function()
                    self.__populate_grow_tree(parent_node.children_list[i], current_depth + 1)
                else:
                    parent_node.children_list[i] = self.generate_random_terminal()

    def __populate_full_tree(self, parent_node: Node, current_depth: int):
        """
        this function populates a Full tree recursively
        :param parent_node:
        :param current_depth:
        :return:
        """

        # add terminal for the last level
        if current_depth is self.depth - 1:
            for i in range(parent_node.max_num_of_children):
                parent_node.children_list[i] = self.generate_random_terminal()

        # only add functions
        else:
            for i in range(parent_node.max_num_of_children):
                parent_node.children_list[i] = self.generate_random_function()
                self.__populate_full_tree(parent_node.children_list[i], current_depth + 1)

    def __print_graph(self) -> str:
        result: str = ""
        if self.root is not None:
            q = queue.Queue()
            q.put(self.root)

            while True:
                if q.empty():
                    break
                while q.qsize() > 0:
                    temp_node: Node = q.get()

                    for i in range(len(temp_node.children_list)):
                        if temp_node.children_list[i] is None:
                            continue
                        result += '"{0}_{1}" -> "{2}_{3}";\n"{0}_{1}" [label="{4}"];\n"{2}_{3}" [label="{5}"];\n' \
                            .format(
                                temp_node.index_id, temp_node.label,
                                temp_node.children_list[i].index_id, temp_node.children_list[i].label,
                                temp_node.label,
                                temp_node.children_list[i].label
                            )
                        if temp_node.children_list[i].type is "T":
                            result += '"{0}_{1}" [shape="box"];\n' \
                                .format(
                                temp_node.children_list[i].index_id,
                                temp_node.children_list[i].label
                            )

                    if temp_node.children_list is not None:
                        for i in range(len(temp_node.children_list)):
                            q.put(temp_node.children_list[i])
            return result

        else:
            return result

    def __update_index_ids(self):
        if self.root is not None:
            inc = 0
            q = queue.Queue()
            q.put(self.root)

            while True:

                if q.empty():
                    break

                while q.qsize() > 0:
                    temp_node: Node = q.get()
                    temp_node.index_id = inc
                    self.number_of_nodes_in_tree += 1
                    inc += 1

                    if temp_node.children_list is not None:
                        for i in range(len(temp_node.children_list)):
                            q.put(temp_node.children_list[i])

    def __calculate_width(self, node: Node, widths: list, current_level: int):
        if node is not None:
            for i in range(node.max_num_of_children):
                widths[current_level] += 1
                self.__calculate_width(node.children_list[i], widths, current_level + 1)

    def __reshape_depth(self, parent_node: Node, current_depth: int, new_depth: int):
        if (parent_node.type is "T") and (parent_node.label not in self.__temp_terminals):
            self.__temp_terminals.append(parent_node.label)

        elif current_depth is new_depth - 1:
            for i in range(parent_node.max_num_of_children):
                if parent_node.children_list[i].type is "T":
                    if parent_node.children_list[i].label in self.__temp_terminals:
                        continue
                    else:
                        self.__temp_terminals.append(parent_node.children_list[i].label)
                else:
                    parent_node.children_list[i] = self.generate_random_terminal()

        else:
            for node in parent_node.children_list:
                if node is not None:
                    self.__reshape_depth(node, current_depth + 1, new_depth)

    def __replace_node(self, node_index: int, current_node: Node, new_node: Node):
        if current_node is None:
            return
        else:
            for i in range(current_node.max_num_of_children):
                if current_node.children_list[i].index_id is node_index:
                    current_node.children_list[i] = new_node
                    break
                else:
                    self.__replace_node(node_index, current_node.children_list[i], new_node)
