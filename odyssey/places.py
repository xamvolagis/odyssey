import datetime


class Odyssey:
    """Top level of your journey"""
    name = None
    children = []

    def __init__(self, name):
        """Initialize a new odyssey with your name"""
        self.name = name

    def add_child(self, child):
        """Add a child (in this case a planet)"""
        self.children.append(child)


class Place:
    """All places should be subclassed from this"""
    name = None
    parent = None
    children = []
    visited = []
    notes = []    # personal notes
    flavors = []  # types that don't deserve a subclass

    def __init__(self, name, flavors=[]):
        ""

