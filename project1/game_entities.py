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
from dataclasses import dataclass, field

@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TOD Describe each instance attribute here
        - name: name of item
        - description: description of item
        - start_position: start position of item
        - target_position: target position of item
        - target_points: target points of item\
        - picked_up_conditions: a list of conditions that must be met to pick up the item

    Representation Invariants:
        - # TOD Describe any necessary representation invariants
        - start_position != target_position
        - target_points > 0
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int
    pick_up_conditions: list[str] = field(default_factory=list)

    # judge whether this item can be picked up
    def can_pick_up(self, inventory: list[str]) -> bool:
        """Return whether this item can be picked up."""
        for cond in self.pick_up_conditions:
            if cond not in inventory:
                return False
        return True


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - # TOD Describe each instance attribute here
        - id_num: int id
        - brief_description: brief description
        - long_description: long description
        - available_commands: a mapping of available commands
        - items: a list of item names
        - visited: a boolean indicating whether this location has been visited

    Representation Invariants:
        - # TOD Describe any necessary representation invariants
        - available_commands != {}
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool = False

    # 进入场景
    def enter(self) -> None:
        """Enter this location."""
        if self.visited:
            print(self.brief_description)
        else:
            print(self.long_description)
            self.visited = True
    
    def remove_item(self, item_name: str):
        """Remove item from this location."""
        self.items.remove(item_name)
    
    def add_item(self, item_name: str) -> None:
        """Add item to this location."""
        self.items.append(item_name)


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    # pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
