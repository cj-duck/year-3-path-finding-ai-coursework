# Artificial Intelligence Coursework
# Christopher Johnson - 40275286
# Last Modified: 16/11/18

import sys
from math import sqrt

# Node class for storing node's and their attributes
class Node(): 

    def __init__(self, id=None, parent=None, position=None, neighbours=None):
        self.id = id
        self.parent = parent
        self.position = position
        self.neighbours = neighbours

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
# Read in file
filename = str(sys.argv[1]) + ".cav"
outputname = str(sys.argv[1])
caverns = []

# Create list from file
with open(filename, 'r') as f:
    caverns = f.read().split(',')

# Read first entry for total number of caverns
number_of_caverns = int(caverns[0])

def node(nodeID):
    
    newNode = Node()
    
    coords_index = 1 + ((nodeID - 1) * 2)
    
    neighbour_nodes = []
    neighbours_list = []

    # Find the nodes which you can travel to from this node aka neighbours
    count = 1
    while count < number_of_caverns + 1:
        neighbours_index = 1 + ((number_of_caverns * 2) + ((count - 1) * number_of_caverns))
        neighbours = caverns[neighbours_index:neighbours_index + number_of_caverns]
        neighbours_list.append(neighbours[nodeID-1])
        count = count + 1

    count = 1
    for x in neighbours_list:
        if str(x) == str(1):
            neighbour_nodes.append(count)
        count = count + 1       

    # Assign values to attributes
    newNode.id = nodeID
    newNode.position = caverns[coords_index:coords_index + 2]
    newNode.neighbours = neighbour_nodes

    return(newNode)

# a star search function
def aStar():

    # Create open and closed lists
    open_list = []
    closed_list = []

    # Set the start and end nodes using the node() function
    start_node = node(1)
    print("Start node: " + str(start_node.id))
    end_node = node(number_of_caverns)
    print("End node: " + str(end_node.id))

    # Add start node to open list
    open_list.append(start_node)

    while len(open_list) > 0:

        # Set current node to first item of the open list
        current_node = open_list[0]

        # Set current_node to the node with the lowest .f attribute
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        # Add the node with the lowest .f attribute to the closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # If the current node is the end node return the path by printing the node id and then setting it to it's parent node and repeating
        if current_node.id == end_node.id:
            path = []
            while current_node is not None:
                path.append(current_node.id)
                current_node = current_node.parent
            return path[::-1]
        
        # Create children list
        children = []

        # Make nodes for each of the current node's neighbours and add them to a children list
        for x in current_node.neighbours:
            child = node(x)
            child.parent = current_node
            children.append(child)

        for child in children:

            flag = 0

            # Check child is not already in the closed list, if it is move on to the next child
            for closed_child in closed_list:
                if child == closed_child:
                    flag = 1
            
            if flag == 1:
                continue
        
            # Calculate g (the distance between the current node and the child)
            child.g = current_node.g + sqrt(((int(child.position[0]) - int(current_node.position[0])) ** 2) + ((int(child.position[1]) - int(current_node.position[1])) ** 2))
            # Calculate h (heuristic distance between the child node and the end end)
            child.h = sqrt(((int(child.position[0]) - int(end_node.position[0])) ** 2) + ((int(child.position[1]) - int(end_node.position[1])) ** 2))
            # Calculate f (g + h)
            child.f = child.g + child.h

            # Check that the child's g value is less than the same node's child in the open list, if it is move on to the next child
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                   flag = 1
            
            if flag == 1:
                continue

            # If the child meets the above criteria add it to the open list
            open_list.append(child)

path = aStar()

with open(outputname + '.csn', 'w') as f:
        for item in path:
            f.write("%s " % item)
            


