"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TOD Describe each instance attribute here
        - start_position: the start position of the item
        - name: item's name
        - target_position: target position of item
        - target_points: target point of item
        - description: description of item

    Representation Invariants:
        - # TOD Describe any necessary representation invariants
        - target_ponints > 0
        - start_position != target_position
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    start_position: int
    target_position: int
    target_points: int
    description: str


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - # TOD Describe each instance attribute here
        - id_num: integer id for this location
        - brief_description: brief description of this location
        - available_commands: a mapping of available commands at this location to
                                the location executing that command would lead to
        - long_description: long description of this location
        - items: a list of item
        - visited: whether this location has been visited or not

    Representation Invariants:
        - # TOD Describe any necessary representation invariants
        - available_commands != {}
    """
    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[Item]
    visited: bool = False

    def enter(self) -> None:
        if self.visited:
            print(self.brief_description)
        else:
            print(self.long_description)
            self.visited = True

    def remove_item(self, item_name: str) -> Item | None:
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return item

    def add_item(self, item: Item) -> None:
        """Add item to this location"""
        self.items.append(item)

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    def __init__(self, name, location_id, brief_description, long_description, available_commands, items,
                 visited=False) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """
        
        self.id_num = location_id
        self.name = name
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited




# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
