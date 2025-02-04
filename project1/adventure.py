
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
        - score: int indicating the score of the game
        - ongoing: bool indicating whether the game is ongoing

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
    # _menu: dict[str, function]
    menu: list[str]
    interactions: list[str]
    inventory: list[Item]
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
        self.menu = ['look', 'inventory', 'score', 'undo', 'log', 'quit', 'step']
        self.interactions = ['take', 'drop', 'use']
        self.inventory = []
        self.current_location_id = initial_location_id  # game begins at this location
        self.score = 0  # player's score
        self.ongoing = True  # whether the game is ongoing
        # 进入初始位置
        self.get_location().enter()
        self.log.add_event(Event(initial_location_id, self.get_location(initial_location_id).long_description))
        self.win_score = 25
        self.currstep = 0
        self.maxstep = 27  # 最大步数暂定27

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            # print(loc_data['available_commands'])
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        # TOD: Add Item objects to the items list; your code should be structured similarly to the loop above
        # YOUR CODE BELOW
        for item in data['items']:
            item_obj = Item(item['name'], item['description'], item['start_position'], item['target_position'], item['target_points'])
            items.append(item_obj)
        return locations, items

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
        # 输入的 loc_id 不存在
        return None

    def get_item_obj(self, item_name: str) -> Optional[Item]:
        """Return Item object associated with the provided item name.
        If no name is provided, return None.
        """
        return next((item for item in self._items if item.name == item_name), None)

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
            self.check_lose()
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
            elif command == 'step':
                self.menu_step()
        elif command in self.interactions:
            if command == 'take':
                self.interact_take()
            elif command == 'drop':
                self.interact_drop()
            elif command == 'use':
                self.interact_use()
        return True

    def menu_look(self) -> None:
        """output the full description of the current location."""
        print(self.get_location().long_description)

    def menu_inventory(self):
        """output the player's inventory."""
        # print("Inventory: " + str(self.inventory))
        print("Inventory: " + str([item.name for item in self.inventory]))

    def menu_score(self):
        """output the player's score."""
        print("Score: " + str(self.score))

    def menu_log(self):
        """output the game log."""
        self.log.display_events()

    def menu_undo(self):
        """undo the last action."""
        # 撤销物品？
        if self.log.is_empty():
            print("No action to undo.")
            return
        print("Undo")
        lastevent = self.log.remove_last_event()
        if lastevent:
            target_object = self.get_item_obj(lastevent.split(' ', 1)[-1])
            # 撤销 take
            if "take" in lastevent:
                self.inventory.remove(target_object)
                self.get_location().add_item(target_object.name)
            elif "drop" in lastevent:
                self.inventory.append(target_object)
                self.get_location().remove_item(target_object.name)
            elif "use" in lastevent:
                self.score -= target_object.target_points
                self._items.append(target_object)
                self.inventory.append(target_object)

        self.current_location_id = self.log.get_last_event_id()

    def menu_quit(self):
        """quit the game."""
        print("Quit")
        self.ongoing = False

    def menu_step(self):
        """Return the total step of player"""
        print("Currentstep: " + str(self.currstep))
        print("Maximum step: " + str(self.maxstep))

    def interact_take(self) -> None:
        """Take an item from current location and add to inventory."""
        loc = self.get_location()
        if not loc.items:
            print("There are no items to pick up here.")
            return
        print("Available items:", loc.items)
        item_name = input("Enter item name (or 'cancel' to abort): ").strip()
        if item_name == 'cancel':
            return

        item_obj = self.get_item_obj(item_name)

        if item_obj and item_name in loc.items:
            loc.remove_item(item_name)
            self.inventory.append(item_obj)
            print(f"You picked up {item_name}.")
            # 给出target_position的名字
            target_loc = self.get_location(item_obj.target_position)
            print("You can use this item in " + target_loc.name + " to gain " + str(item_obj.target_points) + " points.")

            if loc.id_num == item_obj.target_position:
                self.score += item_obj.target_points
                print(f"Delivered {item_name}! +{item_obj.target_points} points!")

            self.log.add_event(
                Event(loc.id_num, loc.long_description),
                command=f"take {item_name}"
            )
        else:
            print("Cannot take that item.")

    def interact_use(self) -> None:
        """Use an item from inventory."""
        if not self._items:
            print("Inventory is empty.")
            return
        print("Inventory:", [item.name for item in self.inventory])
        item_name = input("Enter item name to use (or 'cancel'): ").strip()
        if item_name == 'cancel':
            return
        item_to_use = self.get_item_obj(item_name)
        if item_to_use:
            # 检查是否在目标位置
            if self.current_location_id == item_to_use.target_position:
                self.score += item_to_use.target_points
                print(f"Used {item_name}! Gained {item_to_use.target_points} points.")
                self._items.remove(item_to_use)
                self.inventory.remove(item_to_use)
            else:
                print("This item cannot be used here.")
            # 记录事件
            self.log.add_event(Event(self.current_location_id, self.get_location().long_description),
                               command=f"use {item_name}")
            self.check_win()
        else:
            print("Item not found in inventory.")

    def interact_drop(self) -> None:
        """Drop an item from inventory."""
        if not self.inventory:
            print("Inventory is empty, failed to drop.")
            return
        print("Available items:", [item.name for item in self.inventory])
        item_name = input("Enter item name to drop (or 'cancel'): ").strip()
        if item_name == "cancel":
            return
        elif item_name not in [item.name for item in self.inventory]:
            print("Item not found in inventory.")
            return

        item_to_drop = self.get_item_obj(item_name)
        loc = self.get_location()
        loc.add_item(item_name)
        self.inventory.remove(item_to_drop)
        print(f"You dropped {item_name}.")

        self.log.add_event(
            Event(loc.id_num, loc.long_description),
            command=f"drop {item_name}"
        )

    def check_win(self) -> None:
        """Check if the player reach the score"""
        if self.score >= self.win_score:
            print("You win the game! :>")
            self.ongoing = False

    def check_lose(self) -> None:
        """Check if the player lose the game"""
        # currstep + 1 when player move
        self.currstep += 1
        if self.currstep >= self.maxstep:
            print("Sorry, you lose the game! :<")
            self.ongoing = False


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    # AdventureGame 中有一个 EventList 类，用于存储游戏的事件日志
    #game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.
        location = game.get_location()
        # Display possible actions at this location
        tips = "What to do? Choose from: "
        for cmd in game.menu:
            if cmd == "undo" and game.log.is_empty():
                continue
            tips += cmd + ", "
        print(tips[:-2] + ".")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while not game.action(choice):
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()


        # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
        # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game
