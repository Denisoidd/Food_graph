# Coding Assignment Food database
## How to run ?

Just copy the repository and run the main.py. It will be tested on json files in the repo.
To test on your own files you can load them in main.py file or you can create your own examples also in main.py.

## The idea behind 

In that section I'll explain in general words the way I've implemented a solution for that task. To get more details of implementation you can take a look at comments in the code. 

First of all in order to have an efficient data representation I've created two classes: `Database` and `Model`.

Class `Database` as it's been explained have 4 methods: 
* `__init__`
* `add_nodes`
* `add_extract`
* `get_extract_status`

In `__init__` method I have instantiated three variables within 
each class: `self.cur_version`, `self.extract_version`, `self.extract_information`. First two of them are `Model` instancies and the last is `dict`. From the name of these variables we
can understang that `self.cur_version` contains information about the current directed graph, `self.extract_version` - information about the directed graph version at the moment of 
`add_extract`function call and `self.extract_information` contains the valid information we need to extract.

Let's talk about `Model` class implementation. Firstly `Model` represents a directed graph structure implemented with using python `dict`. As a key it has a parent node, as a value it 
has a list of child nodes. 

This class has following functions: 
* `__init__` with `self.root`, `self.graph`, `self.image_pairs` and `self.reversed` (reversed graph), `add_nodes`
* `extract_valid` - check at the moment of extraction if image has invalid nodes (for example 'img1.jpg: ['E'] when there is no 'E' in the extracted graph)
* `get_number_of_child_nodes` - calculate the number of direct child nodes from the current node
* `get_number_of_parent_child_nodes` - calculate the number of direct child nodes from the direct parent node
* `bfs_finder` - finds the element in the graph by using Breadth First Search
* `reverse_graph` - reverse graph, this function is used in `get_number_of_parent_child_nodes` to find the parent of the current node

