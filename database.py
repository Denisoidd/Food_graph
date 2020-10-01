from copy import deepcopy

class Database(object):
    '''
    In Database we will have two Model object that will
    contain the information of current version and the
    version just before add_extract function.
    Once the function get_extract_status is called we
    will compare two versions and return for each image
    the result: 'valid', 'invalid', 'granularity_staged' and 'coverage_staged'
    '''
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
        print(self.cur_version.children)
        print(self.cur_version.parents)
        print(self.extract_version.children)
        print(self.extract_version.parents)
        return self.extract_information


class Model(object):
    '''
    Model class represent a directed graph.
    It contains add_nodes method and extract_valid
    '''
    def __init__(self, first_element):
        # here we initialize Model class with first_element
        # we have two lists, first one is responsible for child nodes
        # second one for parent node, we can have many child nodes but
        # one or None parent nodes
        self.children = [first_element]
        self.parents = [None]
        self.image_pairs = {}

    def add_nodes(self, nodes):
        for child, parent in nodes:
            self.children.append(child)
            self.parents.append(parent)

    def extract_valid(self, image_dict):
        # check the validity of asked nodes
        # if there is no valid node to extract
        # so image is invalid
        # we suppose that nodes added later doesn't count
        for image in image_dict:
            # we can have multiply categories for one image
            for category in image_dict[image]:
                # if we have only one invalid category so image is fully invalid
                if category not in self.children:
                    self.image_pairs[image] = 'invalid'
                    break
                self.image_pairs[image] = image_dict[image]

        return self.image_pairs
