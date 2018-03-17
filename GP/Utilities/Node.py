import copy


class Node:
    """ this class represent a gene in the solution tree for each individual"""

    def __init__(self, children: list, max_num_of_children: int, node_type: str, label: str, value: object,
                 index_id: int = None, parent=None):
        """
            children :list of Nodes that are below this node as of its childes
            num_of_children :number of children for this Node
            type : defines the type of the Node => function "F" or terminal "T"
            label : is a string that defines the functionality of this Node
            value : holds a value if necessary
            index_ID : assign a unique ID for this Node
            parent : mark the parent of this Node
        """

        if children is None or children is []:
            self.children_list: list = [None] * max_num_of_children
        else:
            self.children_list: list = children

        self.max_num_of_children: int = max_num_of_children
        self.type: str = node_type
        self.label: str = label
        self.value = value
        self.index_id: int = index_id
        self.parent: Node = parent

    def copy(self):
        """
        return a deepCopied of current Node
        :return: Node
        """
        return copy.deepcopy(self)

    def depth(self) -> int:
        """
        calculate the depth of the tree recursively (indirect)
        :return: an integer for depth
        """

        current_depth = 0

        if self.children_list is not None:
            for i in range(len(self.children_list)):
                if (self.children_list[i] is not None) and (self.children_list[i] is not []):
                    current_depth = max(current_depth, self.children_list[i].depth())

        return current_depth + 1
