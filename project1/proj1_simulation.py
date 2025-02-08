"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str],
                 output: bool = False) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id, output)

        current_location = self._game.get_location()
        event = Event(current_location.id_num, current_location.long_description, None, None, None)
        self._events.add_event(event)
        self.generate_events(commands)

    def generate_events(self, commands: list[str]) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        for cmd in commands:
            self._game.action(cmd)
        self._events = self._game.log
        return

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> simulation = AdventureGameSimulation('game_data.json', 1, ["go north,B"])
        >>> simulation.get_id_log()
        [1, 2]

        >>> simulation = AdventureGameSimulation('game_data.json', 1, ["go north,B", "take library_card"])
        >>> simulation.get_id_log()
        [1, 2, 2]
        """

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""
        current_event = self._events.first  # Start from the first event in the list
        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)
            # Move to the next event in the linked list
            current_event = current_event.next

    def get_score(self) -> int:
        """Return the current score of the game."""
        return self._game.state.score

    def get_currstep(self) -> int:
        """Return the current step of the game."""
        return self._game.state.currstep


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
    # from doctest import testmod
    # testmod()
    win_walkthrough = [
        "go north,B",
        "take library_card",
        "go north",
        "go east,C",
        "take laptop_charger",
        "go north",
        "go west",
        "go south",
        "take notebook",
        "go east",
        "go north",
        "go north",
        "take lab_key",
        "go south",
        "go south",
        "take USB_drive",
        "go north",
        "go west",
        "go south",
        "take lucky_mug",
        "use lucky_mug",
        "use USB_drive",
        "use laptop_charger"
    ]

    # Expected location IDs for the win walkthrough
    expected_win_log = [1, 2, 2, 3, 5, 5, 6, 10, 11, 11, 9, 8, 12, 12, 8, 9, 9, 8, 7, 4, 4, 4, 4, 4]

    sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough)
    assert expected_win_log == sim.get_id_log()
    sim.run()
    print(sim.get_score, sim.get_currstep)

    lose_demo = [
        "go north,B",
        "take library_card",
        "go north",
        "go east,C",
        "take laptop_charger",
        "go north",
        "go west",
        "go south",
        "take notebook",
        "go east",
        "go north",
        "go west",
        "take coffee",
        "go east",
        "use coffee",
        "go north",
        "take lab_key",
        "go south",
        "go south",
        "use USB_drive",
        "go east",
        "go west",
        "use laptop_charger",
        "take lucky_mug",
        "use lucky_mug",
        "go north",
        "go east",
        "go north",
        "go south",
        "go east",
        "go south",
        "go west"
    ]
    expected_log = [1, 2, 2, 3, 5, 5, 6, 10, 11, 11, 9, 8, 7, 7, 8, 8, 12, 12, 8, 9, 9, 1, 9, 9, 9, 8, 12, 8, 9, 11]
    sim = AdventureGameSimulation('game_data.json', 1, lose_demo)
    assert expected_log == sim.get_id_log()
    sim.run()

    inventory_demo = ["go north,B", "inventory", "take library_card", "inventory"]
    expected_log = [1, 2, 2]
    sim = AdventureGameSimulation("game_data.json", 1, inventory_demo, True)
    assert expected_log == sim.get_id_log()
    sim.run()

    scores_demo = ["go west", "go north", "go west", "go south",
                   "score", "take lucky_mug", "use lucky_mug", "score"]
    expected_log = [1, 9, 8, 7, 4, 4, 4]
    sim = AdventureGameSimulation("game_data.json", 1, scores_demo, True)
    assert expected_log == sim.get_id_log()
    sim.run()
