


# Enthought library imports
from enthought.traits.api import Any, Category, Enum, false, HasTraits, Instance, \
                                 Int, List, Trait, true

# Singleton representing the default Enable2 layout manager
DefaultLayoutController = LayoutController()


class ComponentLayoutCategory(Category, Component):

    """ Properties defining how a component should be laid out. """

    resizable = Enum('h', 'v')

    max_width = Any

    min_width = Any

    max_height = Any

    min_height = Any

    # Various alignment and positioning functions

    def set_padding(self, left, right, top, bottom):
        pass
    
    def get_padding(self):
        pass
