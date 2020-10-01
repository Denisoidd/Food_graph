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
        print("Cur version")
        print("Children")
        print(self.cur_version.children)
        print("Parents")
        print(self.cur_version.parents)
        print("Ext version")
        print("Children")
        print(self.extract_version.children)
        print("Parents")
        print(self.extract_version.parents)
        # iterate over images
        for image, nodes in self.extract_information.items():
            # check if valid
            if nodes != 'invalid':
                # granularity_staged: label is matched but some labels have new child nodes in the database
                # that quote is taken from the exercise, but in my solution I will suppose that granularity
                # staged is place when child nodes added to the its root. Like it was shown in the example from
                # the assignment:
                # Extract
                # extract = {"img001": ["A"], "img002": ["C1"]}
                # Graph edits
                # edits = [("A1", "A"), ("A2", "A")]
                # Result
                # {"img001": "granularity_staged", "img002": "valid"}
                # So in that misinterpretation, I choose to work like in the example before.

                # iterate over each node in nodes
                granular = False
                coverage = False
                for node in nodes:
                    # print(node)
                    # print(self.cur_version.calculate_number_of_child_nodes(node))
                    # print(self.extract_version.calculate_number_of_child_nodes(node))
                    # print()
                    # check if cur_version and extracted one have different number of child nodes at that particular node
                    if self.cur_version.calculate_number_of_child_nodes(node) != self.extract_version.calculate_number_of_child_nodes(node):
                        granular = True

                    # check if parent nodes of cur_version and extracted have the same number of nodes
                    if self.cur_version.calculate_number_of_child_nodes(self.cur_version.parents[self.cur_version.children.index(node)]) != self.extract_version.calculate_number_of_child_nodes(self.extract_version.parents[self.extract_version.children.index(node)]):
                        granular = True
                        coverage = True
                        break
                if granular:
                    if coverage:
                        self.extract_information[image] = 'coverage_staged'
                    else:
                        self.extract_information[image] = 'granularity_staged'
                else:
                    self.extract_information[image] = 'valid'

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

    def calculate_number_of_child_nodes(self, par_node):
        return sum([1 for elem in self.parents if elem == par_node])
