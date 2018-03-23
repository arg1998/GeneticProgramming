class HyperParameters:
    class GP:
        """
        HyperParameters settings for GP class
        """

        """
        in normal cross_over , these values are used to create a range between 0 and num_of_nodes_in_tree
        
        NOTE:cross_over_min_range is a integer number , be careful with choosing the right number. because it can pass 
             the num_of_nodes_in_tree and break the program
             
        NOTE:cross_over_min_range_multiplier is a float between 0 (0 itself is excluded) and 1 which gets multiplied 
             by num_of_nodes_in_tree
             
        combination of these will result in a range which our crossover function can select a random node in this range
        and do the replacement 
        """
        cross_over_min_range: int = 1
        cross_over_min_range_multiplier: float = 0.8

        """
        this variable controls the depth of the new branch which is going to be added as an add_mutation 
        inside the GP.__mutate_add() method
        
        the default value is less than 2 (because minimum depth for tree is 2) which the function will automatically select the parent's depth 
        for new branch's. 
        otherwise, the new value will be the final_depth for our new branch
        """
        mutate_add_depth: int = 0

    class Tree:
        """
        this variable determines the probability of selecting weather a function or a terminal
        """
        populate_grow_probability: float = 0.65
