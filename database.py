from collections import deque
from copy import deepcopy


class Database(object):
    """
    In Database we will have two Model object that will
    contain the information of current version and the
    version at the moment of add_extract function.
    Once the function get_extract_status is called we
    will compare two versions and return for each image
    the result: 'valid', 'invalid', 'granularity_staged' and 'coverage_staged'
    """

    def __init__(self, first_element):

        # at first we create a cur_version Model object
        self.cur_version = Model(first_element)

        # below information is not initialized yet
        self.extract_information = None
        self.extract_version = None

    def add_nodes(self, nodes):

        # here we add new nodes through Model class add_nodes method
        self.cur_version.add_nodes(nodes)

    def add_extract(self, image_dict):

        # extract_information firstly checked if it's valid or invalid
        # if it's valid so we don't change the value
        # if not we change it to 'invalid'
        self.extract_information = self.cur_version.extract_valid(image_dict)

        # here we save the cur_version to extract_version to compare them later
        # we need to create a deepcopy of the object in order to have an independent copy
        self.extract_version = deepcopy(self.cur_version)

    def get_extract_status(self):

        # iterate over images
        for image, nodes in self.extract_information.items():

            # check if valid
            if nodes != 'invalid':

                # iterate over each node in nodes
                granular = False
                coverage = False
                for node in nodes:

                    # check if cur_version and extracted one have different number of direct child nodes at
                    # that particular node - Granularity condition
                    if self.cur_version.get_number_of_child_nodes(
                            node) != self.extract_version.get_number_of_child_nodes(node):
                        granular = True

                    # check if parent nodes of cur_version and extracted have the same number of nodes
                    # Coverage condition (stronger than granularity)
                    # Could be only if node has a parent
                    if node != self.cur_version.root:
                        if self.cur_version.get_number_of_parent_child_nodes(
                                node) != self.extract_version.get_number_of_parent_child_nodes(node):
                            granular = True
                            coverage = True
                            break

                # final check coverage is more important than granular
                if granular:
                    if coverage:
                        self.extract_information[image] = 'coverage_staged'
                    else:
                        self.extract_information[image] = 'granularity_staged'
                else:
                    self.extract_information[image] = 'valid'

        return self.extract_information


class Model(object):
    """
    Model class represent a directed graph
    """

    def __init__(self, first_element):

        # here we initialize Model class with first_element
        # we represent the directed graph structure by using dictionary
        # key - parent node, list of values - child nodes
        # in order not to have any problems with None key values
        # we create another variable to know the root
        self.root = first_element
        self.graph = {self.root: []}

        # image_pairs variable used in extract_valid function
        self.image_pairs = {}

        # reversed is a place to save a reversed graph
        # it will be used in get_number_of_parent_child_nodes function
        self.reversed = None

    def add_nodes(self, nodes):
        # we will add new nodes by using BFS search firstly we need to find the parent node
        # and then add a new child node in our case we have a dict structure so
        # we can use this as an advantage and implement search and insert much easily

        # iterate over pairs of child and parent nodes
        for node in nodes:

            # check if it's a root node
            if node[1] == self.root:
                self.graph[self.root].append(node[0])
            else:

                # check if parent node is already in the graph
                if node[1] in self.graph:

                    # add the value to the list
                    self.graph[node[1]].append(node[0])

                # if parent is not in keys it must be in leafs we suppose here that parent is valid it must be in
                # keys or in leafs so here we need to simply add a new element to our  dictionary
                else:
                    self.graph[node[1]] = [node[0]]

    def extract_valid(self, image_dict):
        # here we check if the values that want to be extracted are correct (valid)
        for image in image_dict:

            # we can have multiply categories for one image
            for category in image_dict[image]:

                # here we check if category is in the graph to do so we iterate through the graph in BFS manner
                # starting from the root and descending level by level
                if not self.bfs_finder(category):
                    self.image_pairs[image] = 'invalid'
                    break

                # otherwise we just save the values
                self.image_pairs[image] = image_dict[image]

        return self.image_pairs

    def get_number_of_child_nodes(self, par_node):
        """
        In that function we calculate the number of direct child nodes to par_node
        :param par_node:
        :return: number of child nodes
        """
        # here we will directly use dict structure to get the number of child nodes
        # check if par_node has child nodes
        if par_node in self.graph:
            return len(self.graph[par_node])

        # otherwise return 0
        return 0

    def get_number_of_parent_child_nodes(self, cur_node):
        """
        In that function we calculate the number of direct child nodes to direct parent node
        :param cur_node:
        :return: number of child nodes
        """
        # create reversed graph
        self.reverse_graph()

        # we need to obtain a parent node for the cur_node
        par_node = self.reversed[cur_node]

        # now we can use already implemented function to calculate the number of direct child nodes
        return self.get_number_of_child_nodes(par_node)

    def bfs_finder(self, category):
        """
        Finds if the category is in the graph by
        Breadth First Search
        :param category:
        :return: Boolean
        """
        q = deque()
        q.append(self.root)
        while q:
            # if we found a category in queue then we break directly
            if category in q:
                return True

            elem = q.popleft()

            if elem in self.graph:
                for val in self.graph[elem]:
                    q.append(val)

        return False

    def reverse_graph(self):
        """
        Create a reversed graph copy in self.reversed
        :return:
        """
        # here we will directly use the dict structure to reverse the graph
        # in our task every child node has only one parent node
        # once we've reversed our graph as keys in dict we will have child nodes
        # as values we will have parent nodes
        res = {}
        for key in self.graph:
            for value in self.graph[key]:
                if value:
                    res[value] = key
        self.reversed = res
