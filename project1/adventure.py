
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

from dataclasses import dataclass, field
from game_entities import Location, Item, Question, question_bank
from proj1_event_logger import Event, EventList


@dataclass
class Gamestate:
    """A class to store the game state.

    Instance Attributes:
        - score: int indicating the score of the game
        - win_score: int setting the score to win the game
        - currstep: int saving the current step of player
        - maxstep: int setting the max step of player
        - ongoing: bool indicating whether the game is ongoing
        - inventory: list of Item objects representing the player's inventory
    """
    score: int = 0
    win_score: int = 25
    currstep: int = 0
    maxstep: int = 20
    ongoing: bool = True
    inventory: list[Item] = field(default_factory=list)
    output: bool = True


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - # TOD add descriptions of public instance attributes as needed
        - _locations: dict of Location objects representing the locations in the game
        - _items: list of Item objects representing the items in the game
        - menu: list of strings representing the menu options
        - interactions: list of strings representing the interaction options
        - current_location_id: int indicating the current location id of the game
        - output: bool indicating whether to output the game information
        - state: Gamestate object representing the game state
        - log: EventList object representing the game log

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
    menu: list[str]
    interactions: list[str]
    current_location_id: int
    state: Gamestate
    log: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, output: bool = True) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - initial_location_id in game_data_file
        """

        self._locations, self._items, questions = self._load_game_data(game_data_file)
        question_bank.add_questions(questions)
        self.menu = ['look', 'inventory', 'score', 'undo', 'log', 'quit', 'step']
        self.interactions = ['take', 'drop', 'use']
        self.current_location_id = initial_location_id  # game begins at this location
        self.state = Gamestate()
        self.state.output = output
        self.get_location().enter(self.state.output)
        self.log = EventList()
        self.log.add_event(Event(initial_location_id, self.get_location(initial_location_id).long_description))

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item], list[Question]]:
        """
        Load locations and items from a JSON file with the given filename and
        return a tuple consisting of
        (1) a dictionary of locations mapping each game location's ID to a Location object,
        (2) a list of all Item objects
        (3) a list of all Question objects
        """

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'], loc_data['available_commands'],
                                    loc_data['items'], loc_data.get('question_id', None))
            locations[loc_data['id']] = location_obj

        items = []
        for item in data['items']:
            item_obj = Item(item['name'], item['description'],
                            item['start_position'], item['target_position'],
                            item['target_points'], item.get('pick_up_conditions', []))
            items.append(item_obj)

        questions = []
        for question in data['questions']:
            question_obj = Question(question['description'], question['options'], question['answer'])
            questions.append(question_obj)
        return locations, items, questions

    def _display(self, *args, **kwargs) -> None:
        """Display the given arguments if self.output is True."""
        if self.state.output:
            print(*args, **kwargs)

    def get_location(self, loc_id: Optional[int] = None) -> Optional[Location]:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            loc_id = self.current_location_id
        for loc in self._locations:
            if loc == loc_id:
                return self._locations[loc]
        return None

    def get_item_obj(self, item_name: str) -> Optional[Item]:
        """Return Item object associated with the provided item name.
        If no name is provided, return None.
        """
        for item in self._items:
            if item.name == item_name:
                return item
        return None

    def action(self, command: str) -> bool:
        """Perform the given command in the current location.
        Return True if the command was successful, False otherwise.
        """
        # cheat command
        if command.startswith("jump"):
            self.current_location_id = int(command.split(" ")[1])
            return True
        loc = self.get_location()
        item_name = None
        if self._is_interact_cmd(command) and len(command.split(" ")) == 2:
            command, item_name = command.split(" ")
        answer = None
        if "," in command:
            command, answer = command.split(",")
        if not (command in loc.available_commands or command in self.menu or command in self.interactions):
            return False
        self._display("========")
        self._display("You decided to:", command)
        if command in loc.available_commands:
            self._handle_movement(command, answer)
        elif command in self.menu:
            self._handle_menu_command(command)
        elif command in self.interactions:
            self._handle_interaction(command, item_name)
        return True

    def _is_interact_cmd(self, command: str) -> bool:
        """Return True if the given command is an interaction command, False otherwise."""
        return any(command.startswith(s) for s in self.interactions)

    def _handle_movement(self, command: str, answer: Optional[str]) -> None:
        """Handle movement commands."""
        loc = self.get_location()
        self.current_location_id = loc.available_commands[command]
        new_loc = self.get_location()
        new_loc.enter(self.state.output)
        self.log.add_event(Event(self.current_location_id, new_loc.long_description), command)
        if not new_loc.answer_question(self.state.output, answer):
            self._display("Wrong answer!", end=" ")
            self.menu_undo()
        else:
            new_loc.visited = True
        self.check_lose()

    def _handle_menu_command(self, command: str) -> None:
        """Handle menu commands."""
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

    def _handle_interaction(self, command: str, item_name: Optional[str]) -> None:
        """Handle interaction commands."""
        if command == 'take':
            self.interact_take(item_name)
        elif command == 'drop':
            self.interact_drop(item_name)
        elif command == 'use':
            self.interact_use(item_name)

    def menu_look(self) -> None:
        """output the full description of the current location."""
        self._display(self.get_location().long_description)

    def menu_inventory(self) -> None:
        """output the player's inventory."""
        self._display("Inventory: " + str([item.name for item in self.state.inventory]))

    def menu_inventory_simple(self) -> None:
        """output the player's inventory in a simple format."""
        self._display("Inventory: " + str([item.name for item in self.state.inventory]))

    def menu_score(self) -> None:
        """output the player's score."""
        self._display("Score: " + str(self.state.score))

    def menu_log(self) -> None:
        """output the game log."""
        self.log.display_events()

    def menu_undo(self) -> None:
        """undo the last action."""
        # 撤销物品？
        if self.log.is_empty():
            self._display("No action to undo.")
            return
        self._display("Undo")
        lastevent = self.log.remove_last_event()
        if lastevent:
            target_object = self.get_item_obj(lastevent.split(' ', 1)[-1])
            # Undo take
            if "take" in lastevent:
                self.state.inventory.remove(target_object)
                self.get_location().add_item(target_object.name)
            elif "drop" in lastevent:
                self.state.inventory.append(target_object)
                self.get_location().remove_item(target_object.name)
            elif "use" in lastevent:
                self.state.score -= target_object.target_points
                self._items.append(target_object)
                self.state.inventory.append(target_object)

        self.current_location_id = self.log.get_last_event_id()

    def menu_quit(self) -> None:
        """quit the game."""
        self._display("Quit")
        self.state.ongoing = False

    def menu_step(self) -> None:
        """Return the remaining step of player"""
        self._display("Remaining steps: " + str(self.state.maxstep - self.state.currstep))

    def interact_take(self, item_name: Optional[str] = None) -> None:
        """Take an item from current location and add to inventory."""
        loc = self.get_location()
        if not loc.items:
            self._display("There are no items to pick up here.")
            return
        self._display("Available items:", loc.items)
        if item_name is None:
            item_name = input("Enter item name (or 'cancel' to abort): ").strip()
        if item_name == 'cancel':
            return
        item_obj = self.get_item_obj(item_name)
        if item_obj and item_name in loc.items:
            if not item_obj.can_pick_up([item.name for item in self.state.inventory]):
                self._display("You cannot pick up this item.")
                self._display("You need to get " + str(item_obj.pick_up_conditions))
                return
            loc.remove_item(item_name)
            self.state.inventory.append(item_obj)
            self._display(f"You picked up {item_name}.")
            target_loc = self.get_location(item_obj.target_position)
            self._display("You can use this item in " + target_loc.name + " to gain "
                          + str(item_obj.target_points) + " points.")

            if loc.id_num == item_obj.target_position:
                self._display(f"Delivered {item_name}! +{item_obj.target_points} points!")

            self.log.add_event(
                Event(loc.id_num, loc.long_description),
                command=f"take {item_name}"
            )
        else:
            self._display("Cannot take that item.")

    def interact_use(self, item_name: Optional[str] = None) -> None:
        """Use an item from inventory."""
        if not self._items:
            self._display("Inventory is empty.")
            return
        self._display("Inventory:", [item.name for item in self.state.inventory])
        if item_name is None:
            item_name = input("Enter item name to use (or 'cancel'): ").strip()
        if item_name == 'cancel':
            return
        item_to_use = self.get_item_obj(item_name)
        if item_to_use:
            if self.current_location_id == item_to_use.target_position:
                if item_name == "notebook" and not self.use_notebook():
                    return
                self.state.score += item_to_use.target_points
                self._display(f"Used {item_name}! Gained {item_to_use.target_points} points.")
                self.state.inventory.remove(item_to_use)
            else:
                self._display("This item cannot be used here.")
            self.log.add_event(Event(self.current_location_id, self.get_location().long_description),
                               command=f"use {item_name}")
            self.check_win()
        else:
            self._display("Item not found in inventory.")

    def interact_drop(self, item_name: Optional[str] = None) -> None:
        """Drop an item from inventory."""
        if not self.state.inventory:
            self._display("Inventory is empty, failed to drop.")
            return
        self._display("Available items:", [item.name for item in self.state.inventory])
        if item_name is None:
            item_name = input("Enter item name to drop (or 'cancel'): ").strip().lower()
        if item_name == "cancel":
            return
        elif item_name not in [item.name for item in self.state.inventory]:
            self._display("Item not found in inventory.")
            return

        item_to_drop = self.get_item_obj(item_name)
        loc = self.get_location()
        loc.add_item(item_name)
        self.state.inventory.remove(item_to_drop)
        self._display(f"You dropped {item_name}.")

        self.log.add_event(
            Event(loc.id_num, loc.long_description),
            command=f"drop {item_name}"
        )

    def use_notebook(self) -> bool:
        """Use notebook to answer question than gain points."""
        self._display("You used notebook to answer question.")
        cnt = 0
        for i in (2, 3, 4):
            self._display(f"Question {i - 1}:")
            question = question_bank.get_question(i)
            question.display()
            if question.check_answer():
                self._display("Correct!")
                cnt += 1
            else:
                self._display("Wrong!")
                break
        if cnt == 3:
            self._display("You got all questions correct!")
            return True
        return False

    def check_win(self) -> None:
        """Check if the player reach the score"""
        if self.state.score >= self.state.win_score:
            self._display("You win the game! :>")
            self.state.ongoing = False

    def check_lose(self) -> None:
        """Check if the player lose the game"""
        # currstep + 1 when player move
        self.state.currstep += 1
        if self.state.currstep >= self.state.maxstep:
            self._display("Sorry, you lose the game! :<")
            self.state.ongoing = False

    def run(self) -> None:
        """Run the game."""
        while self.state.ongoing:
            location = self.get_location()
            # Display possible actions at this location
            tips = "What to do? Choose from: "
            for cmd in self.menu:
                if cmd == "undo" and self.log.is_empty():
                    continue
                tips += cmd + ", "
            self._display(tips[:-2] + ".")
            self._display("At this location, you can also:")
            for action in location.available_commands:
                self._display("-", action)
            # Validate choice
            choice = input("\nEnter action: ").strip()
            while not self.action(choice):
                self._display("That was an invalid option; try again.")
                choice = input("\nEnter action: ").strip()


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    game.run()
