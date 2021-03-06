import datetime
import pickle
import os


class Odyssey:
    """Top level of your journey"""
    name = None
    children = []
    visiting = []
    save_file = None
    backup_dir = None

    def __init__(self, name):
        """Initialize a new Odyssey with your name"""
        self.name = name
        d, f = os.path.split(__file__)
        self.save_file = os.path.join(d, "data",
                                      ''.join(c if c.isalnum() else '_' for c in name) + '.ody')
        self.backup_dir = os.path.join(d, "data", "backup")

    def add_child(self, child):
        """Add a child (in this case a planet)"""
        self.children.append(child)
        child.parent = self

    def visit(self, *args, **kwargs):
        pass

    def save(self, fname=None, backup=True):
        if not fname:
            fname = self.save_file
        pickle.dump(self, fname)
        if backup:
            _, f = os.path.split(fname)
            pickle.dump(self, os.path.join(self.backup_dir,
                                           f[:-4], datetime.date.today(),
                                           'ody'))


class Visit:
    """A single visit to some Location"""
    place = None
    notes = []
    companions = []
    start_date = None
    end_date = None

    def __init__(self, place, date=datetime.date.today(), left=None,
                 notes=[], companions=[]):
        "Initialize a Visit"
        self.place = place
        self.start_date = date
        self.notes = notes
        self.companions = companions
        if left is not None:
            end_date = left

    def leave(self, date=datetime.date.today()):
        self.end_date = date

    def note(self, note):
        self.notes.append(note)

class Location:
    """All places should be subclassed from this"""
    name = None
    parent = None
    children = []
    visited = []
    current = False
    notes = []    # personal notes
    flavors = []  # types that don't deserve a subclass
    coords = None
    rating = None

    def __init__(self, name, flavors=[], parent=None):
        "Create a Location"
        self.name = name
        self.flavors = flavors
        self.parent = parent

    def add_child(self, child):
        """Add a child"""
        self.children.append(child)
        child.parent = self

    def add_new_child(self, *args, **kwargs):
        self.children.append(Location(*args, **kwargs))
        self.children[-1].parent = self

    def visit(self, *args, **kwargs):
        if not self.current:
            self.current = True
            self.visited.append(Visit(self, *args, **kwargs))
            self.parent.visit(*args, **kwargs)

    def leave(self, date=datetime.date.today()):
        if self.current:
            self.visited[-1].leave(date)
            self.current = False
            for child in self.children:
                child.leave(date)

    def note(self, note):
        self.notes.append(note)


def ymd(y, m, d):
    return datetime.date(y, m, d)
