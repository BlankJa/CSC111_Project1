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
from typing import Optional


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name of item
        - description: description of item
        - start_position: start position of item
        - target_position: target position of item
        - target_points: target points of item\
        - picked_up_conditions: a list of conditions that must be met to pick up the item

    Representation Invariants:
        - start_position != target_position
        - target_points > 0
    """

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
        - id_num: int id
        - brief_description: brief description
        - long_description: long description
        - available_commands: a mapping of available commands
        - items: a list of item names
        - visited: a boolean indicating whether this location has been visited

    Representation Invariants:
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
    question_id: Optional[int] = None
    visited: bool = False

    # 进入场景
    def enter(self, output: bool) -> None:
        """Enter this location."""
        description = self.brief_description
        if not self.visited:
            description = self.long_description
        if output:
            print(description)

    def answer_question(self, output: bool, answer: Optional[str] = None) -> bool:
        """
        Display the question of this location and
        check if the user's answer is correct.
        """
        if self.question_id is None or self.visited:
            return True
        question = question_bank.get_question(self.question_id)
        if output:
            question.display()
        return question.check_answer(answer)

    def remove_item(self, item_name: str) -> None:
        """Remove item from this location."""
        self.items.remove(item_name)

    def add_item(self, item_name: str) -> None:
        """Add item to this location."""
        self.items.append(item_name)


@dataclass
class Question:
    """A question in our text adventure game world.
    Instance Attributes:
        - description: description
        - options: options
        - answer: answer
    """
    description: str
    options: list[str]
    answer: str

    def display(self) -> None:
        """Display this question."""
        print(self.description)
        for i, option in enumerate(self.options, start=65):
            print(f"{chr(i)}. {option}")

    def check_answer(self, answer: Optional[str] = None) -> bool:
        """Check if the user's answer is correct."""
        if answer is None:
            answer = input("Your answer: ")
        return answer.lower() == self.answer


@dataclass
class QuestionBank:
    """A bank of questions in our text adventure game world.
    Instance Attributes:
        - questions: a list of questions
    """
    questions: list[Question] = field(default_factory=list)

    def get_question(self, index: int) -> Question:
        """Get the question at the given index."""
        return self.questions[index]

    def add_questions(self, questions: list[Question]) -> None:
        """Add questions to the bank."""
        self.questions.extend(questions)


question_bank = QuestionBank()

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
