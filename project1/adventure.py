"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - # TOD add descriptions of public instance attributes as needed
        - _locations: dict of Location objects representing the locations in the game
        - _items: list of Item objects representing the items in the game
        - _log: EventList object representing the game log
        - _menu: list of strings representing the menu options
        - current_location_id: int indicating the current location id of the game
        - ongoing: bool indicating whether the game is ongoing
        - score: current score of player

    Representation Invariants:
        - # TOD add any appropriate representation invariants as needed
        - current_location_id in _locations
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    log: EventList
    menu: list[str]
    interactions: list[str]
    current_location_id: int  # Suggested attribute, can be removed
    score: int
    ongoing: bool  # Suggested attribute, can be removed

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)
        self.log = EventList()

        self.menu = ['look', 'inventory', 'score', 'undo', 'log', 'quit']
        self.interactions = ['take', 'drop', 'use']
        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.score = 0
        # enter初始位置
        self.get_location().enter()

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        # TOD: Add Item objects to the items list; your code should be structured similarly to the loop above
        # YOUR CODE BELOW
        for item in data['items']:
            item_obj = Item(item['name'], item['start_position'], item['target_position'], item['target_points'],
                            item['description'])
            items.append(item_obj)
        return (locations, items)

    def get_location(self, loc_id: Optional[int] = None) -> Optional[Location]:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TOD: Complete this method as specified
        # YOUR CODE BELOW
        if loc_id is None:
            loc_id = self.current_location_id
        for loc in self._locations.keys():
            if loc == loc_id:
                return self._locations[loc]
        return None

    def action(self, command: str) -> bool:
        """Perform the given command in the current location.
        Return True if the command was successful, False otherwise.
        """

        loc = self.get_location()
        if not (command in loc.available_commands or command in self.menu or command in self.interactions):
            return False
        print("========")
        print("You decided to:", command)
        if command in loc.available_commands:
            self.current_location_id = cur = loc.available_commands[command]
            loc = self.get_location()
            loc.enter()
            self.log.add_event(Event(cur, loc.long_description), command)
        elif command in self.menu:
            if command == 'look':
                self.menu_look()
            elif command == 'inventory':
                self.menu_inventory()
            elif command == 'score':
                self.menu_score()
            elif command == 'undo':
                self.menu_undo()
            elif command == 'log':
                self.menu_log()
            elif command == 'quit':
                self.menu_quit()
        elif command in self.interactions:
            if command == 'take':
                self.interact_take()
        return True

    def menu_look(self) -> None:
        print(self.get_location().long_description)

    def menu_inventory(self):
        print("Inventory: " + str(self._items))

    def menu_score(self):
        print("Score: " + str(self.score))

    def menu_log(self):
        self.log.display_events()

    def menu_undo(self):
        if(self.log.is_empty()):
            print("No action to undo.")
            return
        print("Undo")
        self.log.remove_last_event()
        self.current_location_id = self.log.get_last_event_id()

    def menu_quit(self):
        print("Quit")
        self.ongoing = False

    def interact_take(self) -> None:
        """Take the item from the current location"""
        loc = self.get_location()
        print("Enter 'cancel' to cancel")
        print("You can take: " + str(loc.items))
        item_name = input("Enter item name: ")
        if item_name == 'cancel' or item_name not in loc.items:
            return
        item = loc.remove_item(item_name)
        self._items.append(item)
        print("You took " + item.name + "from" + loc.name)

if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    # game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None
    # print(game.log.is_empty())

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()

        # TOD: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE


        # TOD: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        # YOUR CODE HERE

        # Display possible actions at this location

        tips = "What to do? Choose from: "
        for cmd in game.menu:
            if cmd == "undo" and game.log.is_empty():
                continue
            tips += cmd + ", "
        print(tips[:-2] + ".")
        print("At this location, you can also:")
        # print(location.available_commands)
        for action in location.available_commands:
            print("-", action, end='\n')

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while not game.action(choice):
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        # if choice in menu:
        #     # TOD: Handle each menu command as appropriate
        #     # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
        #     if choice == "log":
        #         game_log.display_events()
        #     # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
        #
        # else:
        #     # Handle non-menu actions
        #     result = location.available_commands[choice]
        #     game.current_location_id = result
        #
        #     # TOD: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
        #     # TOD: Add in code to deal with special locations (e.g. puzzles) as needed for your game
