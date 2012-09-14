from src.model.node.Node import Node

__author__ = 'jontedesco'

class Venue(Node):
    """
      Node representing a venue (conference) in the DBLP data set
    """

    def __init__(self, id, name):
        super(Venue, self).__init__(id)

        self.name = name